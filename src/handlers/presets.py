import os
import json
import discord
from typing import List
from ..core.config import PRESETS_DIR
from ..logic.roles import manager as roles_manager
from ..logic.channels import manager as channels_manager

def get_preset_list() -> List[str]:
    if not os.path.exists(PRESETS_DIR): return []
    return [f.replace('.json', '') for f in os.listdir(PRESETS_DIR) if f.endswith('.json')]

async def apply_preset(server: discord.Guild, preset_name: str, clear_all: bool = False, skip_id: int = None):
    file_path = os.path.join(PRESETS_DIR, f"{preset_name}.json")
    if not os.path.exists(file_path): raise FileNotFoundError(f"Preset '{preset_name}' not found.")

    with open(file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    new_name = config.get("server_name")
    new_desc = config.get("server_description")
    if new_name or new_desc:
        try: await server.edit(name=new_name if new_name else server.name, description=new_desc if new_desc else server.description)
        except: pass

    if clear_all:
        await roles_manager.clear_all(server)
        await channels_manager.clear_all(server, skip_id)

    for role_data in config.get('roles', []):
        await roles_manager.create_role(server, role_data)

    for cat_data in config.get('categories', []):
        cat_name = cat_data.get('name')
        category = await channels_manager.create_category(server, cat_name)

        for ch_data in cat_data.get('channels', []):
            name = ch_data.get('name')
            ch_type = ch_data.get('type', 'text')
            perms = ch_data.get('permissions', {})
            await channels_manager.create_channel(server, category, name, ch_type, perms)
