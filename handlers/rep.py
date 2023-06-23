import os
import disnake
from config.colors import CMD_SUC, CMD_ERR
from disnake.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from disnake.ext.commands import CommandOnCooldown


load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]


class RepCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = MongoClient(MONGO_URI)
        self.table = self.database["bze5ksolyt7no2d"]
        self.db = self.table["profile"]

    @commands.slash_command(
        name="rep",
        description="дать репутацию"
    )
    @commands.cooldown(1, 60 * 60)
    async def rep(self, inter, member: disnake.Member):
        userID = inter.author.id
        repData = self.db.find_one({"id": member.id})["rep"]

        if member.id == userID:
            await inter.send(embed=disnake.Embed(description="Нельзя выдать самому себе репутацию!", color=CMD_ERR))

        if member.id != userID:
            emb = disnake.Embed(
                description=f"{inter.author.mention} перевел 1 репутацию пользователю {member.mention}\n",
                color=CMD_SUC
            )
            emb.set_author(name=inter.author.name, icon_url=inter.author.display_avatar)

            self.db.update_one({"id": member.id}, {"$set": {"rep": repData + 1}})

            await inter.send(embed=emb)

    @rep.error
    async def my_command_error(self, inter, error):
        timeCool = int(error.retry_after)
        timeNext = f"<t:{int(datetime.now().timestamp() + timeCool)}:R>"
        if isinstance(error, CommandOnCooldown):
            emb = disnake.Embed(
                description=f"Вы уже использовали эту команду. Повторно можно {timeNext}",
                color=CMD_ERR
            )
            emb.set_author(name=inter.author.name, icon_url=inter.author.display_avatar)
            await inter.send(embed=emb)


def setup(bot):
    bot.add_cog(RepCommand(bot))
