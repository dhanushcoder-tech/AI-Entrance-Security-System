import streamlit as st
import cv2
import numpy as np

from app.recognizer import FaceRecognizer


# =========================
# LOAD RECOGNIZER
# =========================

@st.cache_resource
def load_recognizer():

    return FaceRecognizer()



# =========================
# VERIFY FACE FUNCTION
# =========================

def verify_face():

    st.header("🔍 Face Verification")


    recognizer = load_recognizer()


    image = st.camera_input(
        "Capture your face"
    )


    if image is None:
        return



    # Convert image

    bytes_data = image.getvalue()


    img_array = np.frombuffer(
        bytes_data,
        np.uint8
    )


    frame = cv2.imdecode(
        img_array,
        cv2.IMREAD_COLOR
    )


    if frame is None:

        st.error(
            "❌ Image processing failed"
        )

        return



    # Show captured image

    st.image(
        frame,
        channels="BGR",
        caption="Captured Face"
    )



    # Recognize

    student, bbox = recognizer.recognize(
        frame
    )



    # =========================
    # FACE BOX
    # =========================

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



    # =========================
    # VERIFIED
    # =========================

    if student is not None:


        student_id = student[0]
        name = student[1]
        department = student[2]
        year = student[3]
        section = student[4]


        st.success(
            "✅ Identity Verified - Access Granted"
        )


        st.write(
            f"👤 Name : {name}"
        )

        st.write(
            f"🆔 ID : {student_id}"
        )

        st.write(
            f"🏢 Department : {department}"
        )

        st.write(
            f"📚 Year : {year}"
        )

        st.write(
            f"📌 Section : {section}"
        )



    # =========================
    # UNKNOWN
    # =========================

    else:


        st.error(
            "❌ Unknown Person - Access Denied"
        )