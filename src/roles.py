import discord

async def clear_all(server: discord.Guild):
    for role in server.roles:
        if role.name != "@everyone" and not role.managed:
            try: await role.delete()
            except: pass

async def create_role(server: discord.Guild, data: dict):
    name = data.get("name")
    if not name: return

    color = discord.Color.default()
    hex_code = data.get("hex")
    if hex_code:
        try: color = discord.Color.from_str(hex_code)
        except: pass

    hoist = data.get("hoist", False)
    mentionable = data.get("mentionable", False)

    existing = discord.utils.get(server.roles, name=name)
    if not existing:
        await server.create_role(
            name=name,
            color=color,
            hoist=hoist,
            mentionable=mentionable
        )
