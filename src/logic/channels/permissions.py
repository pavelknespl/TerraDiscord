import discord

def get_channel_overwrites(server: discord.Guild, perms_data: dict) -> dict:
    overwrites = {}
    for role_name, perms in perms_data.items():
        role = discord.utils.get(server.roles, name=role_name)
        if role:
            overwrite = discord.PermissionOverwrite()
            for perm_name, value in perms.items():
                if hasattr(overwrite, perm_name):
                    setattr(overwrite, perm_name, value)
            overwrites[role] = overwrite
    return overwrites
