import os
import subprocess
import shutil
import sys

def run_command(command):
    print(f"\nExecuting: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())
    
    return process.returncode == 0

def build_executable():
    print("Starting build process for Deepfake Generator...")
    
    # Create necessary directories
    print("\nCreating directories...")
    os.makedirs("static/uploads", exist_ok=True)
    os.makedirs("static/generated", exist_ok=True)
    os.makedirs("build", exist_ok=True)
    os.makedirs("dist", exist_ok=True)
    
    # Generate icon
    print("\nGenerating application icon...")
    if not run_command("python3 create_icon.py"):
        print("Failed to create icon")
        return False
    
    # Install PyInstaller if not already installed
    print("\nInstalling PyInstaller...")
    if not run_command("pip install pyinstaller"):
        print("Failed to install PyInstaller")
        return False
    
    # Build the executable
    print("\nBuilding executable...")
    if not run_command("pyinstaller deepfake_generator.spec"):
        print("Failed to build executable")
        return False
    
    # Create distribution zip file
    print("\nCreating distribution package...")
    dist_files = [
        "dist/DeepfakeGenerator.exe" if sys.platform == "win32" else "dist/DeepfakeGenerator",
        "dist/DeepfakeGenerator-CLI.exe" if sys.platform == "win32" else "dist/DeepfakeGenerator-CLI",
        "README.md",
        "icon.png"
    ]
    
    zip_name = f"DeepfakeGenerator-{sys.platform}.zip"
    try:
        import zipfile
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in dist_files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
    except Exception as e:
        print(f"Failed to create zip file: {e}")
        return False
    
    print(f"\nBuild completed successfully!")
    print(f"Executable package created: {zip_name}")
    print("\nContents:")
    print("- DeepfakeGenerator (GUI application)")
    print("- DeepfakeGenerator-CLI (Command-line interface)")
    print("- README.md (Documentation)")
    print("- icon.png (Application icon)")
    
    return True

if __name__ == "__main__":
    build_executable()
