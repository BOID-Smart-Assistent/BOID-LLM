import os
import shutil
import json

def load_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

config = load_config('config.json')
CHROMA_PATH = config['database']['chroma_path']

if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)