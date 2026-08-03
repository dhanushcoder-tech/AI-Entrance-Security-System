import cv2
import os
from datetime import datetime


class UnknownPerson:

    def __init__(self):

        self.last_saved = None

        os.makedirs("data/unknown", exist_ok=True)

    def save(self, frame):

        now = datetime.now()

        # Prevent duplicate images within 15 seconds
        if self.last_saved is not None:

            seconds = (now - self.last_saved).total_seconds()

            if seconds < 15:
                return

        filename = now.strftime("unknown_%Y%m%d_%H%M%S.jpg")

        path = os.path.join(
            "data",
            "unknown",
            filename
        )

        success = cv2.imwrite(path, frame)

        if success:

            self.last_saved = now

            print(f"📸 Unknown Person Saved : {filename}")

        else:

            print("❌ Failed to save unknown person.")