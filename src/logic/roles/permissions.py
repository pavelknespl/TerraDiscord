import discord

def get_role_permissions(perms_data: dict) -> discord.Permissions:
    permissions = discord.Permissions()
    for perm_name, value in perms_data.items():
        if hasattr(permissions, perm_name):
            setattr(permissions, perm_name, value)
    return permissions
