import discord
from discord.ext import commands
from discord import Emoji
from pathlib import Path
from discord.ui import Button, View
from random import choice

# coin emoji code is <:mcoin:985997690687094804>
# check emoji code is <:mcheck:986462579260006430>

def num(n: int) -> str:
    return f'{n:,}'

class Casino(commands.Cog):
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
            description=f'\u200E\n **Total** - {num(wallet + bank)} <:mcoin:985997690687094804>\n\u200E'
        )

        fp = Path(__file__).resolve().parent / "assets" / "bank_1.png"
        file = discord.File(fp, filename='image.png')
        e.set_footer(text='Earn coins by chatting or voice calling')
        e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
        e.set_thumbnail(url="attachment://image.png")
        e.add_field(name='Wallet', value=f'{num(wallet)} <:mcoin:985997690687094804>', inline=True)
        e.add_field(name='Bank', value=f'{num(bank)} <:mcoin:985997690687094804>', inline=True)
        await ctx.send(file=file, embed=e)

    @commands.command(aliases=['add'])
    async def addcoins(self, ctx, amt: int):
        q_author = ctx.author
        if ctx.author not in self.bot.coin_amts.keys():
            self.bot.coin_amts[q_author] = [0, 0]
        
        currentBal = self.bot.coin_amts[q_author][0]
        newBal = currentBal + amt
        self.bot.coin_amts[q_author][0] = newBal
        await ctx.send('{} coins added!'.format(num(amt)))
    
    @commands.command(pass_context=True)
    async def debug(self, ctx, emoji: Emoji):
        emb = discord.Embed(description=f'emoji: {emoji}', title=f'emoji: {emoji}')
        emb.add_field(name='id', value=repr(emoji.id))
        emb.add_field(name='name', value=repr(emoji.name))
        await ctx.send(embed=emb)
    
    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amt):
        user_wallet = self.bot.coin_amts[ctx.author][0]
        if amt == 'all':
            to_deposit = user_wallet
            if to_deposit == 0:
                e = discord.Embed(
                    color=discord.Color.yellow(),
                    title='Error!',
                    description='\u200E \nYou cannot deposit less than 1.'
                )

                fp = Path(__file__).resolve().parent / "assets" / "err.png"
                file = discord.File(fp, filename='image.png')
                e.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                e.set_thumbnail(url="attachment://image.png")
                await ctx.send(file=file, embed=e)
            else:
                self.bot.coin_amts[ctx.author][0] = 0
                self.bot.coin_amts[ctx.author][1] += to_deposit
                await ctx.send("**<a:mcheck:986462579260006430> You have deposited {} <:mcoin:985997690687094804> to your bank. **".format(num(to_deposit)))
        else:
            amt = int(amt)
            if amt > self.bot.coin_amts[ctx.author][0]:
                e = discord.Embed(
                    color=discord.Color.yellow(),
                    title='Error!',
                    description='\u200E \nYou only have {} <:mcoin:985997690687094804> in your wallet'.format(self.bot.coin_amts[ctx.author][0])
                )

                fp = Path(__file__).resolve().parent / "assets" / "err.png"
                file = discord.File(fp, filename='image.png')
                e.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                e.set_thumbnail(url="attachment://image.png")
                await ctx.send(file=file, embed=e)
            else:
                self.bot.coin_amts[ctx.author][0] -= amt
                self.bot.coin_amts[ctx.author][1] += amt
                await ctx.send('**<a:mcheck:986462579260006430> You have deposited {} <:mcoin:985997690687094804> to your bank. **'.format(num(amt)))

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amt):
        user_bank = self.bot.coin_amts[ctx.author][1]
        if amt == 'all':
            to_withdraw = user_bank
            if to_withdraw == 0:
                e = discord.Embed(
                    color=discord.Color.yellow(),
                    title='Error!',
                    description='\u200E \nYou cannot withdraw less than 1.'
                )

                fp = Path(__file__).resolve().parent / "assets" / "err.png"
                file = discord.File(fp, filename='image.png')
                e.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                e.set_thumbnail(url="attachment://image.png")
                await ctx.send(file=file, embed=e)
            else:
                self.bot.coin_amts[ctx.author][1] = 0
                self.bot.coin_amts[ctx.author][0] += to_withdraw
                await ctx.send("**<a:mcheck:986462579260006430> You have withdrawn {} <:mcoin:985997690687094804> from your bank. **".format(num(to_withdraw)))
        else:
            amt = int(amt)
            if amt > self.bot.coin_amts[ctx.author][1]:
                e = discord.Embed(
                    color=discord.Color.yellow(),
                    title='Error!',
                    description='\u200E \nYou only have {} <:mcoin:985997690687094804> in your bank'.format(self.bot.coin_amts[ctx.author][1])
                )

                fp = Path(__file__).resolve().parent / "assets" / "err.png"
                file = discord.File(fp, filename='image.png')
                e.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                e.set_thumbnail(url="attachment://image.png")
                await ctx.send(file=file, embed=e)
            else:
                self.bot.coin_amts[ctx.author][1] -= amt
                self.bot.coin_amts[ctx.author][0] += amt
                await ctx.send("**<a:mcheck:986462579260006430> You have withdrawn {} <:mcoin:985997690687094804> to your bank. **".format(num(amt)))

    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx, amt, side):
        cfResult = choice(['heads', 'tails'])
        if amt == 'all':
            gamble_amt = self.bot.coin_amts[ctx.author][0]
            if gamble_amt < 10:
                e = discord.Embed(
                    color=discord.Color.yellow(),
                    title='Error!',
                    description='\u200E \nInvalid bet. The minimum bet is 10 <:mcoin:985997690687094804>'
                )

                fp = Path(__file__).resolve().parent / "assets" / "err.png"
                file = discord.File(fp, filename='image.png')
                e.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                e.set_thumbnail(url="attachment://image.png")
                await ctx.send(file=file, embed=e)
            else:
                if side == 'h':
                    side = 'heads'
                if side == 't':
                    side = 'tails'
                
                if side not in ['heads', 'tails']:
                    await ctx.send("You must choose heads or tails!")
                else:
                    if cfResult == side and cfResult == 'heads':
                        e = discord.Embed(
                            color=discord.Color.green(),
                            title='Coin Flip',
                            description='\u200E \nThe coin flips and lands on...\n**heads** \n\nYou won **{}** <:mcoin:985997690687094804>'.format(num(gamble_amt * 2))
                        )

                        fp = Path(__file__).resolve().parent / "assets" / "cards.png"
                        file = discord.File(fp, filename='image.png')
                        e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                        e.set_thumbnail(url="attachment://image.png")
                        await ctx.send(file=file, embed=e)
                        # await ctx.send('The coin lands on heads. You won {} coins!'.format(num(gamble_amt * 2)))
                        self.bot.coin_amts[ctx.author][0] = gamble_amt * 2
                    elif cfResult == side and cfResult == 'tails':
                        e = discord.Embed(
                            color=discord.Color.green(),
                            title='Coin Flip',
                            description='\u200E \nThe coin flips and lands on...\n**tails** \n\nYou won **{}** <:mcoin:985997690687094804>'.format(num(gamble_amt * 2))
                        )

                        fp = Path(__file__).resolve().parent / "assets" / "cards.png"
                        file = discord.File(fp, filename='image.png')
                        e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                        e.set_thumbnail(url="attachment://image.png")
                        await ctx.send(file=file, embed=e)
                        self.bot.coin_amts[ctx.author][0] = gamble_amt * 2
                    elif cfResult != side and cfResult == 'heads':
                        e = discord.Embed(
                            color=discord.Color.red(),
                            title='Coin Flip',
                            description='\u200E \nThe coin flips and lands on...\n**heads** \n\nYou lost **{}** <:mcoin:985997690687094804>'.format(num(gamble_amt))
                        )

                        fp = Path(__file__).resolve().parent / "assets" / "cards.png"
                        file = discord.File(fp, filename='image.png')
                        e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                        e.set_thumbnail(url="attachment://image.png")
                        await ctx.send(file=file, embed=e)
                        self.bot.coin_amts[ctx.author][0] = 0
                    elif cfResult != side and cfResult == 'tails':
                        e = discord.Embed(
                            color=discord.Color.red(),
                            title='Coin Flip',
                            description='\u200E \nThe coin flips and lands on...\n**tails** \n\nYou lost **{}** <:mcoin:985997690687094804>'.format(num(gamble_amt))
                        )

                        fp = Path(__file__).resolve().parent / "assets" / "cards.png"
                        file = discord.File(fp, filename='image.png')
                        e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                        e.set_thumbnail(url="attachment://image.png")
                        await ctx.send(file=file, embed=e)
                        self.bot.coin_amts[ctx.author][0] = 0
        else:
            try:
                gamble_amt = int(amt)
                if gamble_amt < 10:
                    e = discord.Embed(
                        color=discord.Color.yellow(),
                        title='Error!',
                        description='\u200E \nInvalid bet. The minimum bet is 10 <:mcoin:985997690687094804>'
                    )

                    fp = Path(__file__).resolve().parent / "assets" / "err.png"
                    file = discord.File(fp, filename='image.png')
                    e.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                    e.set_thumbnail(url="attachment://image.png")
                    await ctx.send(file=file, embed=e)
                elif gamble_amt > self.bot.coin_amts[ctx.author][0]:
                    e = discord.Embed(
                        color=discord.Color.yellow(),
                        title='Error!',
                        description='\u200E \nYou do not have sufficient funds in your wallet to do this.'
                    )

                    fp = Path(__file__).resolve().parent / "assets" / "err.png"
                    file = discord.File(fp, filename='image.png')
                    e.set_footer(text='Use `!withdraw <amount>` to withdraw from your bank.')
                    e.set_thumbnail(url="attachment://image.png")
                    await ctx.send(file=file, embed=e)  
                else:
                    if side == 'h':
                        side = 'heads'
                    if side == 't':
                        side = 'tails'
                    
                    if side not in ['heads', 'tails']:
                        await ctx.send("You must choose heads or tails!")
                    else:
                        if cfResult == side and cfResult == 'heads':
                            e = discord.Embed(
                                color=discord.Color.green(),
                                title='Coin Flip',
                                description='\u200E \nThe coin flips and lands on...\n**heads** \n\nYou won **{}** <:mcoin:985997690687094804>'.format(num(gamble_amt * 2))
                            )

                            fp = Path(__file__).resolve().parent / "assets" / "cards.png"
                            file = discord.File(fp, filename='image.png')
                            e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                            e.set_thumbnail(url="attachment://image.png")
                            await ctx.send(file=file, embed=e)
                            # await ctx.send('The coin lands on heads. You won {} coins!'.format(num(gamble_amt * 2)))
                            self.bot.coin_amts[ctx.author][0] += gamble_amt
                        elif cfResult == side and cfResult == 'tails':
                            e = discord.Embed(
                                color=discord.Color.green(),
                                title='Coin Flip',
                                description='\u200E \nThe coin flips and lands on...\n**tails** \n\nYou won **{}** <:mcoin:985997690687094804>'.format(num(gamble_amt * 2))
                            )

                            fp = Path(__file__).resolve().parent / "assets" / "cards.png"
                            file = discord.File(fp, filename='image.png')
                            e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                            e.set_thumbnail(url="attachment://image.png")
                            await ctx.send(file=file, embed=e)
                            self.bot.coin_amts[ctx.author][0] += gamble_amt
                        elif cfResult != side and cfResult == 'heads':
                            e = discord.Embed(
                                color=discord.Color.red(),
                                title='Coin Flip',
                                description='\u200E \nThe coin flips and lands on...\n**heads** \n\nYou lost **{}** <:mcoin:985997690687094804>'.format(num(gamble_amt))
                            )

                            fp = Path(__file__).resolve().parent / "assets" / "cards.png"
                            file = discord.File(fp, filename='image.png')
                            e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                            e.set_thumbnail(url="attachment://image.png")
                            await ctx.send(file=file, embed=e)
                            self.bot.coin_amts[ctx.author][0] -= gamble_amt
                        elif cfResult != side and cfResult == 'tails':
                            e = discord.Embed(
                                color=discord.Color.red(),
                                title='Coin Flip',
                                description='\u200E \nThe coin flips and lands on...\n**tails** \n\nYou lost **{}** <:mcoin:985997690687094804>'.format(num(gamble_amt))
                            )

                            fp = Path(__file__).resolve().parent / "assets" / "cards.png"
                            file = discord.File(fp, filename='image.png')
                            e.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
                            e.set_thumbnail(url="attachment://image.png")
                            await ctx.send(file=file, embed=e)
                            self.bot.coin_amts[ctx.author][0] -= gamble_amt
            except Exception as e:
                ctx.send('Invalid bet.')    

async def setup(bot):
    await bot.add_cog(Casino(bot))
