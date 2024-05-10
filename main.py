from loadEnv import TOKEN, PREFIX
from bot import Bot
import discord
from comandos import Comandos

intents = discord.Intents.all()

bot = Bot([Comandos], intents=intents, command_prefix=PREFIX)

bot.run(TOKEN)