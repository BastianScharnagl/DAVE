import os
from dotenv import load_dotenv

class Config:
    """Configuration class that loads settings from environment variables."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    # API Keys
    KI_AWZ_API_KEY = os.getenv('KI_AWZ_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Service URLs
    KI_AWZ_API_URL = os.getenv('KI_AWZ_API_URL', 'https://chat-1.ki-awz.iisys.de/api')
    
    # Model Configuration
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'lisa-v40-rc1-qwen3235b-a22b-instruct')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Application settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16384'))
    
    @staticmethod
    def validate():
        """Validate that required configuration values are present."""
        required = ['KI_AWZ_API_KEY']
        missing = [key for key in required if not getattr(Config, key)]
        
        if missing:
            raise ValueError(f"Missing required configuration values: {', '.join(missing)}")
        
        return True