import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from config.colors import CMD_SUC, CMD_ERR

load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]


class DepositCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = MongoClient(MONGO_URI)
        self.table = self.database["bze5ksolyt7no2d"]
        self.db = self.table["profile"]

    @commands.slash_command(
        name="deposit",
        description="положить деньги в банк"
    )
    async def deposit(self, inter, amount: int):
        userID = inter.author.id
        bankData = self.db.find_one({"id": userID})["bank"]
        moneyData = self.db.find_one({"id": userID})["money"]

        if amount > moneyData:
            await inter.send(embed=disnake.Embed(description="Не хватает денег!", color=CMD_ERR))

        if moneyData >= amount:
            emb = disnake.Embed(
                description=f"{inter.author.mention} положил в свой банковский счет {amount} <:icons_coin:1119346308482863105>\n",
                color=CMD_SUC
            )
            emb.set_author(name=inter.author.name, icon_url=inter.author.display_avatar)

            self.db.update_one({"id": userID}, {"$set": {"money": moneyData - amount}})
            self.db.update_one({"id": userID}, {"$set": {"bank": bankData + amount}})

            await inter.send(embed=emb)


def setup(bot):
    bot.add_cog(DepositCommand(bot))
