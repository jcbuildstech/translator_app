import boto3
from botocore.config import Config as BotoConfig
from src.config import Config
import uuid
from werkzeug.utils import secure_filename

# Initialize R2 client
s3_client = boto3.client(
    's3',
    endpoint_url=Config.R2_ENDPOINT,
    aws_access_key_id=Config.R2_ACCESS_KEY_ID,
    aws_secret_access_key=Config.R2_SECRET_ACCESS_KEY,
    config=BotoConfig(signature_version='s3v4')
)

def upload_to_r2(file, prefix='uploads'):
    """Upload file to R2, return public URL via custom domain"""
    
    # Generate unique filename
    original_filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())[:8]
    extension = original_filename.rsplit('.', 1)[1] if '.' in original_filename else 'jpg'
    filename = f"{prefix}/{unique_id}_{original_filename}"
    
    # Upload to R2
    s3_client.upload_fileobj(
        file,
        Config.R2_BUCKET_NAME,
        filename,
        ExtraArgs={'ContentType': file.content_type or 'image/jpeg'}
    )
    
    # Return public URL via your custom domain
    return f"{Config.R2_PUBLIC_URL}/{filename}"