import cv2
import numpy as np
import logging
import os
from datetime import datetime
import mediapipe as mp
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepfakeGenerator:
    def __init__(self):
        self.logger = logger
        self.logger.info("DeepfakeGenerator initialized")
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize video effects
        self.effects = {
            'original': lambda frame: frame,
            'grayscale': lambda frame: cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR),
            'edge': lambda frame: cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 100, 200),
            'blur': lambda frame: cv2.GaussianBlur(frame, (15, 15), 0),
            'face_mesh': self.apply_face_mesh
        }
        
    def adjust_image(self, image, brightness=0, contrast=1):
        """
        Adjust image brightness and contrast
        brightness: -100 to 100
        contrast: 0.0 to 3.0
        """
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
        return adjusted
    
    def apply_face_mesh(self, frame):
        """
        Apply face mesh effect to the frame
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        
        if results.multi_face_landmarks:
            height, width = frame.shape[:2]
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
        
        return frame
    
    def process_image(self, input_path, effect='original', brightness=0, contrast=1):
        """
        Process the input image for deepfake generation with effects
        """
        try:
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Could not read the image")
            
            # Apply adjustments
            img = self.adjust_image(img, brightness, contrast)
            
            # Apply selected effect
            if effect in self.effects:
                img = self.effects[effect](img)
            
            return img
        except Exception as e:
            self.logger.error(f"Error processing image {input_path}: {str(e)}")
            raise
    
    def generate_deepfake(self, input_path, output_path, effect='original', brightness=0, contrast=1):
        """
        Generate a deepfake video from the input file with effects
        """
        try:
            # Log the start of processing
            self.logger.info(f"Starting deepfake generation for input file: {input_path}")
            self.logger.info(f"Output will be saved to: {output_path}")
            self.logger.info(f"Applied effect: {effect}")
            
            # Process the input file
            if input_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Process image input
                img = self.process_image(input_path, effect, brightness, contrast)
                
                # Create a video from the image
                height, width = img.shape[:2]
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))
                
                # Write the image multiple times to create a video with progress bar
                for _ in tqdm(range(90), desc="Generating video from image"):  # 3 seconds at 30 fps
                    out.write(img)
                out.release()
                
            elif input_path.lower().endswith(('.mp4', '.avi', '.mov')):
                # Process video input
                cap = cv2.VideoCapture(input_path)
                if not cap.isOpened():
                    raise ValueError("Could not open the video file")
                
                # Get video properties
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                # Create video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                
                # Process each frame with progress bar
                with tqdm(total=total_frames, desc="Processing video frames") as pbar:
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break
                        
                        # Apply adjustments
                        frame = self.adjust_image(frame, brightness, contrast)
                        
                        # Apply selected effect
                        if effect in self.effects:
                            processed_frame = self.effects[effect](frame)
                            # Convert single channel to BGR if needed (e.g., for edge detection)
                            if len(processed_frame.shape) == 2:
                                processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
                            out.write(processed_frame)
                        
                        pbar.update(1)
                
                cap.release()
                out.release()
            
            self.logger.info(f"Deepfake generation completed: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating deepfake for {input_path}: {str(e)}")
            raise
    
    def cleanup(self):
        """
        Clean up any resources
        """
        self.face_mesh.close()
        cv2.destroyAllWindows()
