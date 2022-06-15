from datetime import datetime, timedelta
import discord
from discord.ext import commands
from random import choice


class Xp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_xp = datetime.now()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        
        msg_time = datetime.now()
        if msg_time - self.last_xp > timedelta(seconds=10):
            coinsToAdd = choice(range(150))
            print("Added {} coins to balance!".format(coinsToAdd))
            if message.author not in self.bot.coin_amts.keys():
                self.bot.coin_amts[message.author] = [0, 0]
            self.bot.coin_amts[message.author][0] += coinsToAdd
            # await message.reply('You get {} coins!'.format(choice(range(200))))
            self.last_xp = msg_time

async def setup(bot):
    await bot.add_cog(Xp(bot))        