from disnake.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
import disnake
import os


load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]
database = MongoClient(MONGO_URI)
table = database["bze5ksolyt7no2d"]
db = table["profile"]


class ProfileLoad(disnake.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("События загружены")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        money = 0
        bank = 0
        rep = 0
        items = "нет предметов"
        user = {
            "id": member.id,
            "name": member.name,
            "money": money,
            "bank": bank,
            "rep": rep,
            "items": items
        }
        result = db.insert_one(user)
        print(f"Добавлен пользователь {user['name']} с айди {result.inserted_id}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        query = {"id": member.id}
        result = db.delete_one(query)

        if result.deleted_count > 0:
            print(f"Удален пользователь {member.name} с айди {member.id}")
        else:
            print(f"Пользователь {member.name} с айди {member.id} не найден")


def setup(bot):
    bot.add_cog(ProfileLoad(bot))
