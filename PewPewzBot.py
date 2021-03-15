import discord
import os
import bottasks
import db
from configparser import RawConfigParser
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(verbose=True)
env_path = Path('.') / '.env'
config = RawConfigParser()
config.read('pewzbot.cfg')
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content
    bingo_status = config.getboolean('Main', 'bingo')

    if msg.startswith('!help admin') and message.author.guild_permissions.administrator:
        help = [
                'PewPewzBot is here to help!',
                '!bingo enable/disable - enables/disables bingo game',
        ]
        await message.channel.send("\n".join(help))

    elif msg.startswith('!help'):
        help = [
                'PewPewzBot is here to help!',
                '!stock GME - Stock prices, GME = GameStop for example',
                '!price BTC USD - Currency exchange, BTC = BitCoin for example. Second currency optional, default to USD',
                '!pixelplanet - Get a random pixel planet info',
                '!pixelplanet Earth - Get info on earth. Replace Earth with any other My Pixel Planet name.',
                '!depicted - Get random depicted poster. !depicted colour for coloured version',
                '!depicted bread - Get depicted poster for bread. !depicted colour bread for coloured version',
        ]
        if bingo_status:
                help.append([
                    '!bingo score - Current bingo scores',
                    '!bingo add word - Adds "word" to bingo game',
                    '!bingo info word - Gives info on "word"',
                    '!bingo remove word - Removes "word" from the game'
            ])
        await message.channel.send("\n".join(help))

    elif message.content.startswith('!pixelplanet'):
        query = msg.split(" ")
        if len(query) > 1:
            planet = bottasks.pixel_planet(query[1])
        else:
            planet = bottasks.pixel_planet()
        if planet:
            embedVar = discord.Embed(title=f'{planet["name"]}{" "*5}{planet["number"]}', description=planet["content"], color=planet["rarity"], url=planet["url"])
            embedVar.add_field(name="Pupulation", value=planet["population"], inline=True)
            embedVar.add_field(name="Temperature", value=planet["temperature"], inline=True)
            embedVar.set_image(url=planet["url"]+'.gif')
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("Doesn't seem to be a Pixel Planet. try again babes!")      

    elif message.content.startswith('!depicted'):
        query = msg.split(" ")
        colour = False
        if len(query) > 2 and query[1] in ('color', 'colour'):
            depict = bottasks.depicted(query[2])
            colour = True
        elif len(query) > 1 and query[1] in ('color', 'colour'):
            depict = bottasks.depicted()
            colour = True
        elif len(query) > 1:
            depict = bottasks.depicted(query[1])
        else:
            depict = bottasks.depicted()
        if colour:
            image, color = depict['color']
        else:
            image, color = depict['black']
        depicted_url = depict['http'] + depict['site']
        embedVar = discord.Embed(title=depict['depict'], color=color, url= depicted_url + depict['depict'])
        embedVar.set_image(url=depicted_url + image)
        embedVar.set_footer(text=depict['site'] + depict['depict'])
        await message.channel.send(embed=embedVar)

    elif msg.startswith('!stock'):
        query = msg.split(" ")
        response = bottasks.Finance(query[1]).quote_stock()
        await message.channel.send(response)

    elif msg.startswith('!price'):
        query = msg.split(" ")
        if len(query) == 2:
            query.append('USD')
        await message.channel.send(bottasks.Finance(query[1], query[2]).quote_price())

    elif msg.startswith('!bingo disable') and message.author.guild_permissions.administrator:
        if bingo_status:
            config.set('Main', 'bingo', 'false')
            with open('pewzbot.cfg', 'w') as configfile:
                config.write(configfile)
            await message.channel.send('!Bingo disabled')
        else:
            await message.channel.send('!Bingo already disabled')

    elif msg.startswith('!bingo enable') and message.author.guild_permissions.administrator:
        if not bingo_status:
            config.set('Main', 'bingo', 'true')
            with open('pewzbot.cfg', 'w') as configfile:
                config.write(configfile)
            await message.channel.send('!Bingo enabled')
        else:
            await message.channel.send('!Bingo already enabled')

    elif config.getboolean('Main', 'bingo'):
        bingo = bottasks.Bingo()
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

if __name__ == '__main__':
    db.db_test()
    client.run(os.getenv('TOKEN'))
