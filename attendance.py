import cv2
import face_recognition
import numpy as np
import sqlite3
from datetime import datetime

# Example known encodings and names (load from file/db in real project)
known_face_encodings = []   # load saved encodings
known_face_names = []       # load saved names

# Connect to SQLite database
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Create table if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    name TEXT,
    date TEXT,
    time TEXT
)
''')
conn.commit()

def mark_attendance(name):
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")

    c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
              (name, date_string, time_string))
    conn.commit()

def recognize_faces():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            mark_attendance(name)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

recognize_faces()
