import discord
import os
import bottasks
from dotenv import load_dotenv
load_dotenv(verbose=True)
from pathlib import Path
env_path = Path('.') / '.env'

client = discord.Client()

bingo_words = [
    "DeFi",
    "Decentralised",
    "Habitat",
    "DAO",
    "Etherum"
]

scored_words = []

score = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith('!stock'):
        msg = msg.split(" ")
        price = bottasks.Stock(msg[1]).quote()['05. price']
        await message.channel.send(f'Price for {msg[1].upper()} is {price}!')

    if msg.startswith('!bingo score'):
        scores = bottasks.Bingo(bingo_words, scored_words, score).scores()
        await message.channel.send(scores)

    elif msg.startswith('!bingo'):
        await message.channel.send('Bingo!')

    for word in bingo_words:
        if word.lower() in map(lambda w: w.lower(), msg.split(" ")):
            if word in scored_words:
                await message.channel.send(f'Bingo! You already had "{word}" though.')
            else:
                cross = bottasks.Bingo(bingo_words, scored_words, score).cross(word)
                scored_words.append(word)
                await message.channel.send(cross)

client.run(os.getenv('TOKEN'))