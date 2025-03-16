import cv2  # Thư viện xử lý hình ảnh
import HandTracking as htm  # Module nhận diện bàn tay (đảm bảo có file HandTracking.py)
import pyautogui  # Điều khiển chuột trên máy tính
import numpy as np  # Thư viện hỗ trợ tính toán số học
from flask import Flask, render_template, Response

# Mở webcam để lấy hình ảnh đầu vào
cam = cv2.VideoCapture(0)

# Khởi tạo bộ nhận diện bàn tay, giới hạn chỉ nhận diện 1 bàn tay
detector = htm.handDetector(maxHands=1)

# Danh sách các điểm tương ứng với đầu ngón tay theo mô hình Mediapipe
# (theo thứ tự: ngón cái, trỏ, giữa, áp út, út)
fingers_number = [4, 8, 12, 16, 20]

# Tham số làm mịn để tránh chuột di chuyển giật
Smoothening = 5  
plocX, plocY = 0, 0  # Tọa độ chuột trước đó
clocX, clocY = 0, 0  # Tọa độ chuột hiện tại

# Kích thước khung hình webcam
wCam, hCam = 640, 480

# Kích thước màn hình máy tính
wScreen, hScreen = pyautogui.size()

# Biến kiểm soát trạng thái kéo/thả chuột
drag = False

while True:
    # Đọc hình ảnh từ webcam
    success, frame = cam.read()
    if not success:  # Nếu không lấy được hình ảnh thì bỏ qua vòng lặp
        continue

    # Lật ảnh theo chiều ngang để phản chiếu giống gương
    image = cv2.flip(frame, 1)

    # Nhận diện bàn tay trên ảnh
    image = detector.findHands(image)
    landmark_list = detector.findPosition(image)  # Lấy danh sách vị trí các điểm trên bàn tay

    # Kiểm tra xem có bàn tay trong khung hình không
    if len(landmark_list) != 0:
        # Lấy tọa độ đầu ngón trỏ
        x1, y1 = landmark_list[8][1:]

        # Kiểm tra trạng thái của các ngón tay (duỗi hay co)
        fingers = []  # Danh sách lưu trạng thái ngón tay (1 = duỗi, 0 = co)

        # Kiểm tra ngón cái (so sánh theo trục x)
        if landmark_list[fingers_number[0]][1] < landmark_list[fingers_number[0] - 1][1]:
            fingers.append(1)  # Ngón cái duỗi
        else:
            fingers.append(0)  # Ngón cái co

        # Kiểm tra 4 ngón còn lại (so sánh theo trục y)
        for id_finger in range(1, 5):
            if landmark_list[fingers_number[id_finger]][2] < landmark_list[fingers_number[id_finger] - 2][2]:
                fingers.append(1)  # Ngón tay duỗi
            else:
                fingers.append(0)  # Ngón tay co

        # Vẽ vùng giới hạn cho khu vực di chuyển trên màn hình webcam
        cv2.rectangle(image, (100, 50), (wCam - 100, hCam - 190), (0, 0, 0), 2)

        # Chuyển đổi tọa độ từ vùng webcam sang vùng màn hình máy tính
        x3 = np.interp(x1, (100, wCam - 100), (0, wScreen))
        y3 = np.interp(y1, (50, hCam - 190), (0, hScreen))

        # Làm mịn chuyển động chuột để tránh giật
        clocX = plocX + (x3 - plocX) / Smoothening
        clocY = plocY + (y3 - plocY) / Smoothening

        # Nếu đang kéo chuột mà buông tay ra thì thả chuột
        if drag and fingers.count(0) != 5:
            drag = False
            pyautogui.mouseUp(button="left")

        # Nếu chỉ ngón trỏ duỗi thì di chuyển chuột
        if fingers == [0, 1, 0, 0, 0]:
            pyautogui.moveTo(clocX, clocY)
            cv2.circle(image, (x1, y1), 10, (0, 255, 0), -1)
            plocX, plocY = clocX, clocY

        # Nếu ngón trỏ, ngón giữa, ngón cái duỗi và khoảng cách giữa trỏ & giữa < 27 thì click chuột trái
        elif fingers == [1, 1, 1, 0, 0]:
            length, img, lineInfo = detector.findDistance(8, 12, image)
            if length < 27:
                pyautogui.click()

        # Nếu ngón trỏ, ngón giữa, ngón út duỗi và khoảng cách giữa trỏ & giữa < 27 thì click chuột phải
        elif fingers == [0, 1, 1, 0, 1]:
            length, img, lineInfo = detector.findDistance(8, 12, image)
            if length < 27:
                pyautogui.click(button="right")

        # Nếu chỉ ngón trỏ và ngón giữa duỗi và khoảng cách giữa hai ngón < 27 thì double click
        elif fingers[1] == 1 and fingers[2] == 1 and fingers.count(0) == 3:
            length, img, lineInfo = detector.findDistance(8, 12, image)
            if length < 27:
                pyautogui.doubleClick()

        # Nếu chỉ có ngón cái và ngón trỏ duỗi thì cuộn chuột lên
        elif fingers == [1, 1, 0, 0, 0]:
            pyautogui.scroll(100)

        # Nếu chỉ có ngón trỏ và ngón út duỗi thì cuộn chuột xuống
        elif fingers == [0, 1, 0, 0, 1]:
            pyautogui.scroll(-100)

        # Nếu tất cả các ngón tay co lại thì thực hiện kéo thả chuột
        elif fingers.count(0) == 5:
            if not drag:
                drag = True
                pyautogui.mouseDown(button="left")  # Giữ chuột trái
            pyautogui.moveTo(clocX, clocY)  # Di chuyển chuột khi đang kéo
            plocX, plocY = clocX, clocY

    # Hiển thị hình ảnh từ webcam
    cv2.imshow("Virtual Mouse", image)

    # Đảm bảo cửa sổ hiển thị luôn ở trên cùng
    cv2.setWindowProperty("Virtual Mouse", cv2.WND_PROP_TOPMOST, 1)

    # Nếu nhấn "q" thì thoát chương trình
    if cv2.waitKey(1) == ord("q"):
        break

# Giải phóng webcam và đóng tất cả cửa sổ
cam.release()
cv2.destroyAllWindows()
