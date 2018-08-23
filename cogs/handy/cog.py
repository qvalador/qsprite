# -*- coding: utf-8 -*-

import discord
import sys
from .kmeans import get_colors

from conf import *
from discord.ext import commands

class Handy:
    """Useful functions that don't belong elsewhere."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def colors(self, ctx, user: discord.Member=None):
        """returns the hex code for a colour derived from the user's avatar."""
        if not user:
            user = ctx.message.author
        if user.avatar:
            avatar = 'https://discordapp.com/api/users/{0.id}/avatars/{0.avatar}.jpg'.format(user)
        else:
            avatar = user.default_avatar_url
            
        colors = get_colors(avatar)
        color = colors[0]
        response = '#{}{}{}'.format(hex(color[0])[2:], hex(color[1])[2:], hex(color[2])[2:])
        
        await self.bot.say(response)
        
    @commands.command()
    async def echo(self, channel: discord.Channel, *, arg):
        await self.bot.send_message(channel, arg)
        
    @commands.command(pass_context=True)
    async def avatar(self, ctx, member: discord.Member = None):
        """returns the given user's avatar."""
        if not member:
            member = ctx.message.author
        image_embed = discord.Embed(title="{}'s avatar".format(member.name))
        image_embed.set_image(url=member.avatar_url)
        await self.bot.say(embed=image_embed)

    @commands.command(pass_context=True)
    async def _______update(self, ctx):
        """updates the user log with all messages ever sent in any channel.  very time consuming."""
        return
        for channel in ctx.message.server.channels:
            async for msg in self.bot.logs_from(channel, limit=sys.maxsize):
                try:
                    if len(msg.content) < 2:
                        pass
                    elif msg.author.bot or msg.content[:2] in ['qq', 't!', ';;'] or msg.content[0] in ['!', '/', '`', '+', '?', '<', '+']:
                        pass
                    elif os.path.isfile(log_dir + msg.author.id + ".txt"):
                        with open(log_dir + msg.author.id + '.txt', 'a') as file:
                            file.write(msg.clean_content + '\n')
                    else:
                        with open(log_dir + msg.author.id + '.txt', 'w') as file:
                            file.write(msg.clean_content + '\n')
                except:
                    print('there was an exception, ignoring')
            print("done " + channel.name)
        print("done.")

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """boink."""
        msg = await self.bot.say("pong!")
        latency = int((msg.timestamp - ctx.message.timestamp).total_seconds() * 1000)
        await self.bot.edit_message(msg, new_content="pong! ({}ms)".format(str(latency)))

    @commands.command(pass_context=True)
    async def pong(self, ctx):
        """bink."""
        msg = await self.bot.say("ping!")
        latency = int((msg.timestamp - ctx.message.timestamp).total_seconds() * 1000)
        await self.bot.edit_message(msg, new_content="ping! ({}ms)".format(str(latency)))

def setup(bot):
    bot.add_cog(Handy(bot))