import os
import asyncio
from pathlib import Path
from threading import Thread
from datetime import datetime
import traceback
import toml
import discord
from discord.ext import commands
from flask import Flask

app = Flask('')


@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()


# Better to keep the token away from main.py
# make sure the config.toml file is in your
# .gitignore!

with open('config.toml', 'w') as token_file:
    access_token = os.environ['ACCESS_TOKEN']
    to_write = ['[startup]', '\ntoken = "{}"'.format(access_token)]
    token_file.writelines(to_write)

file_path = Path(__file__).resolve().parent / "config.toml"
with open(file_path, "r") as file:
    config_file = toml.load(file)


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            # Might as well use all intents, as this is a small bot
            intents=discord.Intents.all(),
            command_prefix='!',
            case_insensitive=True
        )

        # Initialising bot variables, these can be accessed
        # **anywhere** you have access to your bot variable.
        self.coin_amts = {}
        self.db = {}
        # Just incase we ever want to access config variables
        self.config = config_file

    async def startup_message(self):
        # Waiting for the cache to populate
        await self.wait_until_ready()

        ch = self.get_channel(965308897256702046)
        await ch.send('Bot is online!')

    async def on_error(self, event_method: str, /, *args, **kwargs) -> None:

        print("Error sending!")
        errors_channel = self.get_channel(965762182124011541)
        embed = discord.Embed(
            title=':x: Bot Error!',
            color=discord.Color.magenta()
        )

        embed.add_field(name="Event", value=event_method)
        embed.description = '```py\n{}\n```'.format(traceback.format_exc())
        embed.timestamp = datetime.utcnow()
        await errors_channel.send(embed=embed)

    async def setup_hook(self):
        # Loading all the cogs in the /cogs folder
        cogs = Path(__file__).resolve().parent
        for filename in os.listdir(cogs / "cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        await self.load_extension('jishaku')
        asyncio.create_task(self.startup_message())

    def run(self, token: str = None) -> None:
        return super().run(
            token or self.config['startup']['token']
        )

    async def close(self):
        await super().close()


if __name__ == '__main__':
    keep_alive()

    bot = MyBot()
    bot.run()
