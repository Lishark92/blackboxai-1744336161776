import argparse
import os
from deepfake import DeepfakeGenerator
from datetime import datetime
from desktop_app_config import UPLOAD_FOLDER, GENERATED_FOLDER, allowed_file
import shutil
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='Deepfake Generator CLI')
    parser.add_argument('input', help='Input file path (image or video)')
    parser.add_argument('--effect', default='original', 
                       choices=['original', 'grayscale', 'edge', 'blur', 'face_mesh'],
                       help='Effect to apply')
    parser.add_argument('--brightness', type=int, default=0,
                       help='Brightness adjustment (-100 to 100)')
    parser.add_argument('--contrast', type=float, default=1.0,
                       help='Contrast adjustment (0.0 to 3.0)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist")
        return
    
    if not allowed_file(args.input):
        print("Error: Invalid file type. Supported types: .png, .jpg, .jpeg, .mp4, .avi, .mov")
        return
    
    try:
        # Initialize generator
        generator = DeepfakeGenerator()
        
        # Create unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.basename(args.input)
        name, _ = os.path.splitext(filename)
        output_filename = f"deepfake_{name}_{timestamp}.mp4"
        
        # Copy input file to uploads folder
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        print(f"\nCopying input file to: {upload_path}")
        shutil.copy2(args.input, upload_path)
        
        # Generate output path
        output_path = os.path.join(GENERATED_FOLDER, output_filename)
        
        # Process parameters
        print("\nProcessing with parameters:")
        print(f"Effect: {args.effect}")
        print(f"Brightness: {args.brightness}")
        print(f"Contrast: {args.contrast}")
        
        # Generate deepfake with progress bar
        print("\nGenerating deepfake...")
        generator.generate_deepfake(
            upload_path,
            output_path,
            effect=args.effect,
            brightness=args.brightness,
            contrast=args.contrast
        )
        
        print(f"\nDeepfake generated successfully!")
        print(f"Output saved to: {output_path}")
        
        # Start HTTP server to serve the file
        print(f"\nStarting HTTP server to serve the generated file...")
        print(f"Please open http://localhost:8000/{output_filename} in your web browser")
        os.system(f'python3 -m http.server 8000 -d {GENERATED_FOLDER}')
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    # Create required directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(GENERATED_FOLDER, exist_ok=True)
    main()
