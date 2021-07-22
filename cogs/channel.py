import discord
from discord.ext import commands
from datetime import datetime


class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def mk(self, ctx):
        """make channel c,t,v,n [name]"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid sub command passed...')

    @mk.command(pass_context=True, name="c",aliases=['dir', "category"])
    async def make_c(self, ctx, name):
        """create Category"""
        existing_category = discord.utils.get(ctx.guild.categories, name=name)
        if existing_category is None:
            await ctx.guild.create_category_channel(name=name)
            embed = discord.Embed(title=f"Creating {name}", color=0x5cbac4, timestamp=datetime.now())
            await ctx.send(embed=embed)
            await ctx.send(f"{discord.utils.get(ctx.guild.categories, name=name).mention}")
        else:
            await ctx.send(f"{name} already exists")

    @mk.command(pass_context=True, name="t", aliases=['text', "Text"])
    async def make_t(self, ctx, name, category=None):
        """create Voice channel"""
        category = discord.utils.get(ctx.guild.categories, name=category)
        existing_channel = discord.utils.get(ctx.guild.channels, name=name, category=category)
        if existing_channel is None:
            await ctx.guild.create_text_channel(name=name, category=category)
            embed = discord.Embed(title=f"Creating {name}: ", color=0x5cbac4,
                                  timestamp=datetime.now())
            await ctx.send(embed=embed)
            await ctx.send(f"{discord.utils.get(ctx.guild.channels, name=name).mention}")
        else:
            await ctx.send(f"{name} already exists")

    @mk.command(pass_context=True,name='v', aliases=['voice', "Voice"])
    async def make_v(self, ctx, name, category=None):
        """create Voice channel"""
        category = discord.utils.get(ctx.guild.categories, name=category)
        existing_channel = discord.utils.get(ctx.guild.channels, name=name,
                                             category=discord.utils.get(ctx.guild.categories, name=category))
        if existing_channel is None:
            await ctx.guild.create_voice_channel(name=name, category=category)
            embed = discord.Embed(title=f"Creating {name}: ", color=0x5cbac4,
                                  timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            await ctx.send(f"{discord.utils.get(ctx.guild.channels, name=name).mention}")
        else:
            await ctx.send(f"{name} already exists")

    @mk.command(pass_context=True,name='n', aliases=['nsfw', "NSFW"])
    @commands.has_permissions(manage_channels=True)
    async def make_n(self, ctx, name, category=None):
        category = discord.utils.get(ctx.guild.categories, name=category)
        existing_channel = discord.utils.get(ctx.guild.channels, name=name, category=category)
        if existing_channel is None:
            await ctx.guild.create_text_channel(name=name, category=category, nsfw=True)
            embed = discord.Embed(title=f"Creating {name}:", color=0x5cbac4, timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            await ctx.send(f"{discord.utils.get(ctx.guild.channels, name=name).mention}")
        else:
            await ctx.send(f"{name} already exists")

    @commands.group()
    async def rm(self, ctx):
        """remove category or channel [name] [category]"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid sub command passed...')

    @rm.command(pass_context=True, name='c',aliases=['dir','category'])
    async def remove_c(self, ctx, name):
        """remove category c [name]"""
        existing_category = discord.utils.get(ctx.guild.categories, name=name)
        if existing_category is not None:
            await existing_category.delete()
            await ctx.send(
                embed=discord.Embed(title=f"Deleting category {name}", color=0x5cbac4, timestamp=datetime.utcnow()))
        else:
            await ctx.send(
                embed=discord.Embed(title=f"{name} not exists", color=0x5cbac4, timestamp=datetime.utcnow()))

    @rm.command(pass_context=True, name='channel', aliases=['t', 'v', 'n', 'text', 'voice'])
    async def remove_channel(self, ctx, name, category=None):
        """remove channel t,v,n [name]"""
        category = discord.utils.get(ctx.guild.categories, name=category)
        existing_channel = discord.utils.get(ctx.guild.channels, name=name, category=category)
        if existing_channel is not None:
            await existing_channel.delete()
            await ctx.send(embed=discord.Embed(title=f"Deleting {name}", color=0x5cbac4, timestamp=datetime.utcnow()))
        else:
            await ctx.send(
                embed=discord.Embed(title=f"{name} not exists", color=0x5cbac4, timestamp=datetime.utcnow()))


def setup(bot):
    bot.add_cog(Channel(bot))
