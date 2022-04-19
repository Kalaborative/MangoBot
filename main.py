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

bot = commands.Bot('`')

client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

    await client.change_presence(activity=discord.Game('a game'))

keep_alive()
bot.load_extension('jishaku')
bot.run('OTY1MzA4MDQ1OTI2MjAzNDkz.YlxTLA.XTe-rt2ltE0ZpPJyjUoO0jF4BnI')
client.run('OTY1MzA4MDQ1OTI2MjAzNDkz.YlxTLA.XTe-rt2ltE0ZpPJyjUoO0jF4BnI')