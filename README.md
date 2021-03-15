# PewPewzBot
Discord bot I have made for our small server. 
The bot saves some data on postgresSQL. It is currently set up to accomodate one server for the database.

It is able to do below as of 15.03.21:

## General commands & use

* `!help` - Shows list of commands
* `!stock GME` - Stock prices, GME = GameStop for example
* `!price BTC USD` - Currency exchange, BTC = BitCoin for example. Second currency optional, default is USD'
* `!pixelplanet` - Scrapes and sends random pixel planet from https://www.mypixelplanet.com/
* `!pixelplanet planet_name` - scraps a specific planet.
* `!depicted` - Scrapes and sends random word poster from https://www.thedepicted.com/. Try `!depicted colour` for coloured version
* `!depicted word` - scraps a specific word. Try `!depicted colour word` for coloured version.
* `!bingo score` - Current bingo scores
* `!bingo info word` - Gives info on "word"
* bingo game checks over the messages looking for added keywords and crosses them off in the process. Game reset on completion.

## Admin commands

* `!admin help` - Shows list of admin commands
* `!bingo enable/disable` - enables/disables bingo game. This will also hide unusuable !bingo commands
* `!bingo add word` - Adds "word" to bingo game
* `!bingo remove word` - Removes "word" from the game
* `!bingo reset` - Reset the bingo game, but not the words