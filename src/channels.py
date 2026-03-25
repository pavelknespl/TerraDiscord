import discord

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
    category = discord.utils.get(server.categories, name=name)
    if not category:
        category = await server.create_category(name)
    return category

async def create_channel(server: discord.Guild, category: discord.CategoryChannel, name: str, ch_type: str):
    existing = discord.utils.get(category.channels, name=name)
    if existing: return

    if ch_type == 'text':
        await server.create_text_channel(name, category=category)
    elif ch_type == 'voice':
        await server.create_voice_channel(name, category=category)
    elif ch_type == 'news':
        await server.create_text_channel(name, category=category, type=discord.ChannelType.news)
    elif ch_type == 'forum':
        await server.create_forum_channel(name, category=category)
