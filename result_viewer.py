import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import os
from desktop_app_config import GENERATED_FOLDER

class ResultViewer:
    def __init__(self, video_path):
        self.window = tk.Toplevel()
        self.window.title("Deepfake Result Viewer")
        self.window.geometry("800x600")
        
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        
        # Get video properties
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        self.current_frame = 0
        self.playing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Video display
        self.canvas = tk.Canvas(
            main_frame, 
            width=min(self.width, 800),
            height=min(self.height, 450)
        )
        self.canvas.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Play/Pause button
        self.play_button = ttk.Button(
            controls_frame,
            text="Play",
            command=self.toggle_play
        )
        self.play_button.grid(row=0, column=0, padx=5)
        
        # Frame slider
        self.frame_var = tk.IntVar(value=0)
        self.frame_slider = ttk.Scale(
            controls_frame,
            from_=0,
            to=self.total_frames - 1,
            variable=self.frame_var,
            orient=tk.HORIZONTAL,
            length=400,
            command=self.slider_changed
        )
        self.frame_slider.grid(row=0, column=1, padx=5)
        
        # Frame counter
        self.frame_label = ttk.Label(
            controls_frame,
            text=f"Frame: 0/{self.total_frames-1}"
        )
        self.frame_label.grid(row=0, column=2, padx=5)
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Show first frame
        self.show_frame(0)
        
    def show_frame(self, frame_number):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        if ret:
            # Convert frame from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize frame if needed
            display_width = min(self.width, 800)
            display_height = min(self.height, 450)
            aspect_ratio = self.width / self.height
            
            if aspect_ratio > display_width / display_height:
                new_width = display_width
                new_height = int(display_width / aspect_ratio)
            else:
                new_height = display_height
                new_width = int(display_height * aspect_ratio)
            
            frame = cv2.resize(frame, (new_width, new_height))
            
            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(
                display_width//2,
                display_height//2,
                image=self.photo,
                anchor=tk.CENTER
            )
            
            # Update frame counter
            self.frame_label.config(text=f"Frame: {frame_number}/{self.total_frames-1}")
    
    def slider_changed(self, value):
        frame_number = int(float(value))
        self.show_frame(frame_number)
        self.current_frame = frame_number
    
    def toggle_play(self):
        self.playing = not self.playing
        self.play_button.config(text="Pause" if self.playing else "Play")
        if self.playing:
            self.play_video()
    
    def play_video(self):
        if self.playing:
            self.current_frame += 1
            if self.current_frame >= self.total_frames:
                self.current_frame = 0
            
            self.frame_var.set(self.current_frame)
            self.show_frame(self.current_frame)
            
            # Schedule next frame update
            self.window.after(int(1000/self.fps), self.play_video)
    
    def cleanup(self):
        self.playing = False
        if self.cap is not None:
            self.cap.release()
        self.window.destroy()

def show_result(video_path):
    viewer = ResultViewer(video_path)
    viewer.window.protocol("WM_DELETE_WINDOW", viewer.cleanup)
    return viewer
