import discord
import async
from discord.ext import commands

class Game:
    """represents one mafia game.  corresponds to a server."""
    
    def __init__(self, bot):
        self.server = None
        self.bot = bot
        self.members = []
        self.town = []
        self.scum = []
        self.to_kill = []

    def get_member(self, target):
        """gets member by name.  returns None if none is found."""
        return self.server.get_member_named(target)

class Townie:
    """base class for mafia players."""
    
    def __init__(self, game):
        self.user = None
        self.game = game
        self.alignment = "town"
        self.alive = True
        self.targetted = False
        self.healed = False
        self.blocked = False
        self.night_target = None
        
    def action(self):
        """performs the player's night action.  in the case of vanilla townie, there is none."""
        pass
        
def Goon(Townie):
    """generic mafia goon."""
    def __init__(self, game):
        super(game)
        self.aligment = "scum"
        
    def action(self, target):
        """changes the kill target.  any scum, barring special circumstances, can change the target at any time during the night.  the player actually killed is the one that is last submitted."""
        member = self.game.get_member(target)
        if member:
            self.game.to_kill.append(member)
            await self.game.bot.say(embed=discord.Embed(title="Action Submitted", description="got it.  {} will be dead by morning.".format(member.display_name), colour=discord.Colour.green()))
        else:
            await self.game.bot.say(embed=discord.Embed(title="Failed", description="that user couldn't be found.", colour=discord.Colour.red()))
        
def Don(Goon):
    """the same as a goon, but investigates as town."""
    
    def __init__(self, game):
        super(game)
        self.alignment = "town"
        
def Doctor(Townie):
    """can heal a user."""
    
    def action(self, target):
        """heals the user, preventing them from dying overnight."""
        member = self.game.get_member(target)
        if member:
            self.game.members[member].healed = True
            await self.game.bot.say(embed=discord.Embed(title="Action Submitted", description="got it.  {} will be dead by morning.".format(member.display_name), colour=discord.Colour.green()))
        else:
            await self.game.bot.say(embed=discord.Embed(title="Failed", description="that user couldn't be found.", colour=discord.Colour.red()))