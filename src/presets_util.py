import os
import json
import discord
from typing import List
from .config import PRESETS_DIR

def get_preset_list() -> List[str]:
    if not os.path.exists(PRESETS_DIR):
        return []
    return [f.replace('.json', '') for f in os.listdir(PRESETS_DIR) if f.endswith('.json')]

async def clear_server_channels(server: discord.Guild, skip_id: int = None):
    for category in server.categories:
        for channel in category.channels:
            if channel.id != skip_id:
                await channel.delete()
        if not category.channels:
            await category.delete()
    
    for channel in server.channels:
        if channel.id != skip_id:
            try:
                await channel.delete()
            except discord.NotFound:
                pass

async def apply_preset(server: discord.Guild, preset_name: str, clear_all: bool = False, skip_id: int = None):
    file_path = os.path.join(PRESETS_DIR, f"{preset_name}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Preset '{preset_name}' not found.")

    with open(file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if clear_all:
        await clear_server_channels(server, skip_id)

    for cat_data in config.get('categories', []):
        cat_name = cat_data.get('name')
        category = discord.utils.get(server.categories, name=cat_name)
        if not category:
            category = await server.create_category(cat_name)

        for ch_data in cat_data.get('channels', []):
            name = ch_data.get('name')
            ch_type = ch_data.get('type', 'text')
            existing = discord.utils.get(category.channels, name=name)
            if not existing:
                if ch_type == 'text':
                    await server.create_text_channel(name, category=category)
                elif ch_type == 'voice':
                    await server.create_voice_channel(name, category=category)
