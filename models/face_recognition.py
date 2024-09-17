import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from insightface.app import FaceAnalysis

class FaceRecognitionModel:
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        self.registered_faces = {}

        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

        self.app = FaceAnalysis(providers=['CPUExecutionProvider']) 
        self.app.prepare(ctx_id=0, det_size=(640, 640))  

    def save_image(self, image_file, user_name):
        filename = secure_filename(f"{user_name}_{image_file.filename}")
        image_path = os.path.join(self.upload_folder, filename)
        image_file.save(image_path)
        return image_path

    def encode_face(self, image_path):
        image = cv2.imread(image_path)
        faces = self.app.get(image)
        if len(faces) == 0:
            return []
        face_encodings = [face.embedding for face in faces]
        return face_encodings

    def register_face(self, image_file, user_name):
        try:
            image_path = self.save_image(image_file, user_name)
            face_encodings = self.encode_face(image_path)

            if len(face_encodings) > 0:
                self.registered_faces[user_name] = {
                    'encoding': face_encodings[0],
                    'image_path': image_path
                }
                return {"status": "success", "message": f"Face registered successfully for {user_name}"}, 200
            else:
                return {"status": "error", "message": "No face detected"}, 400
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500

    def verify_face(self, image_file):
        try:
            image_path = self.save_image(image_file, "verification")
            face_encodings = self.encode_face(image_path)

            if len(face_encodings) > 0:
                for user_name, data in self.registered_faces.items():
                    registered_face = data['encoding']
                    similarity = np.dot(registered_face, face_encodings[0]) / (np.linalg.norm(registered_face) * np.linalg.norm(face_encodings[0]))
                    if similarity > 0.95: 
                        return {"status": "success", "message": f"Face verified successfully for {user_name}"}, 200
            return {"status": "error", "message": "Face verification failed"}, 400
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500