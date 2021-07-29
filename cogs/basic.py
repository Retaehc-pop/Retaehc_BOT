import asyncio

from discord.ext import commands
import discord
from datetime import datetime
from utils import text_to_owo, notify_user


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if str(e).find('.') != -1:
            return

        embed = discord.Embed(title="Command_Error",
                              description=f'->{e}',
                              colour=0xf94324)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_error(self, ctx, ex):
        embed = discord.Embed(title="Error",
                              description=str(ex),
                              colour=0xf94324)
        await ctx.send(embed=embed)

    @commands.command(brief="Any message to owo")
    async def owo(self, ctx):
        embed = discord.Embed(colour=0xffc2c8)
        embed.add_field(name="UWU", value=str(text_to_owo(ctx.message.content)))
        await ctx.send(embed=embed)

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
    async def reminder(self, ctx, time, *, reminder: str):
        """set reminder (time d.h.m.s or dd:mm:yy:hh:mm:ss) (reminder)"""
        print(reminder)
        embed = discord.Embed(title="Reminder", description=f"{reminder} in {time}", color=0x5cbac4,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="If you have any questions send feedback to POP")
        embed.set_author(name=ctx.author, icon_url=f"{ctx.author.avatar_url}")
        if reminder is None:
            await ctx.send(embed=discord.Embed(title="Warning",
                                               description='Please specify what do you want me to remind you about.',
                                               color=0xf94324))
            return

        elif time is None:
            await ctx.send(embed=discord.Embed(title="Warning", description='Please specify time.', color=0xf94324))
            return

        r = reminder.split(' ')
        roles = []
        for item in r:
            if item.startswith("<@&") and item.endswith(">"):
                roles.append(int(item[3:-1]))

        if time.find(':') == -1:
            counter = ""
            seconds = 0
            Time = time.lower().split('.')
            for time in Time:
                if time.endswith('d'):
                    seconds += int(time[:-1]) * 60 * 60 * 24
                    counter += f"{time[:-1]} D"
                elif time.endswith('h'):
                    seconds += int(time[:-1]) * 60 * 60
                    counter += f"{time[:-1]} H"
                elif time.endswith('m'):
                    seconds += int(time[:-1]) * 60
                    counter += f"{time[:-1]} M"
                elif time.endswith('s'):
                    seconds += int(time[:-1])
                    counter += f"{time[:-1]} S"

            if seconds <= 0:
                await ctx.send(embed=discord.Embed(title="Warning",
                                                   description='Please specify a proper duration: Time cant be lower than 0',
                                                   color=0xf94324))
                return
            elif seconds > 7776000:
                await ctx.send(embed=discord.Embed(title="Warning",
                                                   description='You have specified a too long duration!\nMaximum duration is 90 days.',
                                                   color=0xf94324))
                return

            embed.add_field(name=f'{ctx.author}', value=f'Reminder in {counter} about {reminder}')
            await ctx.send(embed=embed)
            await asyncio.sleep(seconds)
            await ctx.send(f"{ctx.author.mention}")
            for role in roles:
                await ctx.send(discord.utils.get(ctx.guild.roles,id=role).mention)
            await ctx.send(
                embed=discord.Embed(title='Reminder', description=f'{reminder} {counter} ago', color=0x5cbac4,
                                    timestamp=datetime.utcnow()))
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
            now = datetime.utcnow()
            delta = dt - datetime.now()
            seconds = (delta.days * 86400) + delta.seconds
            embed.add_field(name="Reminder in ",
                            value=f"{dt.day}/{dt.month}/{dt.year} at {dt.hour}:{dt.minute}:{dt.second}")
            await ctx.send(embed=embed)
            await ctx.send(seconds)
            await asyncio.sleep(seconds)
            await ctx.send(f"{ctx.author.mention}")
            for role in roles:
                await ctx.send(discord.utils.get(ctx.guild.roles, id=role).mention)
            await ctx.send(
                embed=discord.Embed(title='Reminder', description=f'{reminder} {counter} ago', color=0x5cbac4,
                                    timestamp=datetime.utcnow()))

def setup(bot):
    bot.add_cog(Basic(bot))
