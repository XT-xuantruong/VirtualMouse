# Virtual Mouse Project (FastAPI + React)

This project uses FastAPI for the backend to process webcam video and control the mouse via hand gestures, and React for the frontend to display the video stream interactively.

## Prerequisites
- Python 3.8+
- Node.js 16+ and npm
- Webcam

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd VirtualMouseProject
```
### 2. Set Up Backend (Flask)
1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Create a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate  
    # On Windows: venv\Scripts\activate
    ```

3. Install dependencies
    ```
    pip install fastapi uvicorn opencv-python mediapipe pyautogui numpy

    or

    pip install -r requirements.txt
    ```

4. Ensure `HandTracking.py` is in the same directory as `app.py`

### 3. Set Up Frontend
1. Navigate to the frontend directory:
   ```
    cd frontend
   ```
2. Install dependencies
   ```
    npm install
    npm install axios
   ```

### 4. Run the Application
1. Start the Flask server:
```bash
python app.py
```
2. Open your browser and go to:
```bash
http://localhost:8000
```
3. Ensure the React app is configured to communicate with http://localhost:8000
4. Run the Application
   1. Start the backend (FastAPI):
        ```
        cd backend
        python main.py
        ```
   2. Start the frontend (React) in a separate terminal:
        ```
        cd frontend
        npm start
        ```
    3. Open your browser and go to: http://localhost:5173

### Features
- Real-time video streaming with hand detection.
- Mouse control via gestures (move, click, scroll, drag).
- Toggle virtual mouse ON/OFF via a button.
### Troubleshooting
- Ensure the backend runs before the frontend.
- Check CORS settings in main.py if frontend cannot connect to backend.

### Project Structure
```
VirtualMouseProject/
├── backend/
│   ├── main.py          # FastAPI entry point
│   └── HandTracking.py  # Hand detection logic
├── frontend/
│   ├── src/
│   │   ├── App.js       # React main component
│   │   └── App.css      # Styles
│   └── package.json     # Frontend dependencies
```