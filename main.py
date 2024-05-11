from loadEnv import TOKEN, PREFIX
from bot import Bot
import discord
from comandos import Comandos
from discord.ext import commands

intents = discord.Intents.all()

bot = Bot([Comandos], intents=intents, command_prefix=commands.when_mentioned_or(PREFIX))

bot.run(TOKEN)