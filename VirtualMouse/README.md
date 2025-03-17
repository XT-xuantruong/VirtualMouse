# Virtual Mouse Project (Flask)

This project implements a virtual mouse controlled by hand gestures using OpenCV, MediaPipe, and Flask. The backend processes webcam video, detects hand landmarks, and controls the mouse, while the frontend displays the video stream.

## Prerequisites
- Python 3.8+
- Webcam
- Node.js and npm (for development tools, optional)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [<repository-url>](https://github.com/XT-xuantruong/VirtualMouse.git)
cd VirtualMouseProject
```
### 2. Set Up Backend (Flask)
1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
```

2. Install dependencies
```
pip install flask opencv-python mediapipe pyautogui numpy
or
pip install -r requirements.txt
```

3. Ensure `HandTracking.py` is in the same directory as `app.py`

### 3. Set Up Frontend
The frontend uses static HTML/CSS served by Flask. Ensure the following structure:

```
VirtualMouseProject/
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── app.py
└── HandTracking.py
```

### 4. Run the Application
1. Start the Flask server:
```bash
python app.py
```
2. Open your browser and go to:
```bash
http://localhost:5000
```

### Features
- Video stream from webcam with hand detection.
- Mouse control via hand gestures (move, click, scroll, drag).
- Toggle virtual mouse ON/OFF via a button.
### Troubleshooting
- Ensure your webcam is connected and accessible.
- If CORS issues arise, adjust the Flask app configuration.

### Project Structure
```
VirtualMouseProject/
├── static/         # Static files (CSS)
├── templates/      # HTML templates
├── app.py          # Flask backend
└── HandTracking.py # Hand detection logic
```
