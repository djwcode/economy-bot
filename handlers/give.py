import os
import disnake
from config.colors import CMD_SUC, CMD_ERR
from disnake.ext import commands
from disnake.ui import View
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]


class GiveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = MongoClient(MONGO_URI)
        self.table = self.database["bze5ksolyt7no2d"]
        self.db = self.table["profile"]

    @commands.slash_command(
        name="give",
        description="выдать деньги"
    )
    async def give(self, inter, member: disnake.Member, amount: int):
        userID = inter.author.id
        bankUser = self.db.find_one({"id": member.id})["bank"]
        bankMe = self.db.find_one({"id": userID})["bank"]

        if amount > bankMe.bank:
            await inter.response.send_message(embed=disnake.Embed(description="Не хватает денег!", color=CMD_ERR))

        if bankMe.bank >= amount:
            emb = disnake.Embed(
                description=f"{inter.author.mention} перевел {amount} пользователю {member.mention}\n",
                color=CMD_SUC
            )
            emb.set_author(name=inter.author.name, icon_url=inter.author.display_avatar)

            self.db.update_one({"id": member.id}, {"$set": {"bank": amount + bankUser}})
            self.db.update_one({"id": userID}, {"$set": {"bank": bankMe - amount}})

            await inter.response.send_message(embed=emb)


def setup(bot):
    bot.add_cog(GiveCommand(bot))
