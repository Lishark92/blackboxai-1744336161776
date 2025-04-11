from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import config
from deepfake import DeepfakeGenerator

app = Flask(__name__)
app.config.from_object(config)

# Initialize the DeepfakeGenerator
deepfake_generator = DeepfakeGenerator()

def get_unique_filename(filename):
    """Generate a unique filename using timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    return f"{name}_{timestamp}{ext}"

@app.route('/')
def index():
    """Render the main page"""
    effects = list(deepfake_generator.effects.keys())
    return render_template('index.html', effects=effects)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and deepfake generation"""
    if 'file' not in request.files:
        flash('No file selected. Please choose a file to upload.')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected. Please choose a file to upload.')
        return redirect(url_for('index'))
    
    if file and config.allowed_file(file.filename):
        try:
            # Get effect and adjustment parameters
            effect = request.form.get('effect', 'original')
            brightness = int(request.form.get('brightness', 0))
            contrast = float(request.form.get('contrast', 1.0))
            
            # Validate parameters
            if effect not in deepfake_generator.effects:
                flash('Invalid effect selected.')
                return redirect(url_for('index'))
            
            if not (-100 <= brightness <= 100):
                flash('Brightness must be between -100 and 100.')
                return redirect(url_for('index'))
                
            if not (0.0 <= contrast <= 3.0):
                flash('Contrast must be between 0.0 and 3.0.')
                return redirect(url_for('index'))
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            unique_filename = get_unique_filename(filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(input_path)
            
            # Generate output filename
            output_filename = f"deepfake_{unique_filename.rsplit('.', 1)[0]}.mp4"
            output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
            
            # Generate deepfake with effects
            deepfake_generator.generate_deepfake(
                input_path, 
                output_path,
                effect=effect,
                brightness=brightness,
                contrast=contrast
            )
            
            # Redirect to result page
            return redirect(url_for('result', filename=output_filename))
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}. Please try again or check the file format.')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a file with one of the allowed extensions: png, jpg, jpeg, mp4, avi, mov.')
        return redirect(url_for('index'))

@app.route('/result/<filename>')
def result(filename):
    """Display the result page with the generated video"""
    return render_template('result.html', filename=filename)

@app.route('/history')
def history():
    """Display history of generated videos"""
    generated_files = []
    for filename in os.listdir(app.config['GENERATED_FOLDER']):
        if filename.startswith('deepfake_'):
            file_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
            timestamp = os.path.getmtime(file_path)
            generated_files.append({
                'filename': filename,
                'timestamp': datetime.fromtimestamp(timestamp)
            })
    
    # Sort by timestamp, newest first
    generated_files.sort(key=lambda x: x['timestamp'], reverse=True)
    return render_template('history.html', files=generated_files)

@app.route('/download/<filename>')
def download(filename):
    """Download a generated video"""
    return send_from_directory(app.config['GENERATED_FOLDER'], filename)

@app.route('/video/<filename>')
def video(filename):
    """Stream a generated video"""
    return send_from_directory(app.config['GENERATED_FOLDER'], filename)

if __name__ == '__main__':
    # Create required directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)
    app.run(debug=True)
