import cv2
import face_recognition
import pickle
import datetime
import sqlite3

# Load the trained model
model_path = "trained_model.pkl"
with open(model_path, "rb") as f:
    data = pickle.load(f)

def log_attendance(name):
    conn = sqlite3.connect(os.path.join("..", "web_app", "attendance.db"))
    cursor = conn.cursor()
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO attendance (user, time) VALUES (?, ?)", (name, time_str))
    conn.commit()
    conn.close()
    print(f"Logged attendance for {name} at {time_str}")

def recognize_face():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, boxes)
        for encoding, box in zip(encodings, boxes):
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    counts[data["names"][i]] = counts.get(data["names"][i], 0) + 1
                name = max(counts, key=counts.get)
                log_attendance(name)
            top, right, bottom, left = box
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
        cv2.imshow("Face Recognition - Press 'q' to Quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_face()
