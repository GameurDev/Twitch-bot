from twitchio.ext import commands
from config import Config

class UtilsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def prepare(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, Config.COOLDOWN_REGULAR, commands.Bucket.user)
    async def help(self, ctx):
        await ctx.send(Config.HELP)