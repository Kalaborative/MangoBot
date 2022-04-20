import discord
from discord.ext import commands
import requests
import json
from random import choice
from flask import Flask
from threading import Thread
from os import environ

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

bot = commands.Bot('`', intents=intents)

client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    ch = bot.get_channel(965308897256702046)
    await ch.send(f"We have logged in as {bot.user}")
    # print(f"We have logged in as {client.user}")

    await bot.change_presence(activity=discord.Game(f'on {len(bot.guilds)} {"servers" if len(bot.guilds) > 1 else "server"}'))

keep_alive()
bot.load_extension('jishaku')
bot.run('OTY1MzA4MDQ1OTI2MjAzNDkz.YlxTLA.XTe-rt2ltE0ZpPJyjUoO0jF4BnI')
# client.run('OTY1MzA4MDQ1OTI2MjAzNDkz.YlxTLA.XTe-rt2ltE0ZpPJyjUoO0jF4BnI')