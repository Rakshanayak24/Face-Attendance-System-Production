
# camera.py
import cv2
from src.face_auth import FaceAuth
from src.storage import AttendanceDB

def run_camera():
    cam = cv2.VideoCapture(0)
    auth = FaceAuth()
    db = AttendanceDB()

    print("Press R = register | Q = quit")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Identify face
        name = auth.identify(frame)

        if name:
            db.mark(name)

        # Show camera
        cv2.imshow("Face Attendance", frame)
        key = cv2.waitKey(1) & 0xFF

        # Register new face
        if key == ord("r"):
            username = input("Enter name: ")
            if auth.is_registered(username):
                print(f"{username} already registered, choose a different name.")
            else:
                auth.register(frame, username)
                print(f"{username} registered successfully!")

        # Quit
        elif key == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_camera()
