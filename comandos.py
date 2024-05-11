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
        options = ['Sim', 'Não','Sim', 'Não','Sim', 'Não','Sim', 'Não','Não','Não','Não','Não','Sim']
        await ctx.send(random.choice(options))

    @commands.command()
    async def choose(self, ctx: commands.Context):
        message = ctx.message.content
        message = message.replace('%choose', '')
        if "?" in message:
            message = message.replace('?', '')

        if "ou" and ", " in message:
            message = message.replace('ou', ', ')
            options = message.split(', ')
        
        elif "ou" in message:
            options = message.split('ou')
        else:
            options = message.split(', ')
        
        await ctx.send(random.choice(options))

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