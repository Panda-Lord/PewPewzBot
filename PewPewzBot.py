import discord
import os
import bottasks
import db
from random import choice
from configparser import RawConfigParser
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(verbose=True)
env_path = Path('.') / '.env'
config = RawConfigParser()
config.read('pewzbot.cfg')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.type == discord.MessageType.new_member:
        emojis = ["\U0001F44B", "\U0001F973", "\U0000270C", "\U0001F4AA", "\U0001F386", "\U0001F389"]
        await message.add_reaction(choice(emojis))
        return

    if message.author.bot:
        return

    msg = message.content
    bingo_status = config.getboolean('Main', 'bingo')

    if config.getboolean('Main', 'bingo'):
        bingo = bottasks.Bingo()
        if msg.startswith('!bingo score'):
            await message.channel.send(bingo.scores())
            return

        elif msg.startswith('!bingo add') and message.author.guild_permissions.administrator:
            query = msg.split(" ")
            await message.channel.send(bingo.add(query[2]))
            return

        elif msg.startswith('!bingo info'):
            query = msg.split(" ")
            await message.channel.send(bingo.info(query[2]))
            return

        elif msg.startswith('!bingo remove') and message.author.guild_permissions.administrator:
            query = msg.split(" ")
            await message.channel.send(bingo.remove(query[2]))
            return

        elif msg.startswith('!bingo reset') and message.author.guild_permissions.administrator:
            await message.channel.send(bingo.reset())
            return

        elif bingo.bingo_words:
            for word in bingo.bingo_words:
                if word[0].lower() in map(lambda w: w.lower(), msg.split(" ")):
                    await message.channel.send(bingo.cross(word[0]))
                    return

    if not msg.startswith('!'):
        return

    if msg.startswith('!pewpewz admin') and message.author.guild_permissions.administrator:
        help = [
                'PewPewzBot is here to help!',
                '!bingo enable/disable - enables/disables bingo game',
        ]
        if bingo_status:
                help.extend([
                    '!bingo add word - Adds "word" to bingo game',
                    '!bingo remove word - Removes "word" from the game',
                    '!bingo reset - Reset the bingo game, but not the words'
            ])
        await message.channel.send("\n".join(help))
        return

    if msg.startswith('!pewpewz'):
        help = [
                '`PewPewzBot` is here to help!',
                '`!stock GME` - Stock prices, GME = GameStop for example',
                '`!price BTC USD` - Currency exchange, BTC = BitCoin for example. Second currency optional, default to USD',
                '`!cryptochickz` - Get a random CryptoChick info. Add number parameter for specicif chick (`!cryptochickz #1`)',
                '`!pixelplanet` - Get a random pixel planet info. Add name parameter for specici planet (`!pixelplanet Earth`)',
                '`!depicted` - Get random depicted poster. !depicted colour for coloured version. Add name parameter for specici planet (`!depicted bread` or `!depicted colour bread`)',
        ]
        if bingo_status:
                help.extend([
                    '!bingo score - Current bingo scores',
                    '!bingo info word - Gives info on "word"',
            ])
        await message.channel.send("\n".join(help))
        return

    if message.content.startswith('!cryptochickz'):
        query = msg.split(" ")
        if len(query) > 1:
            chick = bottasks.crypto_chickz(query[1].replace('#', ''))
        else:
            chick = bottasks.crypto_chickz()
        if chick:
            embedVar = discord.Embed(title=f'CryptoChickz {chick["name"]}', description=chick["content"], color=chick["color"], url=chick["url"])
            embedVar.add_field(name="Breed", value=chick["breed"], inline=True)
            if chick['accesory']:
                embedVar.add_field(name="Accesory", value=chick["accesory"], inline=True)
            embedVar.set_image(url=chick["image"])
            if chick["owner"]:
                embedVar.set_author(name=chick["owner"], url=chick["owner_url"], icon_url=chick["owner_icon"])
            await message.channel.send(embed=embedVar)
            return
        else:
            await message.channel.send("Doesn't seem to be a CryptoChickz number. Try again babes!")
            return

    if message.content.startswith('!pixelplanet'):
        query = msg.split(" ")
        if len(query) > 1:
            planet = bottasks.pixel_planet(query[1])
        else:
            planet = bottasks.pixel_planet()
        if planet:
            embedVar = discord.Embed(title=f'{planet["name"]}{" "*1}{planet["number"]}', description=planet["content"], color=planet["rarity"], url=planet["url"])
            embedVar.add_field(name="Population", value=planet["population"], inline=True)
            embedVar.add_field(name="Temperature", value=planet["temperature"], inline=True)
            embedVar.set_image(url=planet["url"]+'.gif')
            if planet["owner"]:
                embedVar.set_author(name=planet["owner"], url=planet["owner_url"], icon_url=planet["owner_icon"])
            await message.channel.send(embed=embedVar)
            return
        else:
            await message.channel.send("Doesn't seem to be a Pixel Planet. Try again babes!")
            return

    if message.content.startswith('!depicted'):
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
        if depict:
            if colour:
                image, color = depict['color']
            else:
                image, color = depict['black']
            depicted_url = depict['http'] + depict['site']
            embedVar = discord.Embed(title=depict['depict'], color=color, url= depicted_url + depict['depict'])
            embedVar.set_image(url=depicted_url + image)
            embedVar.set_footer(text=depict['site'] + depict['depict'])
            await message.channel.send(embed=embedVar)
            return
        else:
            await message.channel.send("Don't think we have this one yet. Try again babes!")
            return

    if msg.startswith('!stock'):
        query = msg.split(" ")
        response = bottasks.Finance(query[1]).quote_stock()
        await message.channel.send(response)
        return

    if msg.startswith('!price'):
        query = msg.split(" ")
        if len(query) == 2:
            query.append('USD')
        await message.channel.send(bottasks.Finance(query[1], query[2]).quote_price())
        return

    if msg.startswith('!bingo disable') and message.author.guild_permissions.administrator:
        if bingo_status:
            config.set('Main', 'bingo', 'false')
            with open('pewzbot.cfg', 'w') as configfile:
                config.write(configfile)
            await message.channel.send('!Bingo disabled')
            return
        else:
            await message.channel.send('!Bingo already disabled')
            return

    if msg.startswith('!bingo enable') and message.author.guild_permissions.administrator:
        if not bingo_status:
            config.set('Main', 'bingo', 'true')
            with open('pewzbot.cfg', 'w') as configfile:
                config.write(configfile)
            await message.channel.send('!Bingo enabled')
            return
        else:
            await message.channel.send('!Bingo already enabled')
            return

if __name__ == '__main__':
    db.db_test()
    client.run(os.getenv('TOKEN'))
