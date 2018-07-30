#!/usr/bin/env python
# encoding: utf-8
# v2.0

from discord.ext import commands
import discord
import urllib
import requests
import json
import cogs.pokedex.lookup as dex
from fuzzywuzzy import fuzz, process

class Pokedex:
    """returns information about pokémon."""
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(invoke_without_command=True)
    async def dex(self, *, arg):
        """indexes the database for the closest pokémon match and provides some flavour.  subcommands handle similar events, but with other subjects, such as items."""
        
        flavour = dex.pokemon_basic(arg)
        
        stat_summary = "{}/{}/{}/{}/{}/{}".format(flavour['stats']['hp'], flavour['stats']['attack'], flavour['stats']['defence'], flavour['stats']['special attack'], flavour['stats']['special defence'], flavour['stats']['speed'])
        
        description = flavour['infobit'] + '\n' + stat_summary + '\n\n' + flavour['description']
        
        pokemon_embed = discord.Embed(title=flavour["name"], colour=flavour['colour'], url = 'http://veekun.com/dex/items/{}'.format(urllib.parse.quote(flavour['name'].lower())), description=description)
        
        pokemon_embed.set_thumbnail(url=flavour["sprite"])
        
        await self.bot.say(embed=pokemon_embed)
        
    @dex.command()
    async def item(self, *, arg):
        """indexes the database for the closest item match and provides some flavour."""
   
        flavour = dex.item_basic(arg)
        
        item_embed = discord.Embed(title=flavour['name'], description=flavour['description'], url = 'http://veekun.com/dex/items/{}'.format(urllib.parse.quote(flavour['name'].lower())))
       
        item_embed.set_thumbnail(url=flavour['sprite'])
        
        await self.bot.say(embed=item_embed)
        
    @dex.command()
    async def ability(self, *, arg):
        """indexes the database for the closest ability match and provides some flavour."""
        
        flavour = dex.ability_basic(arg)
        
        name = flavour['name']
        description = flavour['description']
        
        ability_embed = discord.Embed(title=name, description=description, url='http://veekun.com/dex/ability/{}'.format(urllib.parse.quote(flavour['name'])))
        
        await self.bot.say(embed=ability_embed)
        
    @dex.command()
    async def move(self, *, arg):
        """indexes the database for the closest move match and provides some flavour."""
        
        flavour = dex.move_basic(arg)
        
        description = "type: {} / power: {} / accuracy: {}".format(flavour['type'], flavour['power'], flavour['accuracy'])
        
        move_embed = discord.Embed(title=flavour['name'], description=description, colour=flavour['colour'], url='http://veekun.com/dex/moves/{}'.format(urllib.parse.quote(flavour['name'].lower())))
        move_embed.set_footer(text=flavour['description'])
        
        await self.bot.say(embed=move_embed)
        
def setup(bot):
    bot.add_cog(Pokedex(bot))