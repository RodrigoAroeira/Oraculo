from typing import Iterable
from loadEnv import PREFIX
from colorama import Fore
from discord.ext import commands


class Bot(commands.Bot):

    started = False

    def __init__(self, cogs: Iterable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cogs = cogs

    async def on_ready(self):

        await self.load_cogs()

        print(f"Online como {Fore.YELLOW}{self.user}{Fore.RESET} em: {Fore.GREEN}")
        async for guild in self.fetch_guilds():
            print(f"\t- {guild.name}<{guild.id}>")

        print(Fore.RESET)

    async def load_cogs(self):
        for cog in self._cogs:
            await self.add_cog(cog(self))
        await self.tree.sync()
        self._cogs = ()  # Remover cogs, já que on_ready pode rodar mais de uma vez
