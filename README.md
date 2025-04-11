# Deepfake Generator

A user-friendly application for generating and manipulating deepfake videos with various effects.

## Features

- GUI and CLI interfaces
- Multiple video effects (face mesh, grayscale, edge detection, blur)
- Brightness and contrast adjustments
- Real-time video preview
- Progress tracking
- Support for images and videos

## Installation

### Option 1: Executable (Recommended)

1. Download the latest release for your platform
2. Extract the zip file
3. Run `DeepfakeGenerator` for the GUI version or `DeepfakeGenerator-CLI` for the command-line version

### Option 2: From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/deepfake-generator.git
cd deepfake-generator

# Install dependencies
pip install -r requirements.txt

# Run the GUI version
python desktop_app.py

# Run the CLI version
python cli_app.py
```

## Usage

### GUI Version

1. Launch `DeepfakeGenerator`
2. Click "Browse" to select an input file (image or video)
3. Choose an effect from the dropdown menu
4. Adjust brightness and contrast if desired
5. Click "Generate Deepfake"
6. View the result in the built-in viewer

### CLI Version

```bash
# Basic usage
DeepfakeGenerator-CLI input_file.jpg

# With effects and adjustments
DeepfakeGenerator-CLI input_file.mp4 --effect face_mesh --brightness 10 --contrast 1.2

# Available effects
--effect [original|grayscale|edge|blur|face_mesh]

# Adjustment ranges
--brightness [-100 to 100]
--contrast [0.0 to 3.0]
```

## Supported File Types

- Images: .png, .jpg, .jpeg
- Videos: .mp4, .avi, .mov

## System Requirements

- Operating System: Windows 10/11, macOS 10.15+, or Linux
- RAM: 4GB minimum, 8GB recommended
- Storage: 500MB free space
- GPU: Optional but recommended for better performance

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please create an issue on the GitHub repository.
