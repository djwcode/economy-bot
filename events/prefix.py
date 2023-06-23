import disnake
from disnake.ext import commands
from config.colors import CMD_ERR


class PrefixEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            emb = disnake.Embed(
                description="Не найдена команда. Используйте `слэш-команды`",
                color=CMD_ERR
            )
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=emb)
        else:
            print(error)


def setup(bot):
    bot.add_cog(PrefixEvent(bot))
