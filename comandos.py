from discord.ext import commands
from chatbot import rapaizinho
from loadEnv import PREFIX
import discord

class Comandos(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if message.author.bot:
            return
        
        if message.content.startswith(PREFIX):
            await self.bot.process_commands(message)
            return 
        
        
        mensagem = message.content
        response = rapaizinho.generate_response(mensagem)
        
        await message.channel.send(response)
        
        
