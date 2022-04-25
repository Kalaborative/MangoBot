import discord
from discord.ext import commands
from discord.ui import Button, View
import requests
import json
from random import choice
from threading import Thread
from os import environ
# import jishaku
import asyncio

# app = Flask('')

# @app.route('/')
# def home():
#     return "Hello. I am alive!"

# def run():
# 	port = int(environ.get("PORT", 5000))
# 	app.run(host='0.0.0.0', port=port)

# def keep_alive():
#     t = Thread(target=run)
#     t.start()

db = {}
coinAmts = {

}

# discord.ButtonStyle().primary

intents = discord.Intents.default()
intents.message_content = True

# bot = commands.Bot('`', intents=intents)

# client = discord.Client(intents=intents)

# @bot.event
# async def on_ready():
#     ch = bot.get_channel(965308897256702046)
#     await ch.send(f"logged in as {bot.user}")
    # print(f"We have logged in as {client.user}")

    # await bot.change_presence(activity=discord.Game())

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=intents, command_prefix='>')

    async def setup_hook(self):
        await self.load_extension('jishaku')
    
    async def close(self):
        await super().close()
    
    async def on_ready(self):
        ch = self.get_channel(965308897256702046)
        print("Ready!")
        await ch.send(f"logged in as {self.user}")

# keep_alive()
# bot.load_extension('jishaku')
bot = MyBot()

@bot.command()
async def hello(ctx):
    button1 = Button(label='Click me!', style=discord.ButtonStyle.green)
    button2 = Button(emoji='🍦', style=discord.ButtonStyle.primary)
    button3 = Button(label='Go to Google', url='https://google.com')
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    await ctx.send("Hi!", view=view)

@bot.command()
async def bal(ctx):
    q_author = ctx.author
    if q_author not in coinAmts.keys():
        coinAmts[q_author] = [0, 0]
    wallet = coinAmts[q_author][0]
    bank = coinAmts[q_author][1]
    myEmbed = discord.Embed(color=discord.Color.blue(), title=f'{ctx.author}', description=f'Wallet: {wallet} | Bank {bank}')
    await ctx.send(embed=myEmbed)

bot.run('OTY1MzA4MDQ1OTI2MjAzNDkz.YlxTLA.XTe-rt2ltE0ZpPJyjUoO0jF4BnI')
# client.run('OTY1MzA4MDQ1OTI2MjAzNDkz.YlxTLA.XTe-rt2ltE0ZpPJyjUoO0jF4BnI')