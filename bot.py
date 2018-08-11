import discord
import asyncio
import os

from discord.ext import commands
from conf import *

description = """yet another niche, general(?)-purpose discord bot for qvalador.  hey, how'd you find this description, anyway?"""

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('qq '), description=description)

VERSION = "1.0.0"


def update_avatar(filename):
    """updates the avatar to the provided file name."""
    if os.path.isfile(filename):
        with open(filename, "rb") as avatar:
            bot.edit_profile(avatar=avatar.read())


def load_cogs():
    for subdir in next(os.walk(cog_dir))[1]:
        try:
            bot.load_extension("cogs.{}.cog".format(subdir))
            print("loaded plugin: {}".format(subdir))
        except Exception as error:
            exception = "{0}: {1}".format(type(error).__name__, error)
            print("Failed to load {}: {}".format(subdir, exception))


@bot.event
async def on_ready():
    print("connected!")
    print("username: " + bot.user.name)
    print("id: " + bot.user.id)
    update_avatar("avatar.png")
    load_cogs()


@bot.event
async def on_message_edit(old, new):
    await bot.process_commands(new)


@bot.event
async def on_message(msg):
    await bot.process_commands(msg)
    if msg.author.bot or msg.content[:2] not in ['qq', 't!', ';;'] and msg.content[0] not in ['!', '/', '`', '+']:
        return
    elif os.path.isfile(log_dir + msg.author.id + ".txt"):
        with open(log_dir + msg.author.id + '.txt', 'a') as file:
            file.write(msg.clean_content + '\n')
    else:
        with open(log_dir + msg.author.id + '.txt', 'w') as file:
            file.write(msg.clean_content + '\n')


@bot.command()
async def quit():
    """bye!"""
    await bot.say("goodbye to oz, and everything i love.")
    os._exit(0)


@bot.command(pass_context=True)
async def reload(ctx, cogname):
    cog = "cogs." + cogname + ".cog"
    try:
        bot.unload_extension(cog)
        bot.load_extension(cog)
        print('reloaded {}'.format(cogname))
        await bot.say('reloaded {}.'.format(cogname))
    except Exception as e:
        await bot.add_reaction(ctx.message, "🚫")
        await bot.say('{}: {}'.format(type(e).__name__, e))

@bot.command()
async def info():
    """provides basic information about the bot."""
    await bot.say("""**scout, version {}**
hi, i'm a niche, multi-purpose discord bot written in discord.py by qvalador.  try {} help for information on my commands."""
                  .format(VERSION, u'\U00002699'))

try:
    bot.run(token)
except OSError:
    os._exit(0)
