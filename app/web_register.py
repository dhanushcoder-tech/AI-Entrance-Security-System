import streamlit as st
import cv2
import numpy as np

from app.embedding import FaceEmbedding
from app.database import Database


# ==========================
# INITIALIZE
# ==========================

@st.cache_resource
def load_models():

    embedder = FaceEmbedding()
    db = Database()

    return embedder, db


embedder, db = load_models()



# ==========================
# REGISTER FUNCTION
# ==========================

def register_student():

    st.header("🧑‍🎓 Register New Student")


    student_id = st.text_input(
        "Student ID"
    )

    name = st.text_input(
        "Name"
    )

    department = st.text_input(
        "Department"
    )

    year = st.text_input(
        "Year"
    )

    section = st.text_input(
        "Section"
    )


    st.subheader(
        "📷 Capture Face"
    )


    camera_image = st.camera_input(
        "Take Photo"
    )



    if camera_image is not None:


        bytes_data = camera_image.getvalue()


        img_array = np.frombuffer(
            bytes_data,
            np.uint8
        )


        frame = cv2.imdecode(
            img_array,
            cv2.IMREAD_COLOR
        )


        st.image(
            frame,
            channels="BGR",
            caption="Captured Face"
        )



        if st.button(
            "Register Student"
        ):


            if not student_id or not name:

                st.error(
                    "Please enter Student ID and Name"
                )

                return



            faces = embedder.app.get(frame)



            if len(faces) == 0:

                st.error(
                    "❌ No face detected"
                )

                return



            face = faces[0]


            embedding = np.array(
                face.embedding,
                dtype=np.float32
            )



            try:

                db.add_student(
                    student_id,
                    name,
                    department,
                    year,
                    section,
                    embedding.tobytes()
                )


                st.success(
                    f"✅ {name} Registered Successfully"
                )


            except Exception as e:

                st.error(
                    f"Registration Failed: {e}"
                )