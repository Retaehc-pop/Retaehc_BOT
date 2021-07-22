import random

import discord
from discord.ext import commands


class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Gives a random number between 1 and 100")
    async def randint(self, ctx):
        n = random.randrange(1, 101)
        embed = discord.Embed(title=str(n),colour=0x006798)
        await ctx.send(embed=embed)

    @commands.command(brief="Random number between 1 and 6")
    async def dice(self, ctx):
        n = random.randrange(1, 6)
        embed = discord.Embed(title=str(n),colour=0x006798)
        await ctx.send(embed=embed)

    @commands.command(brief="Either Heads or Tails")
    async def coin(self, ctx):
        n = random.randint(0, 1)
        c = "Heads" if n == 1 else "Tails"
        embed = discord.Embed(title=c,colour=0x006798)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Gamble(bot))