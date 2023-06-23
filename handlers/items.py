import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from config.colors import CMD_SUC

load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]
botic = commands.Bot(command_prefix=commands.when_mentioned)


class ItemsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = MongoClient(MONGO_URI)
        self.table = self.database["bze5ksolyt7no2d"]
        self.db = self.table["profile"]
        self.items = self.table["items"]

    @commands.slash_command(
        name="item-setup",
        description="создать предмет"
    )
    async def itemsetup(self, inter,
                        name: str,
                        price: int,
                        limit: int = commands.Param(default="Бесконечно"),
                        description: str = commands.Param(default="Не указано")
                        ):
        time_created = f"<t:{int(datetime.now().timestamp())}:F>"

        emb = disnake.Embed(
            description="Создан предмет",
            color=CMD_SUC
        )
        emb.add_field(name="Название:", value=name, inline=False)
        emb.add_field(name="Цена:", value=price, inline=False)
        emb.add_field(name="Лимит:", value=limit, inline=False)
        emb.add_field(name="Описание:", value=description, inline=False)
        emb.add_field(name="Создан:", value=time_created)
        emb.set_author(name=inter.author.name, icon_url=inter.author.display_avatar)
        emb.set_footer(text="Это сообщение будет удалено через 15 секунд")

        dataItem = {
            "name": name,
            "price": price,
            "description": description,
            "limit": limit,
            "created_at": datetime.today()
        }
        self.items.insert_one(dataItem)
        print(f"Добавлен предмет {name} с ценой {price}")

        await inter.response.send_message(embed=emb, ephemeral=True, delete_after=15.0)


def setup(bot):
    bot.add_cog(ItemsCommand(bot))
