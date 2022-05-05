import discord,random
import chessTools
from discord.ext import commands


class Chess_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['chess'])
    async def chessHelp(self, ctx):
        """ gives a list of chess related commands """
        await ctx.send("Here is a list of all chess related commands I can do:\n- >games - Gives the number of chess games a user has played today.\n- >rating - Gives a users current rating on chess.com.\n- >online - Gives a user's online status.")


    @commands.command(aliases=['games'])
    async def chessCount(self, ctx, username):
        """ gives a users chess game count for today """
        game = chessTools.ChessGames(username)
        await ctx.send(f"{username} has played {game} games of Chess today")

    @commands.command()
    async def rating(self, ctx, username):
        """ gives a users online status """
        rating = chessTools.GetRanking(username)
        await ctx.send(f"{username} current ranking is {rating}")

def setup(bot):
    bot.add_cog(Chess_Commands(bot))
    
    