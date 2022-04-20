import discord
from discord.ext import commands
from discord.ui import Button 
import requests
import json
from random import choice
from threading import Thread
from os import environ
# import jishaku
from flask import Flask
import asyncio

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
	port = int(environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

db = {}

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
        await ch.send(f"logged in as {self.user}")
        # print("Ready!")

keep_alive()
# bot.load_extension('jishaku')
bot = MyBot()
bot.run('OTY1MzA4MDQ1OTI2MjAzNDkz.YlxTLA.XTe-rt2ltE0ZpPJyjUoO0jF4BnI')
# client.run('OTY1MzA4MDQ1OTI2MjAzNDkz.YlxTLA.XTe-rt2ltE0ZpPJyjUoO0jF4BnI')