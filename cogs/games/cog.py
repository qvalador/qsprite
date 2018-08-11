# -*- coding: utf-8 -*-
import discord
import dbhandler
from collections import namedtuple
import random as rng

from discord.ext import commands
from os import listdir

class Connect4:

    def __init__(self):
        self.players = {}
        self.turn = None
        self.next = None
        self.colors = ['🔴', '🍊', '🍋', '🍈', '🔵', '😈', '🍑', '⚫', '🌎', '🌖', '🎱'] # imp emoji is purple on discord
        self.header = [['```', '', '', '', '', '```'], ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣"]]
        self.board = [
            ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
            ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
            ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
            ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
            ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
            ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"]
        ]

    def add_player(self, player):
        if len(self.players) == 2:
            return # two players only
        elif len(self.players) == 1:
            self.header[0][2] = "vs."
            self.header[0][3] = player + '\n'
            self.next = player
            self.header[0][4] = "({}'s turn)".format(self.turn)
        else:
            self.header[0][1] = player
            self.turn = player
        self.players[player] = rng.choice(self.colors)
        self.colors.remove(self.players[player]) # remove the new player's color from the pool

    def check_win(self):
        """checks for a chain of four of the same piece on the board."""
        # Credit to Keveloper for the win check algorithm
        # Check rows for winner
        for row in range(6):
            for col in range(4):
                if self.board[row][col]==self.board[row][col+1]==self.board[row][col+2] ==self.board[row][col+3] and self.board[row][col]!="⬜":
                    if self.board[row][col] == self.players[self.turn]:
                        winner = self.turn
                    else:
                        winner = self.next
                    self.header[0][4] = "({} wins!)".format(winner)
                    return winner
        # Check columns for winner
        for col in range(7):
            for row in range(3):
                if self.board[row][col]==self.board[row+1][col]==self.board[row+2][col]==self.board[row+3][col] and self.board[row][col]!="⬜":
                    if self.board[row][col] == self.players[self.turn]:
                        winner = self.turn
                    else:
                        winner = self.next
                    self.header[0][4] = "({} wins!)".format(winner)
                    return winner
        # Check diagonal (top-left to bottom-right) for winner
        for row in range(3):
            for col in range(4):
                if self.board[row][col]==self.board[row+1][col+1]==self.board[row+2][col+2]==self.board[row+3][col+3] and self.board[row][col]!="⬜":
                    if self.board[row][col] == self.players[self.turn]:
                        winner = self.turn
                    else:
                        winner = self.next
                    self.header[0][4] = "({} wins!)".format(winner)
                    return winner
        # Check diagonal (bottom-left to top-right) for winner
        for row in range(5, 2, -1):
            for col in range(4):
                if self.board[row][col]==self.board[row-1][col+1]==self.board[row-2][col+2]==self.board[row-3][col+3] and self.board[row][col]!="⬜":
                    if self.board[row][col] == self.players[self.turn]:
                        winner = self.turn
                    else:
                        winner = self.next
                    self.header[0][4] = "({} wins!)".format(winner)
                    return winner
    # If no blank spaces left and no one has won, tie game.
        if not any("⬜" == cell for row in self.board for cell in row):
            self.header[0][4] = "(no one wins...)"
            return "no one"
    # No winner yet
        return False

    def add_puck(self, player, col):
        """add a puck to column number `col`"""
        if player == self.turn:
            col -= 1 # index begins at 0
            for i in range(len(self.board) - 1, 1, -1): # start at 5, end at 1 (ignoring row numbering), increment by -1
                if self.board[i][col] == "⬜":
                    self.board[i][col] = self.players[player] # the cell is replaced with the player's color
                    self.turn, self.next = self.next, self.turn # switch
                    self.header[0][4] = "({}'s turn)".format(self.turn)
                    return

    def get_board(self):
        result = ''
        for row in self.header:
            result += ' '.join(row) + '\n'
        for row in self.board:
            result += ' '.join(row) + '\n'
        return result


class Games:
    """Discord, but now it has capitalism."""
    def __init__(self, bot):
        self.bot = bot
        self.handler = dbhandler.DbHandler()

    @commands.command(pass_context=True)
    async def c4(self, ctx):
        """open a game of connect 4."""
        numbers = ["{}⃣".format(i) for i in range(1, 8)] # TODO: fix this >:(
        game = Connect4()
        game.add_player(ctx.message.author.name)
        # set up board
        board = await self.bot.say(game.get_board())
        for item in numbers:
            await self.bot.add_reaction(board, item)
        # get second player
        await self.bot.add_reaction(board, "✅")
        confirm = await self.bot.say("react with ✅ to join the game!")
        while len(game.players) < 2:
            join = await self.bot.wait_for_reaction('✅', message=board)
            if join.user.name in game.players:
                await self.bot.remove_reaction(board, '✅', join.user)
                await self.bot.edit_message(confirm, "react with ✅ to join the game! you may not play against yourself.")
                continue
        game.add_player(join.user.name)
        # clean up
        await self.bot.remove_reaction(board, '✅', self.bot.user)
        await self.bot.remove_reaction(board, '✅', join.user)
        await self.bot.delete_message(confirm)
        await self.bot.edit_message(board, game.get_board())
        # play
        while not game.check_win():
            # wait for a turn to be taken
            turn = await self.bot.wait_for_reaction(numbers, message=board)
            game.add_puck(turn.user.name, numbers.index(turn.reaction.emoji) + 1)
            await self.bot.edit_message(board, game.get_board())
            await self.bot.remove_reaction(board, turn.reaction.emoji, turn.user)
        # clean up
        await self.bot.edit_message(board, game.get_board())
        await self.bot.clear_reactions(board)
            

    @commands.command(pass_context=True)
    async def fish(self, ctx):
        """gone fishing!  costs 15xp."""
        dir = "./cogs/games/assets/fish/"
        fishes = [f[:-4] for f in listdir(dir)] #every file in `dir` with extensions stripped
        usr_xp = self.handler.profile_information(ctx.message.author.id)["xp"]
        if usr_xp < 5:
            await self.bot.add_reaction(ctx.message, "🚫")
            await self.bot.say("this game costs 5xp to play.")
            return
        self.handler.update_xp(ctx.message.author.id, -5) # reduce xp by 5
        catch = rng.choice(fishes)
        await self.bot.send_file(ctx.message.channel, fp=dir + catch + '.png',
                                 content="{} spent 5xp and caught a {}!".format(ctx.message.author.display_name, catch))

        
        

def setup(bot):
    bot.add_cog(Games(bot))