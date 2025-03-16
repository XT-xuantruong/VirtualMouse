import cv2  # Thư viện OpenCV dùng để xử lý ảnh
import mediapipe as mp  # Thư viện MediaPipe dùng để nhận diện bàn tay
import math  # Thư viện toán học dùng để tính khoảng cách

class HandDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, trackCon=0.7):
        """
        Khởi tạo bộ nhận diện bàn tay với các tham số:
        - mode: Chế độ nhận diện (False là nhận diện động)
        - maxHands: Số lượng bàn tay tối đa có thể nhận diện
        - modelComplexity: Độ phức tạp của mô hình (1 là vừa phải)
        - detectionCon: Ngưỡng tin cậy để phát hiện bàn tay
        - trackCon: Ngưỡng tin cậy để theo dõi bàn tay đã nhận diện
        """
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Khởi tạo mô hình nhận diện bàn tay của MediaPipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 
                                        self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils  # Công cụ vẽ kết quả nhận diện bàn tay

    def findHands(self, img, draw=False):
        """
        Phát hiện bàn tay trong ảnh.
        - Chuyển đổi ảnh sang định dạng RGB (MediaPipe chỉ nhận RGB).
        - Xử lý ảnh để phát hiện bàn tay.
        - Nếu 'draw' = True, vẽ khung bàn tay lên ảnh.

        Trả về ảnh sau khi xử lý.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Chuyển ảnh BGR -> RGB
        self.results = self.hands.process(imgRGB)  # Phát hiện bàn tay

        # Nếu phát hiện bàn tay, vẽ lên ảnh (nếu draw=True)
        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw=False):
        """
        Lấy danh sách các tọa độ của 21 điểm mốc (landmarks) trên bàn tay.
        - handNo: Chọn bàn tay thứ mấy để lấy dữ liệu (0 là bàn tay đầu tiên).
        - Nếu 'draw' = True, vẽ các điểm trên bàn tay.

        Trả về danh sách tọa độ của các điểm trên bàn tay.
        """
        self.lmList = []  # Danh sách lưu tọa độ của các điểm trên bàn tay

        # Nếu phát hiện bàn tay
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]  # Chọn bàn tay thứ 'handNo'

            # Duyệt qua từng điểm trên bàn tay
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape  # Lấy kích thước ảnh
                cx, cy = int(lm.x * w), int(lm.y * h)  # Chuyển đổi tọa độ từ tỷ lệ -> pixel
                self.lmList.append([id, cx, cy])  # Lưu lại tọa độ điểm

                # Nếu 'draw' = True, vẽ các điểm lên ảnh
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return self.lmList  # Trả về danh sách tọa độ các điểm trên bàn tay

    def findDistance(self, p1, p2, img, draw=True, r=10, t=2):
        """
        Tính khoảng cách giữa hai điểm trên bàn tay.
        - p1, p2: Chỉ mục của hai điểm cần đo khoảng cách.
        - Nếu 'draw' = True, vẽ đường nối giữa hai điểm.
        - r: Bán kính của vòng tròn vẽ trên các điểm.
        - t: Độ dày của đường nối.

        Trả về:
        - length: Khoảng cách giữa hai điểm.
        - img: Ảnh đã vẽ (nếu draw=True).
        - info: Danh sách chứa tọa độ của hai điểm và điểm trung tâm.
        """
        # Nếu không có danh sách điểm trên bàn tay, trả về khoảng cách = 0
        if not self.lmList:
            return 0, img, [0, 0, 0, 0, 0, 0]

        # Lấy tọa độ của hai điểm cần đo
        x1, y1 = self.lmList[p1][1:]  # Tọa độ điểm p1
        x2, y2 = self.lmList[p2][1:]  # Tọa độ điểm p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Tọa độ trung tâm giữa hai điểm

        # Nếu 'draw' = True, vẽ đường nối giữa hai điểm
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)  # Vẽ đường nối
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)  # Vẽ điểm p1
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)  # Vẽ điểm p2
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)  # Vẽ điểm trung tâm

        # Tính khoảng cách giữa hai điểm (công thức Euclidean)
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return length, img, [x1, y1, x2, y2, cx, cy]
