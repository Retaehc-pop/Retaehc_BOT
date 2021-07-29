import os

from discord.ext import commands
import discord
from settings import *
import asyncio
from datetime import datetime
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
role_dict = {}

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with your heart'))
    print(f'[LOGS] Logged in as {bot.user} (ID: {bot.user.id})')


@bot.event
async def on_connect():
    print('[LOGS] Connecting to discord')


@bot.event
async def on_disconnect():
    print("[LOGS] Disconnected from discord server")


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """Gives a role based on a reaction emoji."""
    end = True
    for key in role_dict.keys():
        if payload.message_id == key:
            end = False
    if end:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    emoji_to_role = role_dict[payload.message_id]
    try:
        role_id = emoji_to_role[payload.emoji]
    except KeyError:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    try:
        await payload.member.add_roles(role)
    except discord.HTTPException:
        pass


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    """Removes a role based on a reaction emoji."""
    end = True
    for keys in role_dict.keys():
        if payload.message_id == keys:
            end = False
    if end:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    emoji_to_role = role_dict[payload.message_id]
    try:
        role_id = emoji_to_role[payload.emoji]
    except KeyError:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        return

    try:
        await member.remove_roles(role)
    except discord.HTTPException:
        pass


@bot.command()
async def setrole(ctx):
    """ create embed which can self assigned role to each person"""
    def is_correct(m):
        return m.author == ctx.message.author

    dic = {}
    await ctx.send("emoji:role or quit")
    while True:
        try:
            intents = await bot.wait_for('message', check=is_correct, timeout=30.0)
            if intents.content == "quit" or intents.content == "done":
                embed = discord.Embed(title="Self Role Assignment",description='add role by reacting to the assigned emoji', timestamp=datetime.utcnow())
                for key in dic.keys():
                    embed.add_field(name=key.name, value=discord.utils.get(ctx.guild.roles, id=dic[key]),)
                message = await ctx.send(embed=embed)
                for key in dic.keys():
                    await message.add_reaction(key.name)
                await asyncio.sleep(3)
                role_dict[message.id] = dic
                return
        except asyncio.TimeoutError:
            return await ctx.send(f'Timeout Error')

        intents = intents.content.split(" ")
        if intents[1].startswith("<@&") and intents[1].endswith(">"):
            role = int(intents[1][3:-1])
            emoj = discord.PartialEmoji(name=intents[0])
            dic[emoj] = role
        else:
            await ctx.send("wrong role")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(DISCORD_BOT_TOKEN)
