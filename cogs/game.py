import random
from discord.ext import commands
import discord
import asyncio

from rps.model import RPS
from rps.parser import RockPaperScissorParser
from rps.controller import RPSGame

from hangman.controller import HangmanGame


# ,command_attrs=dict(hidden=True)
class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="rock | paper | scissor")
    async def rps(self, ctx, user_choice: RockPaperScissorParser = RockPaperScissorParser(RPS.ROCK)):
        """
        Play Rock Paper Scissors
        """
        game_instance = RPSGame()

        user_choice = user_choice.choice

        won, bot_choice = game_instance.run(user_choice)

        if won is None:
            message = f"It's a draw! Both chose: {user_choice}"
        elif won is True:
            message = f"You win: {user_choice} vs {bot_choice}"
        elif won is False:
            message = f"You lose: {user_choice} vs {bot_choice}"

        await ctx.send(message)

    @commands.command()
    # @commands.dm_only()
    async def hangman(self, ctx, guess: str):
        """
        Play hangman
        """
        player_id = ctx.author.id
        hangman_instance = HangmanGame()
        game_over, won = hangman_instance.run(player_id, guess)

        if game_over:
            game_over_message = "You did not win"
            if won:
                game_over_message = "Congrats you won!!"

            game_over_message = game_over_message + \
                                " The word was %s" % hangman_instance.get_secret_word()

            await hangman_instance.reset(player_id)
            await ctx.send(game_over_message)

        else:
            await ctx.send("Progress: %s" % hangman_instance.get_progress_string())
            await ctx.send("Guess so far: %s" % hangman_instance.get_guess_string())

    @commands.command(pass_context=True)
    async def guess(self, ctx):
        """guessing game from 1 - 10"""
        await ctx.send(f'{ctx.message.author.mention} guess a number between 1 and 10.')

        def is_correct(m):
            return m.author == ctx.message.author and m.content.isdigit()

        answer = random.randint(1, 10)
        try:
            gs = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send(f'Sorry, you took too long it was {answer}.')

        if int(gs.content) == answer:
            await ctx.send('You are right!')
        else:
            await ctx.send(f'Oops. It is actually {answer}.')

def setup(bot):
    bot.add_cog(Games(bot))
