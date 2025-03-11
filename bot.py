import discord
import json
import stashtracker

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user.name} is ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?stashes'):
        stashes = stashtracker.get_stashes()
        embed = discord.Embed(title="Stashes", color=discord.Color.blue())
        for stash in stashes:
            kits_count = (len(stashtracker.get_kits_by_stash_id(stash["id"])) + 53) // 54
            embed.add_field(name=stash["name"], value=f'{kits_count} dubs', inline=False)
        await message.channel.send(embed=embed)

client.run(config['token']) 