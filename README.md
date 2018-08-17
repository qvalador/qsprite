# *qsprite*
#### A Discord bot written with Rapptz's [discord.py](https://github.com/Rapptz/discord.py).
Qsprite is the most recent of many discord bots i've run through.  This one is a bit more general purpose, so perhaps you'll find him useful.

## Installation

### Download
 - Using git: `git clone https://github.com/Qvalador/scout.git`
 - Direct download: `https://github.com/Qvalador/scout/archive/master.zip`

### Requisites
 - [Python 3](https://www.python.org/downloads/), specifically developed and tested in Python 3.6
 - [discord.py](https://github.com/Rapptz/discord.py)
 - [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) for fuzzy string searching in the pokédex cog
 - [markovify](https://github.com/jsvine/markovify) for Markov chain generation in the impersionation command (i.e. `qq be`)
 - [NumPy](https://www.numpy.org/), for color analysis in the role-color-grabber command

 
I have not included `conf.py` because it contains sensitive, user-specific information. Don't forget to rename [conf.py.example](./conf.py.example) and update with your relevant information, or the bot will not run.
 
### Configure and launch the bot:

Your bot will need a token (stored in `conf.py`) to run.  You can get a token through [Discord's Applications interface](https://discordapp.com/developers/applications/), which requires amount of set-up.
 
Once that's complete, you can launch with `python main.py` or `python3 main.py` in your terminal.  `run.py` automatically reboots the bot if it's shut down for whatever reason, particularly lapses in connectivity; if you'd rather have it stay dead upon downage, just run `bot.py` instead.

The `Market` cog awards points for chat activity, and levels users up once they reach a certain threshold.  Currently the level titles are taken from [John Egbert's Echeladder](https://vignette.wikia.nocookie.net/mspaintadventures/images/2/2e/EcheladderTopRing.gif/revision/latest?cb=20180204222709), with some minor modifications, as the bot as-is is mostly employed in Homestuck servers.  However, you may wish to change these level titles to something more relevant to your server.  You can change them (and the thresholds required to ascertain them) by modifying [levels.csv](./cogs/market/levels.csv) accordingly.

## Known Issues
- The TCG cog will always fail to load, notably because it's pretty much empty and i don't really have plans to go forward with it at this time.  If it bothers you, feel free to remove it, but it shouldn't actually affect functionality.

## Contact
If you have any questions or concerns, feel free to post an issue or ping me on discord at `kacklord#0046`.