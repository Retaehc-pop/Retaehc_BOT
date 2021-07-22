import os

from discord.ext import commands
import discord
from settings import *

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

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


for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(DISCORD_BOT_TOKEN)
