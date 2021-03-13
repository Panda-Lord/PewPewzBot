import discord
import os
import bottasks
import db
from dotenv import load_dotenv
load_dotenv(verbose=True)
from pathlib import Path
env_path = Path('.') / '.env'

client = discord.Client()
db.db_test()

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
                '!stock GME - Stock prices, GME = GameStop for example',
                '!price BTC USD - Currency exchange, BTC = BitCoin for example. Second currency optional, default to USD',
                '!pixelplanet - Get a random pixel planet. WHy not?'
                '!bingo score - Current bingo scores',
                '!bingo add word - Adds "word" to bingo game',
                '!bingo info word - Gives info on "word"',
                '!bingo remove word - Removes "word" from the game'
        ]
        await message.channel.send("\n".join(help))

    if message.content.startswith('!pixelplanet'):
        planet = bottasks.random_pixel_planet()
        embedVar = discord.Embed(title=f'{planet[1]}{" "*5}{planet[0]}', description=planet[3], color=planet[6], url=planet[2])
        embedVar.add_field(name="Pupulation", value=planet[4], inline=True)
        embedVar.add_field(name="Temperature", value=planet[5], inline=True)
        embedVar.set_image(url=planet[2]+'.gif')
        await message.channel.send(embed=embedVar)

    if msg.startswith('!stock'):
        query = msg.split(" ")
        response = bottasks.Finance(query[1]).quote_stock()
        await message.channel.send(response)

    elif msg.startswith('!price'):
        query = msg.split(" ")
        if len(query) == 2:
            query.append('USD')
        await message.channel.send(bottasks.Finance(query[1], query[2]).quote_price())

    elif msg.startswith('!bingo score'):
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