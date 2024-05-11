from discord.ext import commands
from chatterbot.conversation import Statement
import random
from chatbot import rapaizinho
from loadEnv import PREFIX
import discord

class Comandos(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.started = False
    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

    @commands.command()
    async def ask(self, ctx: commands.Context):
        options = ['Sim', 'Não']
        weights = [5/13, 8/13] # A lista antes tinha 5 sims e 8 nãos
        await ctx.send(random.choices(options, weights=weights)[0])

    @commands.command()
    async def choose(self, ctx: commands.Context):
        message = ctx.message.content.replace(PREFIX + 'choose', '').replace('?','')
        
        message = message.replace(' ou ', ', ')

        options = message.split(', ')
                
        await ctx.send(random.choice(options))

    @commands.command()
    async def nerd(self, ctx: commands.Context):
        await ctx.send(file=discord.File('gifs/nerd_dragon.gif'))

    @commands.command()
    async def goofy(self, ctx: commands.Context):
        await ctx.send(file=discord.File('gifs/bb_dragon.gif'))

    @commands.command()
    async def greedy(self, ctx: commands.Context):
        await ctx.send(file=discord.File('gifs/urso_spyro.gif'))

    @commands.command()
    async def desperate(self, ctx: commands.Context):
        await ctx.send(file=discord.File('gifs/wizards.gif'))

    
    @commands.command()
    async def pat(self, ctx: commands.Context, member: discord.Member):
        # mentions = ctx.message.author.mention
        await ctx.send(member.mention, file=discord.File('gifs/anime_pat.gif'))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if message.author.bot:
            return
        
        if message.content.startswith(PREFIX):
            return 
        
        if not self.started:
            return

        mensagem = Statement(text=message.content)
        response = rapaizinho.generate_response(mensagem)
        
        # response = f"{message.author.nick.split()[0]} disse {mensagem}"
        await message.channel.send(response)
        
    @commands.hybrid_command()
    async def start(self, ctx: commands.Context):
        self.started = True

        await ctx.send("Rapaizinho iniciado!")
        
    @commands.hybrid_command()
    async def stop(self, ctx: commands.Context):
        self.started = False

        await ctx.send("Rapaizinho desligado!")