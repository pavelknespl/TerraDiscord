import discord
from .permissions import get_channel_overwrites

async def clear_all(server: discord.Guild, skip_id: int = None):
    for category in server.categories:
        for channel in category.channels:
            if channel.id != skip_id:
                try: await channel.delete()
                except: pass
        if not category.channels:
            try: await category.delete()
            except: pass
    
    for channel in server.channels:
        if channel.id != skip_id:
            try: await channel.delete()
            except: pass

async def create_category(server: discord.Guild, name: str):
    try:
        category = discord.utils.get(server.categories, name=name)
        if not category:
            category = await server.create_category(name)
        return category
    except:
        return None

async def create_channel(server: discord.Guild, category: discord.CategoryChannel, name: str, ch_type: str, perms_data: dict = None):
    existing = discord.utils.get(category.channels if category else server.channels, name=name)
    if existing: return

    overwrites = get_channel_overwrites(server, perms_data) if perms_data else {}

    try:
        if ch_type == 'voice':
            await server.create_voice_channel(name, category=category, overwrites=overwrites)
        elif ch_type == 'forum':
            await server.create_forum_channel(name, category=category, overwrites=overwrites)
        elif ch_type == 'stage':
            await server.create_stage_channel(name, category=category, overwrites=overwrites)
        elif ch_type == 'news':
            try: await server.create_text_channel(name, category=category, overwrites=overwrites, news=True)
            except: await server.create_text_channel(name, category=category, overwrites=overwrites)
        else:
            await server.create_text_channel(name, category=category, overwrites=overwrites)
    except:
        try:
            if ch_type != 'text':
                await server.create_text_channel(name, category=category, overwrites=overwrites)
        except: pass
