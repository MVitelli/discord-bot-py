import os
import requests
import json
import discord
from dotenv import load_dotenv

load_dotenv()

POKEMON_URL = 'https://pokeapi.co/api/v2/pokemon/'  
OPERATOR = '?'
TOKEN = os.getenv('DISCORD_TOKEN')

def get_pokemon (pokemon):
    response = requests.get(POKEMON_URL + pokemon)
    json_data = json.loads(response.text)
    return json_data

def print_pokemon_type (types):
    poke_types = ""
    for type in types:
        poke_types+= type['type']['name'].capitalize() + "\n"
    return poke_types

class MaxSal(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        
    async def on_message(self, message):
        print(f'Message from {message.author.name}: {message.content}')
        if message.content[0] != OPERATOR:
            return
        command = message.content[1:]
        command = command.split(" ")
        if command[0] == "pokemon":
            pokemon_to_search = command[1]
            types = get_pokemon(pokemon_to_search)['types']
            await message.channel.send(f'{pokemon_to_search} has these types: \n{print_pokemon_type(types)}')

client = MaxSal()
client.run(TOKEN)
