import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# API Key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")