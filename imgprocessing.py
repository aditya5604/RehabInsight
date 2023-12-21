import tkinter as tk
from PIL import Image, ImageTk
import cv2
from pathlib import Path
from threading import Thread
from yolov5.infer import Detector

class ImageProcessor:
    def __init__(self, window):
        self.window = window
        self.window.title("Image Processing")
        self.video_source = 0 

        # Create a canvas to display the processed video feed
        self.canvas = tk.Canvas(window, width=800, height=600)
        self.canvas.pack()

        # Create a button to start the video processing
        self.process_button = tk.Button(window, text="Start Processing", command=self.start_processing, width=20, height=3, font=("Helvetica", 16))
        self.process_button.pack(pady=10)

        # Create a button to stop the video processing
	self.stop_button = tk.Button(window, text="Stop Processing", command=self.stop_processing, width=20, height=3, font=("Helvetica", 16), state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Create an instance of the Detector class
        self.detector = Detector()

	# Initialize variables for video processing
        self.video_capture = None
        self.processing = False

        # Start the Tkinter event loop
        window.protocol("WM_DELETE_WINDOW", self.on_close)
        window.mainloop()

    def start_processing(self):
        # Disable the start button and enable the stop button
        self.process_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Open the video capture
        self.video_capture = cv2.VideoCapture(self.video_source)

        # Start the video processing thread
        self.processing = True
        self.process_thread = Thread(target=self.process_video)
        self.process_thread.start()

    def stop_processing(self):
        # Enable the start button and disable the stop button
        self.process_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Stop the video processing
        self.processing = False
        self.process_thread.join()

        # Release the video capture
        if self.video_capture:
            self.video_capture.release()

    def process_video(self):
        while self.processing:
            # Read a frame from the video capture
            ret, frame = self.video_capture.read()
            if not ret:
                break

            # Process the frame using YOLOv5
            result_frame = self.detector.process_frame(frame)

            # Convert the OpenCV frame to a PIL image
            img = cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)

            # Update the canvas with the new image
            self.canvas.img = img  # To prevent garbage collection
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.window.update()

        # Release the video capture when processing stops
        if self.video_capture:
            self.video_capture.release()

    def on_close(self):
        # Ensure video capture is released before closing the window
        if self.video_capture:
            self.video_capture.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
