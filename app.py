from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from fer import FER
import base64
import json
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Initialize emotion detector
emotion_detector = FER(mtcnn=True)

# Store mood data
mood_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_mood', methods=['POST'])
def analyze_mood():
    try:
        # Get image data from request
        data = request.get_json()
        image_data = data['image']
        
        # Remove data URL prefix
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect emotions
        result = emotion_detector.detect_emotions(image_rgb)
        
        if result:
            emotions = result[0]['emotions']
            dominant_emotion = max(emotions, key=emotions.get)
            confidence = emotions[dominant_emotion]
            
            # Store mood data
            mood_entry = {
                'timestamp': datetime.now().isoformat(),
                'emotion': dominant_emotion,
                'confidence': float(confidence),
                'all_emotions': emotions
            }
            mood_data.append(mood_entry)
            
            return jsonify({
                'success': True,
                'emotion': dominant_emotion,
                'confidence': float(confidence),
                'all_emotions': emotions
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No face detected'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/mood_history')
def mood_history():
    return jsonify(mood_data)

@app.route('/mood_chart')
def mood_chart():
    if not mood_data:
        return jsonify({'error': 'No mood data available'})
    
    # Create mood chart
    emotions = [entry['emotion'] for entry in mood_data]
    timestamps = [entry['timestamp'] for entry in mood_data]
    
    # Count emotions
    emotion_counts = {}
    for emotion in emotions:
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(emotion_counts.values(), labels=emotion_counts.keys(), autopct='%1.1f%%')
    plt.title('Mood Distribution')
    
    # Save to bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return jsonify({'chart': img_base64})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)