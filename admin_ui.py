import os
import tkinter as tk
from tkinter import messagebox
import face_recognition
import PIL
import cv2
from PIL import ImageTk


class AdminUI:
    def __init__(self, admin):
        self.admin = admin
        self.window = tk.Tk()
        self.window.title("Admin")
        self.window.geometry("400x400")

        self.label_username = tk.Label(self.window, text="Username")
        self.label_username.pack()
        self.entry_username = tk.Entry(self.window)
        self.entry_username.pack()

        self.button_capture = tk.Button(self.window, text="Capture", command=self.capture)
        self.button_capture.pack()

        self.button_add = tk.Button(self.window, text="Add User", command=self.add_user, state=tk.DISABLED)
        self.button_add.pack()

        self.label_users = tk.Label(self.window, text="Users")
        self.label_users.pack()
        self.listbox_users = tk.Listbox(self.window)
        for user in self.admin.users:
            self.listbox_users.insert(tk.END, user)
        self.listbox_users.pack()

        self.button_remove = tk.Button(self.window, text="Remove User", command=self.remove_user)
        self.button_remove.pack()

        self.window.mainloop()

    def capture(self):
        self.camera = cv2.VideoCapture(0)
        ret, frame = self.camera.read()
        if not ret:
            messagebox.showerror("Error", "Could not capture photo.")
            self.camera.release()
            return

        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        while True:
            ret, frame = self.camera.read()
            if not ret:
                break

            # Convert the image to RGB for displaying in Tkinter
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the image
            face_locations = face_recognition.face_locations(image)

            # Draw a rectangle around each face
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Display the image in the canvas
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.update()

            # Wait for the Capture button to be pressed
            if self.button_capture_pressed:
                cv2.imwrite("temp.jpg", frame)
                self.button_add.config(state=tk.NORMAL)
                break

            # Check for window close button
            if cv2.getWindowProperty("Live Video", cv2.WND_PROP_VISIBLE) < 1:
                break

        # Release the camera and destroy the canvas
        self.camera.release()
        self.canvas.destroy()

        # Show the captured frame in a separate window
        cv2.imshow("Capture", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def add_user(self):
        username = self.entry_username.get()
        if username:
            self.admin.add_user(username, "temp.jpg")
            self.listbox_users.insert(tk.END, username)
            os.remove("temp.jpg")
            self.button_add.config(state=tk.DISABLED)

    def remove_user(self):
        selection = self.listbox_users.curselection()
        if selection:
            index = selection[0]
            username = self.listbox_users.get(index)
            self.admin.remove_user(username)
            self.listbox_users.delete(index)
