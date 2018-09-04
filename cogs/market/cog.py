# -*- coding: utf-8 -*-
import discord
import csv
import os
import dbhandler

from discord.ext import commands

class Market:
    """Discord, but now it has capitalism."""
    def __init__(self, bot):
        self.bot = bot
        self.levels = {}
        with open("./cogs/market/levels.csv", mode="r") as file:
            reader = csv.reader(file)
            self.levels = {int(row[1]): row[0] for row in reader} # {price: level name, ...}
        self.handler = dbhandler.DbHandler()

    @commands.group(pass_context=True)
    async def profile(self, ctx, usr: discord.Member = None):
        if not usr:
            usr = ctx.message.author # default to sender if no user provided
        info = self.handler.profile_information(usr.id)
        emb = discord.Embed(title=info["level"], description="xp: " + str(info["xp"]), color=usr.color)
        emb.set_author(name=usr.display_name, icon_url=usr.avatar_url)
        await self.bot.say(embed=emb)

    async def on_message(self, msg):
        if not self.handler.exists(msg.author.id):
            self.handler.register(msg.author.id) # register in db if not already registered
            print("registered {} (id:{})".format(msg.author.display_name, msg.author.id))
        else:
            # make sure the message has substance and isn't a bot command
            if len(msg.content) < 2 or msg.content[:2] in ["qq", "t!"] or msg.content[0] in ["!", "<", "/", "+"] or not msg.server or msg.author.bot:
                return
            self.handler.update_xp(msg.author.id, 1) # increments xp by one
            usr_xp = self.handler.profile_information(msg.author.id)["xp"]
            if usr_xp in self.levels: # check if we've reached a level-up point
                self.handler.update_level(msg.author.id, self.levels[usr_xp])
                await self.bot.add_reaction(msg, "🎉")
                await self.bot.send_message(msg.channel, "Congratulations, {}!  You've acquired the rank of **{}**!".format(msg.author.mention, self.levels[usr_xp]))

def setup(bot):
    bot.add_cog(Market(bot))