import pytesseract
from PIL import Image
import cv2
import numpy as np
import io

def preprocess_license_image(image):
    """
    Aggressive preprocessing to remove dot pattern and enhance text
    
    Args:
        image: PIL Image object
    
    Returns:
        numpy array: Preprocessed image ready for OCR
    """
    # Convert PIL to OpenCV format
    img_array = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Apply morphological operations to remove dot pattern
    kernel = np.ones((2,2), np.uint8)
    morph = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
    
    # Adaptive threshold - handles varying lighting
    thresh = cv2.adaptiveThreshold(
        morph, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Invert if needed (make text black on white background)
    if np.mean(thresh) < 127:
        thresh = cv2.bitwise_not(thresh)
    
    return thresh

def extract_text_from_image(image_file):
    """
    Extract text from license image using advanced preprocessing
    
    Args:
        image_file: Flask FileStorage object or file object
    
    Returns:
        str: Extracted text
    """
    # Read bytes
    image_bytes = image_file.read()
    image_file.seek(0)
    
    # Open as PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Preprocess
    processed = preprocess_license_image(image)
    
    # Run Tesseract with custom config for license-like documents
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÑ0123456789/-. '
    text = pytesseract.image_to_string(
        processed, 
        lang='spa',
        config=custom_config
    )
    
    return text.strip()