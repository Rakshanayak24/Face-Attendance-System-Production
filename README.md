# Face Authentication Attendance System (Windows Safe)

Python 3.11 compatible | No dlib | No CMake

---

## Features
- Real camera input via webcam
- Face registration
  - If the same face is detected again, the system asks to enter a name again for uniqueness
- Face recognition (MediaPipe embeddings)
- Punch-in / Punch-out tracking
- SQLite storage for attendance logs
- Basic liveness check (motion consistency)
- Handles normal indoor lighting conditions

---

## Installation

1. Clone the repository.
2. Create a virtual environment (recommended):

- Create a Python 3.11 virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

# Install dependencies
```bash
cd src
pip install --upgrade pip
pip install -r requirements.txt
```

# Run the application
```bash
python app.py
```
## Controls
- r → Register a new face
- q → Quit the application
- Face Registration
- When you press r, the system will:
- Capture your face from the camera.
- Prompt you to enter a unique name.
- If the face is already registered, it will still ask for a name to keep multiple entries separate.

## Attendance
- When a registered face is recognized:
- If the user has not punched in today, it records Punch-in.
- If the user has already punched in, the next recognition records Punch-out.
- Attendance is stored in SQLite database (attendance.db).

## Model & Approach
- Uses MediaPipe Face Mesh to extract facial landmarks.
- Computes embeddings for each registered face.
- Matches incoming camera frames with stored embeddings using nearest neighbor (Euclidean distance).
- Lightweight approach: No deep model training required, works in real-time.
- Basic liveness check: requires slight motion in consecutive frames to prevent static photo spoofing.

## Training Process
- No offline training required.
- Faces are registered online by the user.
- Embeddings are stored in the SQLite database for comparison.
- Accuracy Expectations
- Works reliably in normal indoor lighting.
- Recognizes registered faces even with small head rotations.
- Punch-in / Punch-out logs are accurate for normal usage.

# May fail under:
- Low or very bright lighting
- Extreme side poses or occluded faces
- Multiple similar-looking faces
- Sudden rapid movements

## Known Limitations
- System startup can be slow on first launch due to MediaPipe initialization (~30–60 seconds).
- protobuf warnings may appear during runtime — they do not affect functionality.
- Attendance marking depends on face being visible and facing the camera.
- Spoof prevention is basic; advanced attacks (videos, 3D masks) may bypass it.

## Database
- SQLite database attendance.db stores:
- name (user name)
- punch_in_time
- punch_out_time
- date
- Each face registration stores unique embeddings linked to a username.

## Folder Structure
```bash
├── requirements.txt
├── README.md
├── src/
│   ├── face_auth.py    # Face registration & recognition
│   └── storage.py      # SQLite database logic
|   |__ app.py          # Main script to run 
|   |__ camera.py       # Camera & attendance logic
```
## Example Flow
Start camera:
- python app.py

- Press R to register face → enter name.
- Look at the camera → system recognizes you and logs attendance.
- If recognized again, logs Punch-out.

## Notes
- Recommended: normal lighting, stable camera position.
- You can register multiple users.
- Database updates automatically on recognition.
- For a fresh start, delete attendance.db and run again.
