# -*- coding: utf-8 -*-
import discord
import pickle
import csv

from conf import *
from discord.ext import commands

class Profile:
    """represents a user profile."""
    def __init__(self, user):
        self.user = user
        self.name = user.display_name
        self.id = user.id
        self.level = None
        self.xp = 0
        
    def embed(self):
        """returns an embed with the user's information."""
        emb = discord.Embed(title=self.level, description="xp: " + str(self.xp), color=self.user.color)
        emb.set_author(name=self.user.display_name, icon_url=self.user.avatar_url)
        return emb

class Market:
    """Discord, but now it has capitalism."""
    def __init__(self, bot):
        self.bot = bot
        self.profile_dir = "./cogs/market/profiles.pickle"
        self.users = {}
        self.users = pickle.load(open(self.profile_dir, "rb"))
        self.levels = {}
        with open("./cogs/market/levels.csv", mode="r") as file:
            reader = csv.reader(file)
            self.levels = {int(row[1]): row[0] for row in reader} # {price: level name, ...}
        
    def save(self):
        pickle.dump(self.users, open(self.profile_dir, "wb"))
        
    @commands.group(pass_context=True, invoke_without_command=True)
    async def profile(self, ctx, user:discord.Member=None):
        """container function for profile commands.  returns the user's profile if no subcommand is invoked."""
        if not user:
            user = ctx.message.author # default to author if no user is specified
        try:
            await self.bot.say(embed=self.users[user.id].embed())
        except KeyError:
            await self.bot.add_reaction(ctx.message, "\U0001F6AB") # no entry sign emoji
            await self.bot.say("you need to have a profile for that.")
            
    @profile.command(pass_context=True)
    async def xp(self, ctx, user:discord.Member, num):
        """sets the xp of <user> to <num>.  don't play with this kids."""
        if ctx.message.author.id != "117662741413625859": # check if it's me
            await self.bot.add_reaction(ctx.message, "\U0001F6AB") # no entry sign emoji
            await self.bot.say("you're not cool enough for that.")
        else:
            num = int(num)
            self.users[user.id].xp = num
        
    async def register(self, user):
        """creates a profile for the user."""
        self.users[user.id] = Profile(user)
        
    async def on_message(self, msg):
        if msg.author.id not in self.users:
            await self.register(msg.author)
        # a lot of checks. ensures the message is long enough,
        # is not a bot command, and is not from another bot.
        elif len(msg.content) > 2 and msg.content[:2] not in ["qq", "t!"] and msg.content[0] not in ["!", "<", "/", "+"] and not msg.author.bot: #bot command prefixes
            self.users[msg.author.id].xp += 1
            if self.users[msg.author.id].xp in self.levels:
                await self.bot.add_reaction(msg, "\U0001F389") # party popper emoji
                await self.bot.send_message(msg.channel, "Congratulations, {}!  You've acquired the rank of **{}**!".format(msg.author.mention, self.levels[self.users[msg.author.id].xp]))
                self.users[msg.author.id].level = self.levels[self.users[msg.author.id].xp]
        self.save()

def setup(bot):
    bot.add_cog(Market(bot))