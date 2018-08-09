from conf import log_dir
from discord.ext import commands

import random as rng
import discord
import markovify
import os
import codecs

class RNG:
    """Utilities that provide pseudo-RNG."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def random(self, ctx):
        """displays a random thing you request."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("hey, {}!  you didn't pass a subcommand.".format(ctx.message.author.display_name))

    @random.command()
    async def lenny(self):
        """Displays a random lenny face."""
        lenny = rng.choice([
            "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)",
            "( ͡o ͜ʖ ͡o)", "͡(° ͜ʖ ͡ -)", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "(ง ͠° ͟ل͜ ͡°)ง",
            "ヽ༼ຈل͜ຈ༽ﾉ"
        ])
        await self.bot.say(lenny)

    @commands.command()
    async def choose(self, *choices):
        """chooses between multiple choices.
        to denote multiple choices, you should use double quotes.
        """
        if len(choices) < 2:
            await self.bot.say('not enough choices to pick from.')
        else:
            await self.bot.say(rng.choice(choices))
            
    @commands.command()
    async def roll(self, dice : str):
        """rolls a dice in NdN format."""
        try:
            rolls, limit = dice.split('d')
            if rolls == '':
                rolls = '1'
            rolls = int(rolls)
            limit = int(limit)
        except Exception:
            await self.bot.say('format has to be in NdN!')
            return

        randlist = [str(rng.randint(1, limit)) for r in range(rolls)]
        result = '🎲 ' + ', '.join(randlist)
        if rolls > 1:
            result_sum = " → **{}**".format(sum([int(i) for i in randlist]))
        else:
            result_sum = ''
        await self.bot.say(result + result_sum)
            
    @commands.command()
    async def be(self, user: discord.Member, other: discord.Member=None):
        """generates a markov chain based on the specified user's logs."""
        log_path = log_dir + user.id + '.txt'
        if os.path.exists(log_path):
            with codecs.open(log_path, "r",encoding='utf-8', errors='ignore') as f:
                text = filter(None, (line.rstrip() for line in f))
                #text = lines.read()
                text_model = markovify.NewlineText(text)
                name = user.display_name
                colour = user.colour
                if other:
                    with open(log_dir + other.id + '.txt') as s:
                        other_text = s.read()
                        other_model = markovify.NewlineText(other_text)
                        text_model = markovify.combine([text_model, other_model])
                        name += " + " + other.display_name
                        colour = discord.Colour((user.colour.value + other.colour.value) / 2)
                sentence = text_model.make_sentence(tries=100)
            embed = discord.Embed(title='', colour=colour, description=sentence)
            embed.set_author(name=name, icon_url=user.avatar_url)
            await self.bot.say(embed=embed)
        else:
            await self.bot.say("i don't have any messages logged from that user yet.")

def setup(bot):
    bot.add_cog(RNG(bot))