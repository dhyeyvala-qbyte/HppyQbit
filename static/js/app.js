class MoodTracker {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.stream = null;
        this.isTracking = false;
        
        this.initializeElements();
        this.bindEvents();
    }
    
    initializeElements() {
        this.startBtn = document.getElementById('startBtn');
        this.captureBtn = document.getElementById('captureBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.currentMood = document.getElementById('currentMood');
        this.emotionIcon = document.getElementById('emotionIcon');
        this.emotionName = document.getElementById('emotionName');
        this.confidence = document.getElementById('confidence');
        this.emotionBreakdown = document.getElementById('emotionBreakdown');
        this.emotionBars = document.getElementById('emotionBars');
        this.historyList = document.getElementById('historyList');
        this.viewHistoryBtn = document.getElementById('viewHistoryBtn');
        this.clearHistoryBtn = document.getElementById('clearHistoryBtn');
        this.chartModal = document.getElementById('chartModal');
        this.chartContainer = document.getElementById('chartContainer');
    }
    
    bindEvents() {
        this.startBtn.addEventListener('click', () => this.startCamera());
        this.captureBtn.addEventListener('click', () => this.captureMood());
        this.stopBtn.addEventListener('click', () => this.stopCamera());
        this.viewHistoryBtn.addEventListener('click', () => this.viewHistory());
        this.clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        
        // Modal close events
        document.querySelector('.close').addEventListener('click', () => {
            this.chartModal.style.display = 'none';
        });
        
        window.addEventListener('click', (event) => {
            if (event.target === this.chartModal) {
                this.chartModal.style.display = 'none';
            }
        });
    }
    
    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: 640, 
                    height: 480,
                    facingMode: 'user'
                } 
            });
            
            this.video.srcObject = this.stream;
            this.video.play();
            
            this.startBtn.disabled = true;
            this.captureBtn.disabled = false;
            this.stopBtn.disabled = false;
            
            this.isTracking = true;
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            alert('Unable to access camera. Please ensure you have granted permission.');
        }
    }
    
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        this.video.srcObject = null;
        this.startBtn.disabled = false;
        this.captureBtn.disabled = true;
        this.stopBtn.disabled = true;
        
        this.isTracking = false;
        
        // Reset display
        this.emotionIcon.textContent = '😐';
        this.emotionName.textContent = 'Neutral';
        this.confidence.textContent = '0%';
        this.emotionBreakdown.style.display = 'none';
    }
    
    captureMood() {
        if (!this.isTracking) return;
        
        // Set canvas dimensions to match video
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        
        // Draw current frame to canvas
        this.ctx.drawImage(this.video, 0, 0);
        
        // Convert to base64
        const imageData = this.canvas.toDataURL('image/jpeg', 0.8);
        
        // Show loading state
        this.captureBtn.innerHTML = '<div class="loading"></div> Analyzing...';
        this.captureBtn.disabled = true;
        
        // Send to server for analysis
        this.analyzeMood(imageData);
    }
    
    async analyzeMood(imageData) {
        try {
            const response = await fetch('/analyze_mood', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayMood(result);
                this.addToHistory(result);
            } else {
                alert('Error: ' + result.message);
            }
            
        } catch (error) {
            console.error('Error analyzing mood:', error);
            alert('Error analyzing mood. Please try again.');
        } finally {
            // Reset button
            this.captureBtn.innerHTML = '<i class="fas fa-camera"></i> Capture Mood';
            this.captureBtn.disabled = false;
        }
    }
    
    displayMood(result) {
        const emotion = result.emotion;
        const confidence = Math.round(result.confidence * 100);
        
        // Update main display
        this.emotionIcon.textContent = this.getEmotionEmoji(emotion);
        this.emotionName.textContent = this.capitalizeFirst(emotion);
        this.confidence.textContent = confidence + '%';
        
        // Show emotion breakdown
        this.showEmotionBreakdown(result.all_emotions);
        
        // Add animation
        this.emotionIcon.style.animation = 'none';
        setTimeout(() => {
            this.emotionIcon.style.animation = 'bounce 1s ease-in-out';
        }, 10);
    }
    
    showEmotionBreakdown(emotions) {
        this.emotionBars.innerHTML = '';
        
        // Sort emotions by confidence
        const sortedEmotions = Object.entries(emotions)
            .sort(([,a], [,b]) => b - a);
        
        sortedEmotions.forEach(([emotion, confidence]) => {
            const bar = document.createElement('div');
            bar.className = 'emotion-bar';
            
            const percentage = Math.round(confidence * 100);
            
            bar.innerHTML = `
                <span class="emotion-label">${this.capitalizeFirst(emotion)}</span>
                <div class="bar-container">
                    <div class="bar-fill" style="width: ${percentage}%"></div>
                </div>
                <span class="bar-value">${percentage}%</span>
            `;
            
            this.emotionBars.appendChild(bar);
        });
        
        this.emotionBreakdown.style.display = 'block';
    }
    
    addToHistory(result) {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        
        historyItem.innerHTML = `
            <div>
                <span class="emotion">${this.getEmotionEmoji(result.emotion)} ${this.capitalizeFirst(result.emotion)}</span>
                <div class="timestamp">${timeString}</div>
            </div>
            <div class="confidence">${Math.round(result.confidence * 100)}%</div>
        `;
        
        // Remove "no data" message if it exists
        const noData = this.historyList.querySelector('.no-data');
        if (noData) {
            noData.remove();
        }
        
        // Add to top of list
        this.historyList.insertBefore(historyItem, this.historyList.firstChild);
    }
    
    async viewHistory() {
        try {
            const response = await fetch('/mood_chart');
            const result = await response.json();
            
            if (result.chart) {
                this.chartContainer.innerHTML = `<img src="data:image/png;base64,${result.chart}" alt="Mood Chart">`;
                this.chartModal.style.display = 'block';
            } else {
                alert('No mood data available to display chart.');
            }
        } catch (error) {
            console.error('Error loading chart:', error);
            alert('Error loading mood chart.');
        }
    }
    
    clearHistory() {
        if (confirm('Are you sure you want to clear all mood history?')) {
            this.historyList.innerHTML = '<p class="no-data">No mood data yet. Start tracking your emotions!</p>';
            // Note: In a real app, you'd also clear the server-side data
        }
    }
    
    getEmotionEmoji(emotion) {
        const emojiMap = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'fear': '😨',
            'surprise': '😲',
            'disgust': '🤢',
            'neutral': '😐'
        };
        return emojiMap[emotion] || '😐';
    }
    
    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MoodTracker();
});