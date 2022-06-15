import discord
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        embed = discord.Embed(
            title='Ignoring exception in command {}:'.format(ctx.command),
            color=discord.Color.dark_purple()
        )
        
        # embed.description = '```py\n{}\n```'.format(traceback.format_exc())
        embed.description = str(error)

        errChannel = self.bot.get_channel(965762182124011541)
        await errChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))