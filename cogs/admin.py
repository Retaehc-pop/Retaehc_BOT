from discord.ext import commands
import discord

import datetime

from settings import MODERATOR_ROLE_NAME


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        """load cogs"""
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send("Could not unload cog")
            return
        await ctx.send("Cog unloaded")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        """load cogs"""
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not load cog")
            return
        await ctx.send("Cog loaded")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """reload cogs"""
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not reload cog")
            return
        await ctx.send("Cog reloaded")

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, *args):
        """Server status"""
        guild = ctx.guild

        no_voice_channels = len(guild.voice_channels)
        no_text_channels = len(guild.text_channels)

        embed = discord.Embed(Title=str(guild.name),
                              description=f"by -> {self.bot.user.name}",
                              timestamp=datetime.datetime.utcnow(),
                              colour=0xffffff)

        embed.set_thumbnail(
            url="https://spaceac.net/wp-content/uploads/2021/03/2020-Transparent-Red-1024x1024.png")

        embed.set_image(
            url="https://spaceac.net/wp-content/uploads/2021/03/Banner-White-980x139.png")

        emoji_string = ""
        for e in guild.emojis:
            if e.is_usable():
                emoji_string += str(e)
        embed.add_field(name="Custom Emojies",
                        value=emoji_string or "No emojis available", inline=False)


        embed.add_field(name="# Voice Channels", value=str(no_voice_channels))

        embed.add_field(name="# Text Channels", value=str(no_text_channels))

        embed.add_field(name="AFK Channel:", value=guild.afk_channel)

        embed.add_field(name="Total User", value=str(guild.member_count), inline=False)

        embed.add_field(name="Total Role", value=str(len(guild.roles)), inline=True)

        embed.add_field(name="region", value=str(guild.region), inline=False)
        embed.title = guild.name


        # embed.set_author(name=self.bot.user.name)
        embed.set_footer(text='Cheater Bot Created by Retaehc')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))