const video = document.getElementById('video');
const overlay = document.getElementById('overlay');
const ctx = overlay.getContext('2d');
const toggleBtn = document.getElementById('toggle');
const logBtn = document.getElementById('log');
const intervalSelect = document.getElementById('interval');
const statusEl = document.getElementById('status');
const dominantEl = document.getElementById('dominant');
const confEl = document.getElementById('conf');
const samplesEl = document.getElementById('samples');
const autoLogCheckbox = document.getElementById('autoLog');

let detectionInterval = 1000;
let running = false;
let loopHandle = null;
let sessionId = crypto.getRandomValues(new Uint32Array(4)).join('-');
let lastDetection = null;
let lastAutoSentAt = 0;

let chart;

function initChart() {
  const ctx = document.getElementById('chart');
  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['neutral', 'happy', 'sad', 'angry', 'fearful', 'disgusted', 'surprised'],
      datasets: [{
        label: 'Detections (last hour)',
        data: [0,0,0,0,0,0,0],
        backgroundColor: 'rgba(110,168,254,0.5)',
        borderColor: 'rgba(110,168,254,1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });
}

async function setupCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
  video.srcObject = stream;
  await new Promise(r => video.onloadedmetadata = r);
  overlay.width = video.videoWidth;
  overlay.height = video.videoHeight;
}

async function loadModels() {
  const base = 'https://justadudewhohacks.github.io/face-api.js/models';
  await Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri(base),
    faceapi.nets.faceExpressionNet.loadFromUri(base)
  ]);
}

function getDominant(expressions) {
  let topKey = null;
  let topVal = -Infinity;
  for (const [k,v] of Object.entries(expressions)) {
    if (v > topVal) { topVal = v; topKey = k; }
  }
  return { emotion: topKey, confidence: topVal };
}

async function detectOnce() {
  const detection = await faceapi.detectSingleFace(
    video,
    new faceapi.TinyFaceDetectorOptions({ inputSize: 224, scoreThreshold: 0.5 })
  ).withFaceExpressions();

  ctx.clearRect(0, 0, overlay.width, overlay.height);

  if (!detection) {
    statusEl.textContent = 'No face detected';
    dominantEl.textContent = '—';
    confEl.textContent = '—';
    return null;
  }

  const { box } = detection.detection;
  const dom = getDominant(detection.expressions);

  // draw box
  ctx.strokeStyle = 'rgba(110,168,254,0.9)';
  ctx.lineWidth = 3;
  ctx.strokeRect(box.x, box.y, box.width, box.height);

  // draw label
  ctx.fillStyle = 'rgba(0,0,0,0.6)';
  ctx.fillRect(box.x, Math.max(0, box.y - 26), 160, 24);
  ctx.fillStyle = '#eaf2ff';
  ctx.font = '600 14px Inter, sans-serif';
  ctx.fillText(`${dom.emotion} ${(dom.confidence*100).toFixed(1)}%`, box.x + 8, Math.max(12, box.y - 8));

  dominantEl.textContent = dom.emotion;
  confEl.textContent = (dom.confidence * 100).toFixed(1) + '%';
  statusEl.textContent = 'Detecting…';

  lastDetection = dom;
  if (autoLogCheckbox.checked) {
    const now = Date.now();
    if (now - lastAutoSentAt > Math.max(2000, detectionInterval)) {
      lastAutoSentAt = now;
      sendLastDetection();
    }
  }
  return dom;
}

function startLoop() {
  if (loopHandle) clearInterval(loopHandle);
  loopHandle = setInterval(detectOnce, detectionInterval);
}

async function refreshAggregate() {
  try {
    const res = await fetch('/api/moods/recent?minutes=60');
    if (!res.ok) throw new Error('Failed');
    const data = await res.json();
    samplesEl.textContent = String(data.sampleCount || 0);

    const order = ['neutral', 'happy', 'sad', 'angry', 'fearful', 'disgusted', 'surprised'];
    chart.data.datasets[0].data = order.map(k => data.totals?.[k] ?? 0);
    chart.update();
  } catch (e) {
    // Ignore if backend not running yet
  }
}

async function sendLastDetection() {
  if (!lastDetection) return;
  try {
    const payload = {
      emotion: lastDetection.emotion,
      confidence: lastDetection.confidence,
      clientTime: new Date().toISOString(),
      sessionId,
      source: 'face-api.js'
    };
    const res = await fetch('/api/moods', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed');
    await refreshAggregate();
    statusEl.textContent = 'Logged to server';
  } catch (e) {
    statusEl.textContent = 'Log failed';
  }
}

function wireUI() {
  toggleBtn.addEventListener('click', async () => {
    if (!running) {
      detectionInterval = Number(intervalSelect.value);
      startLoop();
      toggleBtn.textContent = 'Pause';
      running = true;
      statusEl.textContent = 'Detecting…';
    } else {
      if (loopHandle) clearInterval(loopHandle);
      toggleBtn.textContent = 'Start';
      running = false;
      statusEl.textContent = 'Paused';
    }
  });

  intervalSelect.addEventListener('change', () => {
    detectionInterval = Number(intervalSelect.value);
    if (running) startLoop();
  });

  logBtn.addEventListener('click', sendLastDetection);
}

(async function main() {
  initChart();
  try {
    await setupCamera();
    await loadModels();
    statusEl.textContent = 'Ready';
    await refreshAggregate();
  } catch (e) {
    statusEl.textContent = 'Camera or model load failed';
  }
  wireUI();
})();
