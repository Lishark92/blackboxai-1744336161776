import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import os
from deepfake import DeepfakeGenerator
from datetime import datetime
from desktop_app_config import UPLOAD_FOLDER, GENERATED_FOLDER, allowed_file
import shutil

class DeepfakeDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deepfake Generator Desktop")
        self.root.geometry("800x600")
        
        # Initialize DeepfakeGenerator
        self.generator = DeepfakeGenerator()
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Deepfake Generator", 
            font=("Helvetica", 24, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(
            self.main_frame, 
            text="File Selection", 
            padding="10"
        )
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(
            file_frame, 
            textvariable=self.file_path, 
            width=50
        )
        file_entry.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        browse_button = ttk.Button(
            file_frame, 
            text="Browse", 
            command=self.browse_file
        )
        browse_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Effect settings frame
        effect_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Effect Settings", 
            padding="10"
        )
        effect_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Effect selection
        ttk.Label(effect_frame, text="Effect:").grid(row=0, column=0, padx=5, pady=5)
        self.effect_var = tk.StringVar(value="original")
        effect_combo = ttk.Combobox(
            effect_frame, 
            textvariable=self.effect_var,
            values=list(self.generator.effects.keys()),
            state="readonly"
        )
        effect_combo.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Brightness control
        ttk.Label(effect_frame, text="Brightness:").grid(row=1, column=0, padx=5, pady=5)
        self.brightness_var = tk.IntVar(value=0)
        brightness_scale = ttk.Scale(
            effect_frame,
            from_=-100,
            to=100,
            variable=self.brightness_var,
            orient=tk.HORIZONTAL
        )
        brightness_scale.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Contrast control
        ttk.Label(effect_frame, text="Contrast:").grid(row=2, column=0, padx=5, pady=5)
        self.contrast_var = tk.DoubleVar(value=1.0)
        contrast_scale = ttk.Scale(
            effect_frame,
            from_=0.0,
            to=3.0,
            variable=self.contrast_var,
            orient=tk.HORIZONTAL
        )
        contrast_scale.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Generate button
        self.generate_button = ttk.Button(
            self.main_frame,
            text="Generate Deepfake",
            command=self.generate_deepfake,
            style="Accent.TButton"
        )
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            self.main_frame,
            length=300,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            wraplength=700
        )
        self.status_label.grid(row=5, column=0, columnspan=2)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Helvetica", 11, "bold"))
    
    def browse_file(self):
        filetypes = (
            ('Image files', '*.png *.jpg *.jpeg'),
            ('Video files', '*.mp4 *.avi *.mov'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Select a file',
            filetypes=filetypes
        )
        
        if filename:
            if not allowed_file(filename):
                messagebox.showerror(
                    "Invalid File",
                    "Please select a file with one of these extensions: .png, .jpg, .jpeg, .mp4, .avi, .mov"
                )
                return
            self.file_path.set(filename)
    
    def generate_deepfake(self):
        input_path = self.file_path.get()
        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("Error", "Please select a valid file")
            return
        
        try:
            # Update UI state
            self.generate_button.state(['disabled'])
            self.status_var.set("Processing...")
            self.progress_var.set(0)
            self.root.update()
            
            # Create unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.basename(input_path)
            name, _ = os.path.splitext(filename)
            output_filename = f"deepfake_{name}_{timestamp}.mp4"
            
            # Copy input file to uploads folder
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            shutil.copy2(input_path, upload_path)
            
            # Generate output path
            output_path = os.path.join(GENERATED_FOLDER, output_filename)
            
            # Generate deepfake
            self.generator.generate_deepfake(
                upload_path,
                output_path,
                effect=self.effect_var.get(),
                brightness=self.brightness_var.get(),
                contrast=self.contrast_var.get()
            )
            
            # Update UI
            self.progress_var.set(100)
            self.status_var.set(f"Deepfake generated successfully!\nSaved as: {output_filename}")
            
            # Show the result viewer
            from result_viewer import show_result
            viewer = show_result(output_path)
            
            # Ask to open output folder
            if messagebox.askyesno("Success", "Would you like to open the output folder?"):
                if os.name == 'nt':  # Windows
                    os.startfile(GENERATED_FOLDER)
                else:  # Linux/Mac
                    os.system(f'python3 -m http.server 8000 -d {GENERATED_FOLDER}')
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set(f"Error: {str(e)}")
            self.progress_var.set(0)
        
        finally:
            self.generate_button.state(['!disabled'])
            self.root.update()

def main():
    root = tk.Tk()
    root.title("Deepfake Generator")
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')  # Use 'clam' theme for better looking widgets
    
    app = DeepfakeDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
