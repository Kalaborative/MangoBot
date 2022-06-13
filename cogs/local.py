import discord
from discord.ext import commands
from discord.ui import Button, View


class Local(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        button1 = Button(label='Click me!', style=discord.ButtonStyle.green)
        button2 = Button(emoji='🍦', style=discord.ButtonStyle.primary)
        button3 = Button(label='Go to Google', url='https://google.com')
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        await ctx.send("Hi!", view=view)

    @commands.command()
    async def bal(self, ctx):
        if ctx.author not in self.bot.coin_amts.keys():
            self.bot.coin_amts[ctx.author] = [0, 0]

        wallet = self.bot.coin_amts[ctx.author][0]
        bank = self.bot.coin_amts[ctx.author][1]

        e = discord.Embed(
            color=discord.Color.blue(),
            title=f'{ctx.author}',
            description=f'Wallet: {wallet} | Bank {bank}'
        )
        await ctx.send(embed=e)

    @commands.command()
    async def addbal(self, ctx, amt: int):
        q_author = ctx.author
        if ctx.author not in self.bot.coin_amts.keys():
            self.bot.coin_amts[q_author] = [0, 0]
        
        currentBal = self.bot.coin_amts[q_author][0]
        newBal = currentBal + amt
        self.bot.coin_amts[q_author][0] = newBal
        await ctx.send('{} coins added!'.format(amt))

async def setup(bot):
    await bot.add_cog(Local(bot))
