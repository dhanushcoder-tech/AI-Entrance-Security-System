import cv2


class FaceDetector:

    def __init__(self):

        self.face_cascade = cv2.CascadeClassifier(
            "models/haarcascade_frontalface_default.xml"
        )

        if self.face_cascade.empty():
            print("❌ Failed to load Haar Cascade model!")
        else:
            print("✅ Haar Cascade model loaded successfully!")

    def detect(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50)
        )

        return faces