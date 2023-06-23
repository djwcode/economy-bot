import os
from datetime import datetime
from random import randint

import disnake
from disnake.ext import commands
from disnake.ext.commands import CommandOnCooldown
from dotenv import load_dotenv
from pymongo import MongoClient

from config.colors import CMD_SUC, CMD_ERR

load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]


class WorkCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = MongoClient(MONGO_URI)
        self.table = self.database["bze5ksolyt7no2d"]
        self.db = self.table["profile"]

    @commands.slash_command(
        name="work",
        description="заработать деньги"
    )
    @commands.cooldown(1, 120 * 60)
    async def work(self, inter):
        userID = inter.author.id
        moneyData = self.db.find_one({"id": inter.author.id})["money"]
        money = randint(0, 100)

        emb = disnake.Embed(
            description=f"Вы успешно заработали {money} <:icons_coin:1119346308482863105>",
            color=CMD_SUC
        )
        emb.set_author(name=inter.author.name, icon_url=inter.author.display_avatar)

        self.db.update_one({"id": userID}, {"$set": {"money": moneyData + money}})

        await inter.send(embed=emb)

    @work.error
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
    bot.add_cog(WorkCommand(bot))
