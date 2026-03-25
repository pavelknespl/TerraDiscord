import os
import json
import discord
from typing import List
from .config import PRESETS_DIR
from . import channels

def get_preset_list() -> List[str]:
    if not os.path.exists(PRESETS_DIR): return []
    return [f.replace('.json', '') for f in os.listdir(PRESETS_DIR) if f.endswith('.json')]

async def apply_preset(server: discord.Guild, preset_name: str, clear_all: bool = False, skip_id: int = None):
    file_path = os.path.join(PRESETS_DIR, f"{preset_name}.json")
    if not os.path.exists(file_path): raise FileNotFoundError(f"Preset '{preset_name}' not found.")

    with open(file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if clear_all:
        await channels.clear_all(server, skip_id)

    for cat_data in config.get('categories', []):
        cat_name = cat_data.get('name')
        category = await channels.create_category(server, cat_name)

        for ch_data in cat_data.get('channels', []):
            name = ch_data.get('name')
            ch_type = ch_data.get('type', 'text')
            await channels.create_channel(server, category, name, ch_type)
