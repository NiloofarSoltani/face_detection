import cv2
import face_recognition


class FaceRecognition:
    def __init__(self, cascade_file_path):
        self.cascade_classifier = cv2.CascadeClassifier(cascade_file_path)

    def recognize_faces(self, frame, users):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            face_image = frame[y:y+h, x:x+w]
            face_encoding = face_recognition.face_encodings(face_image)
            name = "Unknown"
            if len(face_encoding) == 1:
                face_encoding = face_encoding[0]
                matches = face_recognition.compare_faces(list(users.values()), face_encoding)
                distances = face_recognition.face_distance(list(users.values()), face_encoding)
                min_distance = min(distances)
                if min_distance < 0.6:
                    index = distances.tolist().index(min_distance)
                    name = list(users.keys())[index]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        return frame
