import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PRESETS_DIR = 'presets'

if not TOKEN:
    print("Error: DISCORD_TOKEN not found in .env")
    exit(1)

if not os.path.exists(PRESETS_DIR):
    os.makedirs(PRESETS_DIR)
