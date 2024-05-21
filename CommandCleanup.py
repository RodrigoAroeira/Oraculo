from typing import Optional
from discord.ext import commands
import discord
import os
import pytz
from bot import Bot


class ConfirmButton(discord.ui.Button):

    def __init__(self, messages: list[discord.Message], original_ctx: commands.Context) -> None:
        super().__init__(style=discord.ButtonStyle.green, label="Confirm")
        self.messages = messages
        self.original_ctx = original_ctx

    async def callback(self, interaction: discord.Interaction):
        if not interaction.channel.permissions_for(interaction.channel.me).manage_messages:
            await interaction.response.send_message("Nice try, mas eu ainda não tenho permissões para fazer isso", ephemeral=True, delete_after=15)
            return
        await interaction.message.delete(delay=15)
        return
        for message in self.messages:
            await message.delete()
        await interaction.message.delete()

        await self.original_ctx.send(f"{len(self.messages)} mensagens apagadas", delete_after=15)



class CancelButton(discord.ui.Button):

    def __init__(self):
        super().__init__(style=discord.ButtonStyle.red, label="Cancel")

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()




class CommandCleanup(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(permission="manage_messages")
    async def clean(self, ctx: commands.Context,*, content: str, limit: int = 1000, author: Optional[discord.Member] = None):


        if not ctx.guild.me.permissions_in(ctx.channel).manage_messages:
            return await ctx.send("Eu não tenho permissão para apagar mensagens.")

        if not ctx.channel.permissions_for(ctx.author).manage_messages:
            return await ctx.send("Você não tem permissão para usar esse comando.")
        # await ctx.message.delete()

        messages = [
            message
            async for message in ctx.channel.history(limit=limit, before=ctx.message.created_at)
            if content.lower() in message.content.lower()
            # and (author is None or message.author.id == author.id)
        ]

        if not messages:
            return await ctx.send("Nenhuma mensagem encontrada.")

        filename = "messages.txt"
        with open(filename, "w") as file:
            for message in messages:
                local_time = message.created_at.replace(tzinfo=pytz.utc).astimezone(tz=None)
                file.write(
                    f"{message.author} {local_time.strftime('%Y-%m-%d %H:%M:%S')} - {message.content}\n"
                )

        confirm_button = ConfirmButton(messages, ctx)
        cancel_button = CancelButton()

        view = discord.ui.View()

        view.add_item(confirm_button)
        view.add_item(cancel_button)

        timeoutMinutes = 15
        timeoutSeconds = timeoutMinutes * 60
        message = await ctx.author.send(
            "Tem certeza que deseja apagar essas mensagens?",
            file=discord.File(filename),
            view=view,
            delete_after=timeoutSeconds
        )
        os.remove(filename)


        warning = await ctx.author.send(f"Essa mensagem será deletada em {timeoutMinutes} minutos.", delete_after=timeoutSeconds)
        messages.append(warning) # Delete warning message with
