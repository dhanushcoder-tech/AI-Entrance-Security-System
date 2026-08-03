import cv2
from datetime import datetime

from app.unknown import UnknownPerson
from app.recognizer import FaceRecognizer
from app.database import Database
from app.logger import can_log


class Camera:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise Exception("Camera not detected")


        self.unknown = UnknownPerson()
        self.recognizer = FaceRecognizer()
        self.db = Database()

        self.last_unknown_save = None



    def start(self):

        print("AI Entrance Camera Started")


        while True:


            success, frame = self.cap.read()


            if not success:

                print("Camera frame error")
                break



            student, bbox = self.recognizer.recognize(frame)



            now = datetime.now()

            current_date = now.strftime("%d-%m-%Y")
            current_time = now.strftime("%H:%M:%S")



            # HEADER

            cv2.rectangle(
                frame,
                (0,0),
                (640,45),
                (40,40,40),
                -1
            )


            cv2.putText(
                frame,
                "AI ENTRANCE SECURITY SYSTEM",
                (120,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )



            # =========================
            # KNOWN PERSON
            # =========================


            if student is not None:


                student_id = student[0]
                name = student[1]
                department = student[2]



                if can_log(student_id):


                    self.db.mark_attendance(
                        student_id,
                        name,
                        current_date,
                        current_time,
                        "Granted"
                    )


                    print(
                        "Attendance:",
                        name
                    )




                # Face rectangle

                if bbox is not None:


                    x1, y1, x2, y2 = map(
                        int,
                        bbox
                    )


                    cv2.rectangle(
                        frame,
                        (x1,y1),
                        (x2,y2),
                        (0,255,0),
                        3
                    )




                cv2.putText(
                    frame,
                    f"{name} | {department}",
                    (20,90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2
                )



                cv2.putText(
                    frame,
                    "ACCESS GRANTED",
                    (20,130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    3
                )



            # =========================
            # UNKNOWN PERSON
            # =========================


            else:


                if bbox is not None:


                    x1, y1, x2, y2 = map(
                        int,
                        bbox
                    )


                    cv2.rectangle(
                        frame,
                        (x1,y1),
                        (x2,y2),
                        (0,0,255),
                        3
                    )



                    # Save unknown once per second

                    if self.last_unknown_save != current_time:


                        self.unknown.save(frame)

                        self.last_unknown_save = current_time





                cv2.putText(
                    frame,
                    "UNKNOWN PERSON",
                    (20,90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0,0,255),
                    2
                )



                cv2.putText(
                    frame,
                    "ACCESS DENIED",
                    (20,130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3
                )





            # FOOTER


            cv2.putText(
                frame,
                f"{current_date}  {current_time}",
                (10,465),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2
            )



            cv2.imshow(
                "AI Entrance Security System",
                frame
            )



            if cv2.waitKey(1) & 0xFF == ord("q"):

                break





        self.cap.release()

        cv2.destroyAllWindows()