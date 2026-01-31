import cv2
from datetime import datetime
import sqlite3
from face_auth import FaceAuth

# Database setup
DB_PATH = "attendance.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS attendance (
                name TEXT,
                time TEXT,
                action TEXT
            )""")
conn.commit()

def mark_attendance(name, state):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO attendance (name, time, action) VALUES (?, ?, ?)", (name, time_now, state))
    conn.commit()
    print(f"[DB] {name} marked {state} at {time_now}")
    print(f"[Attendance] {name} punched {state} at {time_now.split()[1]}")

# FaceAuth instance
face_auth = FaceAuth()
attendance_state = {}  # track IN/OUT per user

# Camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Press R = register | Q = quit")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_display = frame.copy()
    cv2.imshow("Camera", frame_display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    elif key == ord("r"):
        name = input("Enter name: ").strip()
        success, msg = face_auth.register_face(name, frame)
        print(f"[FaceAuth] {msg}")
        if success:
            attendance_state[name] = "OUT"  # start as OUT

    else:
        # Auto-recognition loop
        recognized = face_auth.recognize_face(frame)
        if recognized and face_auth.can_mark(recognized):
            state = attendance_state.get(recognized, "OUT")
            new_state = "IN" if state == "OUT" else "OUT"
            attendance_state[recognized] = new_state
            mark_attendance(recognized, new_state)

cap.release()
cv2.destroyAllWindows()
conn.close()
