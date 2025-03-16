import cv2
import numpy as np
import pyautogui
from models.hand_tracking import HandDetector

class MouseService:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=1)
        self.fingers_number = [4, 8, 12, 16, 20]
        self.Smoothening = 5
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        self.wCam, self.hCam = 640, 480
        self.wScreen, self.hScreen = pyautogui.size()
        self.drag = False
        self.virtual_mouse_enabled = True

    async def generate_frames(self):
        while True:
            success, frame = self.cam.read()
            if not success:
                break

            image = cv2.flip(frame, 1)
            image = self.detector.findHands(image)
            landmark_list = self.detector.findPosition(image)

            if len(landmark_list) != 0:
                x1, y1 = landmark_list[8][1:]
                fingers = []
                if landmark_list[self.fingers_number[0]][1] < landmark_list[self.fingers_number[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id_finger in range(1, 5):
                    if landmark_list[self.fingers_number[id_finger]][2] < landmark_list[self.fingers_number[id_finger] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                cv2.rectangle(image, (100, 50), (self.wCam - 100, self.hCam - 190), (0, 0, 0), 2)
                status_text = "Virtual Mouse: ON" if self.virtual_mouse_enabled else "Virtual Mouse: OFF"
                cv2.putText(image, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0) if self.virtual_mouse_enabled else (0, 0, 255), 2)

                if self.virtual_mouse_enabled:
                    x3 = np.interp(x1, (100, self.wCam - 100), (0, self.wScreen))
                    y3 = np.interp(y1, (50, self.hCam - 190), (0, self.hScreen))
                    self.clocX = self.plocX + (x3 - self.plocX) / self.Smoothening
                    self.clocY = self.plocY + (y3 - self.plocY) / self.Smoothening

                    if self.drag and fingers.count(0) != 5:
                        self.drag = False
                        pyautogui.mouseUp(button="left")
                    elif fingers == [0, 1, 0, 0, 0]:
                        pyautogui.moveTo(self.clocX, self.clocY)
                        cv2.circle(image, (x1, y1), 10, (0, 255, 0), -1)
                        self.plocX, self.plocY = self.clocX, self.clocY
                    elif fingers == [1, 1, 1, 0, 0]:
                        length, _, _ = self.detector.findDistance(8, 12, image)
                        if length < 27:
                            pyautogui.click()
                    elif fingers == [0, 1, 1, 0, 1]:
                        length, _, _ = self.detector.findDistance(8, 12, image)
                        if length < 27:
                            pyautogui.click(button="right")
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers.count(0) == 3:
                        length, _, _ = self.detector.findDistance(8, 12, image)
                        if length < 27:
                            pyautogui.doubleClick()
                    elif fingers == [1, 1, 0, 0, 0]:
                        pyautogui.scroll(100)
                    elif fingers == [0, 1, 0, 0, 1]:
                        pyautogui.scroll(-100)
                    elif fingers.count(0) == 5:
                        if not self.drag:
                            self.drag = True
                            pyautogui.mouseDown(button="left")
                        pyautogui.moveTo(self.clocX, self.clocY)
                        self.plocX, self.plocY = self.clocX, self.clocY

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def toggle_virtual_mouse(self):
        self.virtual_mouse_enabled = not self.virtual_mouse_enabled
        return self.virtual_mouse_enabled

mouse_service = MouseService()