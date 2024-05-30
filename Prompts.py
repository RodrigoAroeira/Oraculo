from pprint import pprint
from discord.ext import commands
import discord
import os
from loadEnv import PREFIX

import time


class Train(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.filename = "prompts.txt"

    @commands.command(hidden=True)
    async def reach(self, ctx: commands.Context):
        if not await self.bot.is_owner(ctx.author):
            return
        await ctx.message.delete()
        print("Training...")
        text_channels: dict[discord.TextChannel, int] = {}
        start = time.time()
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                text_channels[channel] = 0

        print("Found all channels")
        
        with open(self.filename, "w", encoding="utf-8") as file:
            for channel in text_channels:
                print("Writing for", channel)
                if channel.permissions_for(channel.guild.me).read_message_history is False:
                    print("No permission to read messages in", channel)
                    continue
                if channel.name == 'bots123':
                    print("Skipping bots channel")
                    continue
                async for message in channel.history(limit=None):
                    if not message.author.bot:
                        file.write(f"{message.content}\n")
                        text_channels[channel] += 1

                print("Finished", channel)

        end = time.time()
        print("Wrote all messages from")
        pprint(text_channels)

        print("Time taken:", end - start)
        print("Messages written:", sum(text_channels.values()))

        os.rename(self.filename, "data/prompts.txt")

