from loadEnv import TOKEN, PREFIX
from bot import Bot
import discord
from comandos import Comandos
from CommandCleanup import CommandCleanup
from discord.ext import commands

intents = discord.Intents.all()

bot = Bot(
    (Comandos, CommandCleanup),
    intents=intents,
    command_prefix=commands.when_mentioned_or(PREFIX),
    owner_ids=OWNER_IDS,
)

bot.run(TOKEN)

