import discord
from discord import app_commands
from discord.ext import commands
from typing import List
from .config import TOKEN
from ..handlers import presets, exporter
from ..logic.roles import manager as roles_manager
from ..logic.channels import manager as channels_manager

class DiscordAsCodeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Ready.")

bot = DiscordAsCodeBot()

@bot.tree.command(name="add", description="Add preset to server")
@app_commands.describe(preset="Preset name")
@app_commands.checks.has_permissions(administrator=True)
async def add_preset_cmd(interaction: discord.Interaction, preset: str):
    await interaction.response.defer(ephemeral=True)
    try:
        await presets.apply_preset(interaction.guild, preset, clear_all=False)
        await interaction.followup.send(f"Preset '{preset}' added.", ephemeral=True)
    except Exception as e: await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="set", description="Reset server and apply preset")
@app_commands.describe(preset="Preset name")
@app_commands.checks.has_permissions(administrator=True)
async def set_preset_cmd(interaction: discord.Interaction, preset: str):
    await interaction.response.defer(ephemeral=True)
    try:
        await presets.apply_preset(interaction.guild, preset, clear_all=True, skip_id=interaction.channel.id)
        await interaction.followup.send(f"Server reset and preset '{preset}' applied.", ephemeral=True)
    except Exception as e: await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="reset", description="Delete ALL roles and channels")
@app_commands.checks.has_permissions(administrator=True)
async def reset_cmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        await roles_manager.clear_all(interaction.guild)
        await channels_manager.clear_all(interaction.guild, skip_id=interaction.channel.id)
        await interaction.followup.send("Server cleared.", ephemeral=True)
    except Exception as e: await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="export", description="Export current server structure")
@app_commands.checks.has_permissions(administrator=True)
async def export_cmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        filename = await exporter.export_server(interaction.guild)
        await interaction.followup.send(f"Exported to 'exports/{filename}'.", ephemeral=True)
    except Exception as e: await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)

@add_preset_cmd.autocomplete('preset')
@set_preset_cmd.autocomplete('preset')
async def set_ac(interaction, current: str) -> List[app_commands.Choice[str]]:
    return [app_commands.Choice(name=p, value=p) for p in presets.get_preset_list() if current.lower() in p.lower()]

def run():
    if TOKEN: bot.run(TOKEN)
    else: print("Missing TOKEN.")
