import insightface
import numpy as np


class FaceEmbedding:

    def __init__(self):

        self.app = insightface.app.FaceAnalysis(
            providers=["CPUExecutionProvider"]
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )


    def get_embedding(self, image):

        faces = self.app.get(image)

        if len(faces) == 0:
            return None


        embedding = np.array(
            faces[0].embedding,
            dtype=np.float32
        )


        # Normalize embedding
        embedding = embedding / np.linalg.norm(
            embedding
        )


        return embedding