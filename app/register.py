import cv2
import time

from app.embedding import FaceEmbedding
from app.database import Database


class RegisterStudent:

    def __init__(self):

        self.embedder = FaceEmbedding()
        self.db = Database()



    def register(self):

        print("\n===== STUDENT REGISTRATION =====")


        name = input("Enter Name: ")
        student_id = input("Enter Student ID: ")
        department = input("Enter Department: ")
        year = input("Enter Year: ")
        section = input("Enter Section: ")



        print("\nStarting camera...")
        print("Look at the camera")
        print("Auto capturing face...")


        camera = cv2.VideoCapture(0)


        saved = False


        while True:


            ret, frame = camera.read()


            if not ret:
                break



            cv2.putText(
                frame,
                "LOOK AT CAMERA - AUTO REGISTER",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )


            cv2.imshow(
                "Automatic Registration",
                frame
            )



            # Try detecting face continuously

            embedding = self.embedder.get_embedding(frame)



            if embedding is not None and not saved:


                print("Face detected...")
                print("Saving student...")


                self.db.add_student(

                    student_id,
                    name,
                    department,
                    year,
                    section,
                    embedding.tobytes()

                )


                saved = True


                print("\n✅ STUDENT REGISTERED SUCCESSFULLY")


                time.sleep(2)

                break




            if cv2.waitKey(1) & 0xff == ord('q'):

                print("Cancelled")
                break



        camera.release()

        cv2.destroyAllWindows()



if __name__ == "__main__":

    RegisterStudent().register()