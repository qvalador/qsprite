#!/usr/bin/env python
# encoding: utf-8
# v2.0

from discord.ext import commands
import discord

import cogs.pokedex.lookup as dex
from fuzzywuzzy import fuzz, process

class Pokedex:
    """returns information about pokémon."""
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    async def dex(self, *, arg):
        shiny = False
        if arg.split()[0].lower() == "shiny":
            arg = arg.split(' ', 1)[1]
            shiny = True
        query = dex.lookup_thing(arg)
        if not query:
            await self.bot.say("Sorry, nothing was found.")
            return
        obj = query[0]
        objdict = dex.get_thing(obj)
        cases = {
                "pokemon": self.get_pokemon_embed,
                "move": self.get_move_embed,
                "item": self.get_item_embed,
                "ability": self.get_ability_embed,
                "nature": self.get_nature_embed
                }
        if shiny:
            embed = self.get_pokemon_embed(objdict, shiny=True)
        else:
            for item in cases:
                if objdict["table"] == item:
                    embed = cases[item](objdict)

        await self.bot.say(embed=embed)

    @dex.command()
    async def shiny(self, *, arg):
        print("nice.")

    def get_pokemon_embed(self, pokemon, shiny=False):
        if shiny:
            pokemon["sprite"] = pokemon["sprite"].split('/')
            pokemon["sprite"].insert(8, 'shiny')
            pokemon["sprite"] = '/'.join(pokemon["sprite"])
        stat_names = [str(item).ljust(8) for item in pokemon["stats"].keys()]
        stat_values = [str(item).ljust(8) for item in pokemon["stats"].values()]
        statheads = ['','']
        statbody = ['','']
        stats = ''
        for i in range(0, len(stat_names)):
            if i < 3:
                n = 0
            else:
                n = 1
            statheads[n] += stat_names[i]
            statbody[n] += stat_values[i]
        for i in range(0, len(statheads)):
            stats += statheads[i] + '\n'
            stats += statbody[i] + '\n'

        abilities = "`{}`".format("`/`".join(pokemon["abilities"]))
        if pokemon["hidden"]:
            abilities += " (*{}*)".format(pokemon["hidden"])
        return discord.Embed(
            title = "#{}, the {}".format(pokemon["id"], pokemon["species"]),
            description = '**Ability:** {}\n{}'.format(abilities, pokemon["flavor"]),
            color = pokemon["color"]
        ).set_author(name=pokemon["name"], url=pokemon["link"], icon_url=pokemon["party"]
        ).set_thumbnail(url=pokemon["sprite"]
        ).add_field(name="Stats", value="```coffeescript\n{}```".format(stats)
        ).set_footer(text="Click the Pokémon name for more information.")

    def get_move_embed(self, move):
        return discord.Embed(
            title = "{}-type\t[`{}`]".format(move["type"], move["damage class"].title()),
            description = move["effect"],
            color = move["color"]
        ).set_author(
            name = move["name"], url = move["link"], icon_url = move["sprite"]
            ).add_field(name="Power", value=move["power"],inline=True
            ).add_field(name="PP", value=move["pp"], inline=True
            ).add_field(name="Accuracy", value=move["accuracy"], inline=True
            ).set_footer(text="Click the move name for more information.")

    def get_item_embed(self, item):
        return discord.Embed(
            title = '',
            description = item["effect"],
            color = item["color"]
        ).set_author(name=item["name"], icon_url=item["sprite"], url=item["link"]
        ).set_footer(text = "Click the item name for more information.")

    def get_ability_embed(self, ability):
        return discord.Embed(
            title = '',
            description = ability["effect"]
        ).set_author(name=ability["name"], url=ability["link"]
        ).set_footer(text = "Click the ability name for more information.")

    def get_nature_embed(self, nature):
        return discord.Embed(
            title = '',
            description = '',
        ).add_field(name="Increases", value=nature["up"], inline=True
        ).add_field(name="Decreases", value=nature["down"], inline=True
        ).set_author(name=nature["name"], url=nature["link"]
        ).set_footer(text = "Click the nature name for more information.")
        
def setup(bot):
    bot.add_cog(Pokedex(bot))