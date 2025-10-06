# Mood Tracker - Webcam Emotion Detection

A web application that tracks your mood using real-time facial emotion recognition through your device's webcam. Built with Python Flask, OpenCV, and modern web technologies.

## Features

- 🎥 **Real-time Webcam Access**: Uses your device's camera to capture facial expressions
- 😊 **Emotion Detection**: Detects 7 different emotions (happy, sad, angry, fear, surprise, disgust, neutral)
- 📊 **Mood History**: Tracks and stores your mood over time
- 📈 **Visualization**: Beautiful charts showing mood distribution
- 🎨 **Modern UI**: Responsive design with smooth animations
- 📱 **Mobile Friendly**: Works on desktop and mobile devices

## Screenshots

The application features:
- Live camera feed with face detection overlay
- Real-time emotion analysis with confidence scores
- Emotion breakdown showing all detected emotions
- Mood history with timestamps
- Interactive pie chart visualization

## Installation

### Prerequisites

- Python 3.7 or higher
- A webcam-enabled device
- Modern web browser with camera access

### Setup

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Start the Camera**: Click "Start Camera" to begin webcam access
2. **Capture Mood**: Click "Capture Mood" to analyze your current facial expression
3. **View Results**: See your detected emotion with confidence score
4. **Track History**: View your mood history and trends
5. **View Charts**: Click "View Chart" to see mood distribution visualization

## Technical Details

### Backend (Python Flask)
- **Flask**: Web framework for handling HTTP requests
- **OpenCV**: Computer vision library for image processing
- **FER (Facial Emotion Recognition)**: Deep learning model for emotion detection
- **NumPy**: Numerical computing for image data manipulation
- **Matplotlib**: Chart generation for mood visualization

### Frontend (HTML/CSS/JavaScript)
- **HTML5**: Semantic markup with video element for webcam access
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **Vanilla JavaScript**: Camera access, image capture, and API communication
- **Font Awesome**: Icons for better user experience

### Emotion Detection
The application uses the FER (Facial Emotion Recognition) library which is built on top of:
- **MTCNN**: Multi-task CNN for face detection
- **Deep learning models**: Pre-trained models for emotion classification

## API Endpoints

- `GET /`: Main application page
- `POST /analyze_mood`: Analyzes captured image for emotions
- `GET /mood_history`: Returns stored mood data
- `GET /mood_chart`: Returns mood distribution chart

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Privacy & Security

- All image processing happens locally on your device
- No images are stored permanently on the server
- Camera access requires explicit user permission
- Data is only stored in browser session (not persistent)

## Troubleshooting

### Camera Not Working
- Ensure you've granted camera permissions in your browser
- Check if another application is using the camera
- Try refreshing the page and granting permissions again

### Installation Issues
- Make sure you have Python 3.7+ installed
- Try using a virtual environment:
  ```bash
  python -m venv mood_tracker_env
  source mood_tracker_env/bin/activate  # On Windows: mood_tracker_env\Scripts\activate
  pip install -r requirements.txt
  ```

### Performance Issues
- Close other applications using the camera
- Ensure good lighting for better face detection
- Try reducing video quality in browser settings

## Future Enhancements

- [ ] Persistent mood data storage
- [ ] Mood trends and analytics
- [ ] Export mood data to CSV/JSON
- [ ] Multiple user profiles
- [ ] Mood reminders and notifications
- [ ] Integration with calendar apps
- [ ] Advanced emotion detection models

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the project repository.