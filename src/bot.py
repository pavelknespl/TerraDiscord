import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from typing import List
from .config import TOKEN
from .presets_util import get_preset_list, apply_preset

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

async def preset_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    presets = get_preset_list()
    return [
        app_commands.Choice(name=p, value=p)
        for p in presets if current.lower() in p.lower()
    ]

@bot.tree.command(name="add", description="Add preset to server")
@app_commands.describe(preset="Preset name")
@app_commands.checks.has_permissions(administrator=True)
async def add_preset_cmd(interaction: discord.Interaction, preset: str):
    await interaction.response.defer(ephemeral=True)
    try:
        await apply_preset(interaction.guild, preset, clear_all=False)
        await interaction.followup.send(f"Preset '{preset}' added.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="set", description="Reset server and apply preset")
@app_commands.describe(preset="Preset name")
@app_commands.checks.has_permissions(administrator=True)
async def set_preset_cmd(interaction: discord.Interaction, preset: str):
    await interaction.response.defer(ephemeral=True)
    try:
        await apply_preset(interaction.guild, preset, clear_all=True, skip_id=interaction.channel.id)
        await interaction.followup.send(f"Server reset and preset '{preset}' applied.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)

@add_preset_cmd.autocomplete('preset')
@set_preset_cmd.autocomplete('preset')
async def set_ac(interaction, current):
    return await preset_autocomplete(interaction, current)

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}")

def run():
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Missing TOKEN.")
