import requests
import json

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

def get_stashes():
    url = config['url'] + '/stashes'
    response = requests.get(url)
    return response.json()

def get_kits_by_stash_id(stash_id):
    url = config['url'] + f'/kits?stash_id={stash_id}'
    response = requests.get(url)
    return response.json()

def get_players_in_auth():
    url = config['authurl']
    response = requests.get(url)
    return response.json()