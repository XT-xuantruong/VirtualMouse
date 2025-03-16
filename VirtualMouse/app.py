import cv2
import HandTracking as htm
import pyautogui
import numpy as np
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

# Khởi tạo webcam và bộ nhận diện tay
cam = cv2.VideoCapture(0)
detector = htm.handDetector(maxHands=1)
fingers_number = [4, 8, 12, 16, 20]

# Tham số làm mịn chuyển động chuột
Smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0
wCam, hCam = 640, 480
wScreen, hScreen = pyautogui.size()
drag = False

# Biến trạng thái Virtual Mouse
virtual_mouse_enabled = True

def generate_frames():
    """Tạo luồng video từ webcam và xử lý nhận diện tay"""
    global plocX, plocY, clocX, clocY, drag, virtual_mouse_enabled
    while True:
        success, frame = cam.read()
        if not success:
            break

        # Lật ảnh ngang
        image = cv2.flip(frame, 1)
        image = detector.findHands(image)
        landmark_list = detector.findPosition(image)

        if len(landmark_list) != 0:
            x1, y1 = landmark_list[8][1:]  # Tọa độ đầu ngón trỏ

            # Kiểm tra trạng thái ngón tay
            fingers = []
            if landmark_list[fingers_number[0]][1] < landmark_list[fingers_number[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id_finger in range(1, 5):
                if landmark_list[fingers_number[id_finger]][2] < landmark_list[fingers_number[id_finger] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Vẽ vùng giới hạn
            cv2.rectangle(image, (100, 50), (wCam - 100, hCam - 190), (0, 0, 0), 2)

            # Hiển thị trạng thái Virtual Mouse trên video
            status_text = "Virtual Mouse: ON" if virtual_mouse_enabled else "Virtual Mouse: OFF"
            cv2.putText(image, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                       (0, 255, 0) if virtual_mouse_enabled else (0, 0, 255), 2)

            # Điều khiển chuột chỉ khi Virtual Mouse được bật
            if virtual_mouse_enabled:
                x3 = np.interp(x1, (100, wCam - 100), (0, wScreen))
                y3 = np.interp(y1, (50, hCam - 190), (0, hScreen))
                clocX = plocX + (x3 - plocX) / Smoothening
                clocY = plocY + (y3 - plocY) / Smoothening

                if drag and fingers.count(0) != 5:
                    drag = False
                    pyautogui.mouseUp(button="left")
                elif fingers == [0, 1, 0, 0, 0]:  # Di chuyển chuột
                    pyautogui.moveTo(clocX, clocY)
                    cv2.circle(image, (x1, y1), 10, (0, 255, 0), -1)
                    plocX, plocY = clocX, clocY
                elif fingers == [1, 1, 1, 0, 0]:  # Click trái
                    length, _, _ = detector.findDistance(8, 12, image)
                    if length < 27:
                        pyautogui.click()
                elif fingers == [0, 1, 1, 0, 1]:  # Click phải
                    length, _, _ = detector.findDistance(8, 12, image)
                    if length < 27:
                        pyautogui.click(button="right")
                elif fingers[1] == 1 and fingers[2] == 1 and fingers.count(0) == 3:  # Double click
                    length, _, _ = detector.findDistance(8, 12, image)
                    if length < 27:
                        pyautogui.doubleClick()
                elif fingers == [1, 1, 0, 0, 0]:  # Cuộn lên
                    pyautogui.scroll(100)
                elif fingers == [0, 1, 0, 0, 1]:  # Cuộn xuống
                    pyautogui.scroll(-100)
                elif fingers.count(0) == 5:  # Kéo thả
                    if not drag:
                        drag = True
                        pyautogui.mouseDown(button="left")
                    pyautogui.moveTo(clocX, clocY)
                    plocX, plocY = clocX, clocY

        # Chuyển ảnh sang định dạng JPEG
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Hiển thị trang chính"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream video tới frontend"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_virtual_mouse', methods=['POST'])
def toggle_virtual_mouse():
    """API để bật/tắt Virtual Mouse"""
    global virtual_mouse_enabled
    virtual_mouse_enabled = not virtual_mouse_enabled
    return jsonify({'status': 'success', 'enabled': virtual_mouse_enabled})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)