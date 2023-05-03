import tkinter as tk

import cv2
from PIL import Image, ImageTk

from face_recgnition_class import FaceRecognition
from admin import Admin
import face_recognition

class FaceRecognitionUI:
    def __init__(self, cascade_file_path):
        self.admin = Admin()
        self.recognizer = FaceRecognition(cascade_file_path)
        self.window = tk.Tk()
        self.window.title("Face Recognition")
        self.window.geometry("800x600")

        self.canvas = tk.Canvas(self.window, width=800, height=600)
        self.canvas.pack()

        self.update_image()

        self.window.mainloop()

    def update_image(self):
        _, frame = cv2.VideoCapture(0).read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.recognizer.recognize_faces(frame, self.admin.users)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo
        self.window.after(10, self.update_image)
