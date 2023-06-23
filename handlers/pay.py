import os
import disnake
from config.colors import CMD_SUC, CMD_ERR
from disnake.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]


class PayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = MongoClient(MONGO_URI)
        self.table = self.database["bze5ksolyt7no2d"]
        self.db = self.table["profile"]

    @commands.slash_command(
        name="pay",
        description="перевести деньги"
    )
    async def pay(self, inter, member: disnake.Member, amount: int):
        userID = inter.author.id
        bankUser = self.db.find_one({"id": member.id})["bank"]
        bankMe = self.db.find_one({"id": userID})["bank"]

        if amount > bankMe:
            await inter.send(embed=disnake.Embed(description="Не хватает денег!", color=CMD_ERR))

        if bankMe >= amount:
            emb = disnake.Embed(
                description=f"{inter.author} перевел {amount} пользователю {member}\n",
                color=CMD_SUC
            )
            emb.set_author(name=inter.author.name, icon_url=inter.author.display_avatar)

            self.db.update_one({"id": userID}, {"$set": {"bank": bankMe - amount}})
            self.db.update_one({"id": member.id}, {"$set": {"bank": bankUser + amount}})

            await inter.send(embed=emb)


def setup(bot):
    bot.add_cog(PayCommand(bot))
