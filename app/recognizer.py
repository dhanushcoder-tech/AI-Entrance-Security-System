import sqlite3
import numpy as np
from scipy.spatial.distance import cosine

from app.embedding import FaceEmbedding


class FaceRecognizer:

    def __init__(self):

        self.embedder = FaceEmbedding()

        self.conn = sqlite3.connect(
            "data/database.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        # Matching threshold
        self.threshold = 0.45


    def recognize(self, frame):

        try:

            # Detect faces
            faces = self.embedder.app.get(frame)

            if len(faces) == 0:
                return None, None


            # Taking first face
            face = faces[0]


            # Bounding box
            bbox = face.bbox.astype(int).tolist()


            # Live face embedding
            live_embedding = np.array(
                face.embedding,
                dtype=np.float32
            )


            # Normalize
            live_embedding = live_embedding / np.linalg.norm(
                live_embedding
            )


            # Get registered students

            self.cursor.execute("""
                SELECT 
                    student_id,
                    name,
                    department,
                    year,
                    section,
                    embedding
                FROM students
            """)


            students = self.cursor.fetchall()


            if len(students) == 0:
                return None, bbox



            best_student = None
            best_distance = 999



            for student in students:


                stored_blob = student[5]


                if stored_blob is None:
                    continue



                stored_embedding = np.frombuffer(
                    stored_blob,
                    dtype=np.float32
                )


                # Normalize stored embedding
                stored_embedding = (
                    stored_embedding /
                    np.linalg.norm(stored_embedding)
                )


                distance = cosine(
                    live_embedding,
                    stored_embedding
                )



                if distance < best_distance:

                    best_distance = distance
                    best_student = student



            print(
                "Match distance:",
                best_distance
            )


            # Match found

            if best_distance < self.threshold:

                return best_student, bbox



            # Unknown

            return None, bbox



        except Exception as e:

            print(
                "Recognition Error:",
                e
            )

            return None, None



    def close(self):

        self.conn.close()