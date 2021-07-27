import os
from discord.client import Client
import requests
import json
import discord
from fourinarow import fourInARowMatch
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

    # matchInProg = self.matchInProg

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        self.match = fourInARowMatch()
        self.lastBoard = None

    async def on_message(self, message):
        if message.author == self.user:
            return

        lastBoard = self.lastBoard

        print(f'Message from {message.author.name}: {message.content}')
        if message.content[0] != OPERATOR:
            return
        
        command = message.content[1:]
        command = command.split(" ")
        
        # if command[0] == "pokemon":
        #     pokemon_to_search = command[1]
        #     types = get_pokemon(pokemon_to_search)['types']
        #     await message.channel.send(f'{pokemon_to_search} has these types: \n{print_pokemon_type(types)}')
        
        if command[0] == "4inarow" and command[1] == "start":
            if self.match.getMatchInProg():
                await message.channel.send(f'There is a match in progress')
                return
            self.match.newMatchInProg()
            lastBoard = await message.channel.send(file=discord.File("img/4inrow.png"))
            await lastBoard.add_reaction()
            return
        if self.match.getMatchInProg():
            if command[0] == 'put': 
                if self.match.addPiece(command[1]):
                    self.match.boardUpdate()

                    await message.channel.send(file=discord.File("img/4inrow.png"))
                else:
                    await message.channel.send(f'Bad move')
            winner = self.match.checkWinner()
            if winner > 0:
                if winner == 1 or winner == 2:
                    await message.channel.send(f'Player {winner} wins!')
                else:
                    await message.channel.send(f'Draw!')
                del self.match
                self.match = fourInARowMatch()
            else:
                self.match.changePlayer()



    # def __init__(self):


client = MaxSal()

client.run(TOKEN)
