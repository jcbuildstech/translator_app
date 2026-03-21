import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration from environment variables"""
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    ENV = os.getenv('FLASK_ENV', 'production')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # R2 Storage
    R2_ENDPOINT = os.getenv('R2_ENDPOINT')
    R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
    R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
    R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')
    
    @classmethod
    def validate(cls):
        """Check that required config is present"""
        required = [
            'SECRET_KEY', 'R2_ENDPOINT', 'R2_ACCESS_KEY_ID',
            'R2_SECRET_ACCESS_KEY', 'R2_BUCKET_NAME'
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")