# config.py

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME")