from loadEnv import TOKEN, PREFIX, GOUTE, BELA
from bot import Bot
import discord
from comandos import Comandos
from CommandCleanup import CommandCleanup
from Prompts import Train
from discord.ext import commands

intents = discord.Intents.all()


OWNERS = GOUTE + BELA

bot = Bot(
    (Comandos, CommandCleanup, Train),
    intents=intents,
    command_prefix=commands.when_mentioned_or(PREFIX),
    owner_ids=OWNERS,
)

bot.run(TOKEN)
