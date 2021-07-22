from datetime import datetime
import random

import aiohttp
from discord.ext import commands
import discord

# import praw
import asyncpraw

from settings import REDDIT_APP_ID, REDDIT_APP_SECRET, REDDIT_SUBREDDITS, REDDIT_NSFW_SUBREDDITS


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = None
        if REDDIT_APP_ID and REDDIT_APP_SECRET:
            self.reddit = asyncpraw.Reddit(client_id=REDDIT_APP_ID, client_secret=REDDIT_APP_SECRET,
                                           user_agent=f"DISCORD_BOT:{REDDIT_APP_ID}:")

    @commands.command()
    async def reddit(self, ctx, subreddit: str = ""):
        async with ctx.channel.typing():
            if self.reddit:
                nsfw_flag = False
                rnd = random.randint(0, len(REDDIT_SUBREDDITS))
                chosen_subreddit = REDDIT_SUBREDDITS[rnd]
                if subreddit:
                    if subreddit in REDDIT_NSFW_SUBREDDITS:
                        chosen_subreddit = subreddit
                        nsfw_flag = True
                    else:
                        chosen_subreddit = subreddit

                a = await self.reddit.subreddit(chosen_subreddit)
                submissions = a.hot()

                a = []
                n=0
                async for x in submissions:
                    a.append(x)
                    n+=1
                post_to_pick = random.randint(0, n-1)
                nsfw_flag = True if a[post_to_pick].over_18 else False
                if nsfw_flag:
                    if not ctx.channel.is_nsfw():
                        await ctx.send("Please use this command in NSFW channel")
                        return
                await ctx.send(a[post_to_pick].url)

            else:
                await ctx.send("This is not working. Contact Administrator.")

    @commands.command(brief="Random picture of a meow")
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Meow",timestamp=datetime.utcnow(), colour=0xcc7900)
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="https://random.cat/")
                    await ctx.send(embed=embed)

    @commands.command(brief="Random picture of a woof")
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof",timestamp=datetime.utcnow(), colour=0xcc7900)
                    embed.set_image(url=data['url'])
                    embed.set_footer(text="http://random.dog/")

                    await ctx.send(embed=embed)

    @commands.command(brief="Random picture of a floofy")
    async def fox(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Floof",timestamp=datetime.utcnow(), colour=0xcc7900)
                    embed.set_image(url=data['image'])
                    embed.set_footer(text="https://randomfox.ca/")

                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))
