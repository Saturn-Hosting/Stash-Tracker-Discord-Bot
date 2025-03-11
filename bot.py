import discord
import json
import requests

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def get_stashes():
    url = config['url'] + '/stashes'
    response = requests.get(url)
    return response.json()

def get_kits_by_stash_id(stash_id):
    url = config['url'] + f'/kits?stash_id={stash_id}'
    response = requests.get(url)
    return response.json()


@client.event
async def on_ready():
    print(f'{client.user.name} is ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?stashes'):
        stashes = get_stashes()
        r = ''
        for stash in stashes:
            kitCount = len(get_kits_by_stash_id(stash['id']))
            dubCount = (kitCount + 53) // 54
            r += f'{stash["name"]} - {dubCount} dubs\n'
        await message.channel.send(r)

client.run(config['token']) 