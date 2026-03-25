import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))

TOKEN = os.getenv('DISCORD_TOKEN')
PRESETS_DIR = 'presets'
EXPORTS_DIR = 'exports'

if not TOKEN:
    print("Error: DISCORD_TOKEN is missing.")
    exit(1)

for d in [PRESETS_DIR, EXPORTS_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)
