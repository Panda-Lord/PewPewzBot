import discord
import os
import bottasks
import db
from dotenv import load_dotenv
load_dotenv(verbose=True)
from pathlib import Path
env_path = Path('.') / '.env'

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content
    bingo = bottasks.Bingo()

    if msg.startswith('!help'):
        help = [
                'PewPewzBot is here to help!',
                '!stock GME - price of GameStop',
                '!crype BTC - price of BitCoin',
                '!bingo score - Current bingo scores',
                '!bingo add word - Adds "word" to bingo game',
                '!bingo info word - Gives info on "word"',
                '!bingo remove word - Removes "word" from the game'
        ]
        await message.channel.send("\n".join(help))

    if msg.startswith('!stock'):
        query = msg.split(" ")
        response = bottasks.Finance(query[1]).quote_stock()
        await message.channel.send(response)

    if msg.startswith('!crypto'):
        query = msg.split(" ")
        await message.channel.send(bottasks.Finance(query[1]).quote_crypto())

    if msg.startswith('!bingo score'):
        await message.channel.send(bingo.scores())

    elif msg.startswith('!bingo add'):
        query = msg.split(" ")
        await message.channel.send(bingo.add(query[2]))

    elif msg.startswith('!bingo info'):
        query = msg.split(" ")
        await message.channel.send(bingo.info(query[2]))

    elif msg.startswith('!bingo remove'):
        query = msg.split(" ")
        await message.channel.send(bingo.remove(query[2]))

    elif msg.startswith('!bingo reset'):
        await message.channel.send(bingo.reset())

    elif bingo.bingo_words:
        for word in bingo.bingo_words:
            if word[0].lower() in map(lambda w: w.lower(), msg.split(" ")):
                await message.channel.send(bingo.cross(word[0]))

client.run(os.getenv('TOKEN'))