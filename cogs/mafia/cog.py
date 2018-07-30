import discord
from discord.ext import commands
        
class Mafia:
    """hosts games of mafia, aka werewolf.  note: requires lots of server permissions."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def mafia(self, ctx):
        """command container for mafia functions"""
        if ctx.invoked_subcommand is None:
            await self.bot.say(embed=discord.Embed(title="Failed", description="this command doesn't do anything on its own.  use a subcommand.", colour=discord.Colour.red()))

def setup(bot):
    bot.add_cog(Mafia(bot))