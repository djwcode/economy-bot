import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

from config.colors import CMD_SUC

load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]


class ProfileCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = MongoClient(MONGO_URI)
        self.table = self.database["bze5ksolyt7no2d"]
        self.db = self.table["profile"]

    @commands.slash_command(
        name="profile",
        description="посмотреть профиль"
    )
    async def profile(self, inter,
                      member: disnake.Member = commands.Param(default=None)):
        if member is None:
            member = inter.author

        bankData = self.db.find_one({"id": member.id})["bank"]
        moneyData = self.db.find_one({"id": member.id})["money"]
        itemsData = self.db.find_one({"id": member.id})["items"]
        repData = self.db.find_one({"id": member.id})["rep"]

        emb = disnake.Embed(
            title="Профиль",
            description=f"Профиль пользователя {member.mention} \n",
            color=CMD_SUC
        )
        emb.add_field(name="", value="**Деньги**", inline=False)
        emb.add_field(name="- Банк:", value=f"<:icons_coin:1119346308482863105> {bankData}", inline=True)
        emb.add_field(name="- Наличными:", value=f"<:icons_coin:1119346308482863105> {moneyData}", inline=True)
        emb.add_field(name="", value="**Инвентарь**", inline=False)
        emb.add_field(name="- Предметы:", value=itemsData, inline=True)
        emb.add_field(name="- Репутация:", value=repData, inline=True)
        emb.set_thumbnail(url=member.display_avatar)
        emb.set_author(name=member.name, icon_url=member.display_avatar)

        await inter.response.send_message(embed=emb)


def setup(bot):
    bot.add_cog(ProfileCommand(bot))
