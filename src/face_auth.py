import cv2
import pickle
import os
from datetime import datetime
import mediapipe as mp
import numpy as np

ENCODINGS_PATH = "encodings.pkl"

class FaceAuth:
    def __init__(self):
        self.encodings = {}
        self.load_encodings()
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False)
        self.cooldown_time = 5  # seconds to wait before marking same user again
        self.last_seen = {}  # { name: last_punch_time }

    def load_encodings(self):
        if os.path.exists(ENCODINGS_PATH):
            with open(ENCODINGS_PATH, "rb") as f:
                self.encodings = pickle.load(f)
        else:
            self.encodings = {}

    def save_encodings(self):
        with open(ENCODINGS_PATH, "wb") as f:
            pickle.dump(self.encodings, f)

    def register_face(self, name, frame):
        if name in self.encodings:
            return False, f"{name} already registered, choose a different name."
        encoding = self.compute_face_encoding(frame)
        if encoding is not None:
            self.encodings[name] = encoding
            self.save_encodings()
            return True, f"{name} registered successfully!"
        else:
            return False, "Face not detected, try again."

    def compute_face_encoding(self, frame):
        # Simple placeholder: resize & flatten face region
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_face_mesh.process(img)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            encoding = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
            return encoding
        return None

    def recognize_face(self, frame, threshold=0.6):
        encoding = self.compute_face_encoding(frame)
        if encoding is None:
            return None
        for name, stored_enc in self.encodings.items():
            dist = np.linalg.norm(encoding - stored_enc)
            if dist < threshold:
                return name
        return None

    def can_mark(self, name):
        # Check cooldown
        last = self.last_seen.get(name)
        now = datetime.now().timestamp()
        if last and (now - last) < self.cooldown_time:
            return False
        self.last_seen[name] = now
        return True


