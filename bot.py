import discord
from discord.ext import commands
from discord import app_commands
import json
import stashtracker

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=discord.Intents.all())
    
    async def on_ready(self):
        print(f"✅ Bot {self.user} has logged in successfully.")
        guild = discord.Object(id=config['guild_id'])
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

client = Bot()

@client.tree.command(name="stashes", description="Get the list of stashes")
@app_commands.describe()
async def stashes(interaction: discord.Interaction):
    stashes = stashtracker.get_stashes()
    embed = discord.Embed(title="📦 Stashes", color=discord.Color.blue())
    for stash in stashes:
        kitCount = len(stashtracker.get_kits_by_stash_id(stash["id"]))
        dubCount = (kitCount + 53) // 54
        embed.add_field(name=f"{stash['id']} | {stash["name"]}", value=f'{dubCount} dubs • {kitCount} kits', inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="kits", description="Get the list of kits in a stash")
@app_commands.describe()
async def kits(interaction: discord.Interaction, stash_id: int):
    kits = stashtracker.get_kits_by_stash_id(stash_id)
    embed = discord.Embed(title="🛠 Kits", color=discord.Color.blue())
    for kit in kits:
        embed.add_field(name=kit["name"], value=kit["description"], inline=False)
    await interaction.response.send_message(embed=embed)

client.run(config['token'])
