from discord.ext import commands
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer
from markov import Markov, predict_words
import random
from chatbot import rapaizinho
from loadEnv import PREFIX
import discord

trainer = ListTrainer(rapaizinho)

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

        subst = {'me': 'se', 'te':'me', 'meu': 'seu', 'minha':'sua', 'eu': 'você'}

        for idx, option in enumerate(options):
            for palavra in option.split():
                if palavra.lower() in subst:
                    options[idx] = options[idx].replace(palavra, subst[palavra]).capitalize()
            
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

    @commands.command()
    async def markov(self, ctx: commands.Context):
        message = ctx.message.content.replace(PREFIX + 'markov', '')
        message = message.split()
        m = Markov(file_path='data/prompts.txt')
        chain = m.model
        await ctx.send(predict_words(chain, first_word = message[0], number_of_words = int(message[1])))

    @commands.command()
    async def write(self, ctx: commands.Context):
        message = ctx.message.content.replace(PREFIX + 'write', '')
        punctuations = ["!", ".", "?"]
        if message[-1:] not in punctuations:
            message += '.'
        file = open('data/prompts.txt', 'a')
        file.write(message)
        file.close()
        await ctx.send("Mensagem foi guardada na memória!")

    @commands.command()
    async def train(self, ctx: commands.Context):
        message = ctx.message.content.replace(PREFIX + 'train', '').replace('%','')
        mensagem = Statement(text=message, tags=['conversa'])
        last_message = message
        response = rapaizinho.generate_response(mensagem)
        await ctx.send(response)

        await ctx.send(f"'{response.text}' foi uma resposta coerente para '{message}'?\nSim ou Não")

        def check(m):
            return 'sim' in m.content or 'Sim' in m.content or 'Não' in m.content or 'não' in m.content

        current_message = await self.bot.wait_for('message', check=check)
        if ('sim' in current_message.content or 'Sim' in current_message.content):
            correct_response = Statement(text=response.text, persona='Rapazinho')
            rapaizinho.learn_response(correct_response, last_message)
            trainer.train([last_message, response.text])
            await ctx.send('Aprendido!')
        else:
            await ctx.send('Por favor, me diga qual seria uma resposta coerente: ')
            current_message = await self.bot.wait_for('message')
            correct_response = Statement(text=current_message.content, persona='Rapazinho')
            rapaizinho.learn_response(correct_response, last_message)
            trainer.train([last_message, response.text])
            await ctx.send('Aprendido!')


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if message.author.bot:
            return
        
        if message.content.startswith(PREFIX):
            return 
        
        if not self.started:
            return

        mensagem = Statement(text=message.content, tags=['conversa'])
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