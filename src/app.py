from flask import Flask, request, render_template, jsonify
from src.config import Config
from src.storage import upload_to_r2

# Create Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)

# Validate config on startup
Config.validate()

@app.route('/')
def index():
    """Upload form page"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle license image upload with OCR extraction"""
    
    # Check if files were uploaded
    if 'front_image' not in request.files or 'back_image' not in request.files:
        return jsonify({'error': 'Both front and back images required'}), 400
    
    front_file = request.files['front_image']
    back_file = request.files['back_image']
    
    # Check if files have filenames (not empty)
    if front_file.filename == '' or back_file.filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    try:
        # Upload both images to R2
        front_url = upload_to_r2(front_file, prefix='licenses/front')
        back_url = upload_to_r2(back_file, prefix='licenses/back')
        """
        # Reset file pointers so we can read them again for OCR
        front_file.seek(0)
        back_file.seek(0)
        
        # Extract text from both images
        from src.ocr import extract_text_from_image
        front_text = extract_text_from_image(front_file)
        back_text = extract_text_from_image(back_file)
        
        return jsonify({
            'status': 'success',
            'message': 'Images uploaded and processed',
            'front_url': front_url,
            'back_url': back_url,
            'ocr': {
                'front': front_text,
                'back': back_text
            }
        })
        """
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for Coolify"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)