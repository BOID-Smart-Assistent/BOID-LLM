import os
import shutil
import json
from dotenv import load_dotenv
import os
# Load .env file
load_dotenv()

CHROMA_PATH = os.getenv('DATABASE_CHROMA_PATH')

if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)