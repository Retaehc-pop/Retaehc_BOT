import discord
from discord.ext import commands

from utils import get_momma_jokes


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="yo mama (member)")
    async def insult(self, ctx, member: discord.Member = None):
        insult = await get_momma_jokes()
        if member is not None:
            await ctx.send(f"{member.mention} eat this: {insult} ")
        else:
            await ctx.send(f"{ctx.message.author.name} for yourself: {insult}")


def setup(bot):
    bot.add_cog(NSFW(bot))
