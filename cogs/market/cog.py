# -*- coding: utf-8 -*-
import discord
import pickle
import csv
import os
import sqlite3

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
        self.levels = {}
        with open("./cogs/market/levels.csv", mode="r") as file:
            reader = csv.reader(file)
            self.levels = {int(row[1]): row[0] for row in reader} # {price: level name, ...}
        self.connection = sqlite3.connect("./cogs/market/profiles.db")
        self.cur = self.connection.cursor()

    @commands.group(pass_context=True)
    async def profile(self, ctx, usr: discord.Member = None):
        if not usr:
            usr = ctx.message.author
        sql_command = "SELECT * FROM profiles WHERE id = ?"
        result = self.cur.execute(sql_command, (usr.id,)).fetchone()
        emb = discord.Embed(title=result[1], description="xp: " + str(result[2]), color=usr.color)
        emb.set_author(name=usr.display_name, icon_url=usr.avatar_url)
        await self.bot.say(embed=emb)

    @commands.command()
    async def reset(self):
        self.cur.execute("DROP TABLE profiles;")
        sql_command = """
                        CREATE TABLE profiles (
                        id INTEGER,
                        level TEXT,
                        xp INTEGER,
                        PRIMARY KEY (id)
                        );"""
        self.cur.execute(sql_command)

    def register(self, usr):
        sql_command = """INSERT INTO profiles (id, xp, level) VALUES (?,?,?);"""
        self.cur.execute(sql_command, (usr.id, 0, "None"))
        self.connection.commit() # !! https://stackoverflow.com/questions/18393763/sqlite-not-saving-data-between-uses

    @commands.command(pass_context=True)
    async def me(self, ctx):
        sql_command = "SELECT * FROM profiles"
        self.cur.execute(sql_command)
        await self.bot.say(self.cur.fetchall())

    async def on_message(self, msg):
        exists = self.cur.execute("SELECT EXISTS(SELECT 1 FROM profiles WHERE id=?);", (msg.author.id,)).fetchone()
        if not exists[0]:
            self.register(msg.author)
            print("registered " + msg.author.display_name)
        else:
            #"UPDATE employee SET xp=99 WHERE name='karkat'"
            if len(msg.content) > 2 and msg.content[:2] not in ["qq", "t!"] and msg.content[0] not in ["!", "<", "/", "+"] and not msg.author.bot:
                sql_command = "UPDATE profiles SET xp = xp + 1 WHERE id = ?"
                self.cur.execute(sql_command, (msg.author.id,))
                self.connection.commit()
            sql_command = "SELECT xp FROM profiles WHERE id = ?"
            usr_xp = self.cur.execute(sql_command, (msg.author.id,)).fetchone()[0]
            if usr_xp in self.levels:
                await self.bot.add_reaction(msg, "🎉")
                await self.bot.send_message(msg.channel, "Congratulations, {}!  You've acquired the rank of **{}**!".format(msg.author.mention, self.levels[usr_xp]))
                sql_command = "UPDATE profiles SET level = ? WHERE id = ?"
                self.cur.execute(sql_command, (self.levels[usr_xp], msg.author.id))
                self.connection.commit()



def setup(bot):
    bot.add_cog(Market(bot))