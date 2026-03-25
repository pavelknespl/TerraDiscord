import os
import json
import discord
from datetime import datetime
from .config import EXPORTS_DIR

def get_perms_dict(overwrites):
    result = {}
    for target, overwrite in overwrites.items():
        name = target.name if hasattr(target, 'name') else str(target)
        perms = {p: v for p, v in dict(overwrite).items() if v is not None}
        if perms:
            result[name] = perms
    return result

async def export_server(server: discord.Guild):
    data = {
        "server_name": server.name,
        "server_description": server.description or "",
        "roles": [],
        "categories": []
    }

    for role in reversed(server.roles):
        if role.is_default() or role.managed: continue
        
        r_data = {
            "name": role.name,
            "hex": str(role.color),
            "hoist": role.hoist,
            "mentionable": role.mentionable,
            "permissions": {p: v for p, v in dict(role.permissions).items() if v}
        }
        data["roles"].append(r_data)

    for category in server.categories:
        cat_data = {
            "name": category.name,
            "channels": []
        }
        
        for channel in category.channels:
            ch_type = "text"
            if isinstance(channel, discord.VoiceChannel): ch_type = "voice"
            elif isinstance(channel, discord.StageChannel): ch_type = "stage"
            elif isinstance(channel, discord.ForumChannel): ch_type = "forum"
            elif channel.type == discord.ChannelType.news: ch_type = "news"

            ch_data = {
                "name": channel.name,
                "type": ch_type,
                "permissions": get_perms_dict(channel.overwrites)
            }
            cat_data["channels"].append(ch_data)
        
        data["categories"].append(cat_data)

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_name = "".join(x for x in server.name if x.isalnum() or x in " -_").strip()
    filename = f"{safe_name}_{date_str}.json"
    path = os.path.join(EXPORTS_DIR, filename)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filename
