import random
from twitchio.ext import commands
from config import Config

class BingoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reset_bingo()

    def prepare(self, bot):
        # Méthode requise si utilisation de load_module
        self.bot = bot

    def reset_bingo(self):
        self.bingo_active = False
        self.secret_number = None
        self.winner = None
        self.guesses = set()

    @commands.command(name="bingo")
    async def start_bingo(self, ctx):
        if not self.bot.is_moderator(ctx):
            return

        if self.bingo_active:
            await ctx.send("⚠️ Un bingo est déjà en cours !")
            return

        self.reset_bingo()
        self.bingo_active = True
        self.secret_number = random.randint(Config.BINGO_MIN, Config.BINGO_MAX)
        await ctx.send(f"🎲 BINGO ! Devinez le nombre entre {Config.BINGO_MIN} et {Config.BINGO_MAX}")
        print(f"Nombre secret: {self.secret_number}")

    @commands.command(name="stopbingo")
    async def stop_bingo(self, ctx):
        if not self.bot.is_moderator(ctx):
            return

        if not self.bingo_active:
            await ctx.send("ℹ️ Aucun bingo en cours")
            return

        self.bingo_active = False
        await ctx.send(f"🛑 Bingo arrêté. Le nombre était: {self.secret_number}")

    async def cog_check(self, ctx):
        if ctx.message.echo or not ctx.message.author:
            return False

        if self.bingo_active and not self.winner:
            await self.check_bingo_guess(ctx.message)
        return False

    async def check_bingo_guess(self, message):
        try:
            content = message.content.strip()
            if not content.isdigit():
                return

            guess = int(content)
            if not (Config.BINGO_MIN <= guess <= Config.BINGO_MAX):
                return

            if message.author.name in self.guesses:
                return

            self.guesses.add(message.author.name)

            if guess == self.secret_number:
                self.winner = message.author.name
                self.bingo_active = False
                await message.channel.send(f"🏆 {self.winner} a gagné ! Nombre: {self.secret_number}")
        except Exception as e:
            print(f"❌ Erreur Bingo: {str(e)}")
            