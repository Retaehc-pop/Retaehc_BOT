import asyncio

from discord.ext import commands
import discord
from datetime import datetime
from utils import text_to_owo, notify_user


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        print(ex)
        embed = discord.Embed(title="Error",
                              description=str(ex),
                              colour=0xf94324)
        await ctx.send(embed=embed)

    @commands.command(brief="Any message to owo")
    async def owo(self, ctx):
        embed = discord.Embed(colour=0xffc2c8)
        embed.add_field(name="UWU", value=str(text_to_owo(ctx.message.content)))
        await ctx.send(embed)

    @commands.command(brief="Creates an invite link to the channel")
    @commands.guild_only()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)

    @commands.command()
    async def poke(self, ctx, member: discord.Member = None):
        """POKE SOMEONE"""
        if member is not None:
            message = f"{ctx.author.name} poked you!!!!"
            await notify_user(member, message)
        else:
            await ctx.send("@mention to poke someone.")

    @commands.command(pass_context=True)
    async def users(self, ctx):
        """display user in this server"""
        embed = discord.Embed(title=f"Member in {ctx.guild.name}",
                              timestamp=datetime.utcnow(),
                              description=f"There are {ctx.guild.member_count} users",
                              color=0x5cbac4, )
        server_role = ctx.guild.roles
        server_role.reverse()
        for i, role in enumerate(server_role):
            if role.name != "@everyone" and len(role.members) != 0:
                a = "\n".join(str(m.name) for m in role.members)
                embed.add_field(name=role.name, value=a, inline=False)
                # if i%2 == 0:
                #     embed.add_field(name=role.name, value=a, inline=True)
                # else:
                #     embed.add_field(name=role.name, value=a, inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['clock', 'date'])
    async def time(self, ctx):
        """ display time"""
        embed = discord.Embed(title=f"{datetime.today().strftime('%d/%m/%Y')}",
                              color=discord.Colour.random(), )
        embed.add_field(name=f"{datetime.now().time()}", value=f"{ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """PONG"""
        embed = discord.Embed(title="PONG")
        await ctx.send(embed=embed)

    @commands.command(case_insensitive=True, aliases=["remind", "remindme", "remind_me", "alarm"])
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def reminder(self, ctx, time, *, reminder, role: discord.Role):
        """set reminder (time dhms or dd:mm:yy:hh:mm:ss) (reminder)"""
        embed = discord.Embed(title="Reminder", description=f"{reminder} in {time}",
                              color=0x5cbac4, timestamp=datetime.utcnow())
        embed.set_footer(text="If you have any questions send feedback to POP")
        embed.set_author(name=ctx.author, icon_url=f"{ctx.author.avatar_url}")
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning',
                            value='Please specify what do you want me to remind you about.')  # Error message
            await ctx.send(embed=embed)
            return
        elif time is None:
            embed.add_field(name='Warning',
                            value='Please specify time')  # Error message
            await ctx.send(embed=embed)
            return
        else:
            if time.find('/') == -1:
                counter = ""
                if time.lower().endswith("d"):
                    seconds += int(time[:-1]) * 60 * 60 * 24
                    counter = f"{seconds // 60 // 60 // 24} days"
                if time.lower().endswith("h"):
                    seconds += int(time[:-1]) * 60 * 60
                    counter = f"{seconds // 60 // 60} hours"
                elif time.lower().endswith("m"):
                    seconds += int(time[:-1]) * 60
                    counter = f"{seconds // 60} minutes"
                elif time.lower().endswith("s"):
                    seconds += int(time[:-1])
                    counter = f"{seconds} seconds"
                if seconds == 0:
                    embed.add_field(name='Warning',
                                    value='Please specify a proper duration, send `reminder_help` for more information.')
                elif seconds > 7776000:
                    embed.add_field(name='Warning',
                                    value='You have specified a too long duration!\nMaximum duration is 90 days.')
                else:
                    await ctx.send(embed=embed)
                    await asyncio.sleep(seconds)
                    await ctx.send(f"Hi, {ctx.author.mention} asked me to remind you about {reminder} {counter} ago.")
                    return
            else:
                counter = time.split(":")
                if len(counter) != 6:
                    embed.add_field(name='Warning',
                                    value='Please specify time')  # Error message
                    await ctx.send(embed=embed)
                    return

                dt = datetime(day=int(counter[0]), month=int(counter[1]), year=int(counter[2]),
                              hour=int(counter[3]), minute=int(counter[4]), second=int(counter[5]))
                now = datetime.now()
                delta = dt - datetime.now()
                seconds = (delta.days * 86400) + delta.seconds
                embed.add_field(name="you will be alarm at",
                                value=f"{dt.day}/{dt.month}/{dt.year} at {dt.hour}:{dt.minute}:{dt.second}")
                await ctx.send(embed=embed)
                await asyncio.sleep(seconds)
                await ctx.send(f"{ctx.author.mention} asked me to remind {role} about {reminder} since {now}.")


def setup(bot):
    bot.add_cog(Basic(bot))
