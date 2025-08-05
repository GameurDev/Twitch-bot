from twitchio.ext import commands
from config import Config

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def prepare(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, Config.COOLDOWN_REGULAR, commands.Bucket.user)
    async def discord(self, ctx):
        await ctx.send(f"Rejoignez notre Discord: {Config.DISCORD_URL}")
        print('log')

    @commands.command()
    @commands.cooldown(1, Config.COOLDOWN_REGULAR, commands.Bucket.user)
    async def altasis(self, ctx):
        await ctx.send(f"Discord Altasis: {Config.ALTASIS_DISCORD}")

    @commands.command()
    @commands.cooldown(1, Config.COOLDOWN_REGULAR, commands.Bucket.user)
    async def ip(self, ctx):
        await ctx.send(f"IP Minecraft: {Config.MINECRAFT_IP}")

    @commands.command()
    @commands.cooldown(1, Config.COOLDOWN_REGULAR, commands.Bucket.user)
    async def site(self, ctx):
        await ctx.send(f"Site web: {Config.WEBSITE_URL}")

    @commands.command()
    @commands.cooldown(1, Config.COOLDOWN_REGULAR, commands.Bucket.user)
    async def config(self, ctx):
        await ctx.send(Config.PC_CONFIG)