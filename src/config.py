import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))

TOKEN = os.getenv('DISCORD_TOKEN')
PRESETS_DIR = 'presets'

if not TOKEN:
    print("Error: DISCORD_TOKEN is missing or .env file is unreadable.")
    exit(1)

if not os.path.exists(PRESETS_DIR):
    os.makedirs(PRESETS_DIR)
