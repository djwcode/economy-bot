from disnake.ext import commands
from disnake import Intents
from dotenv import load_dotenv
from pymongo import MongoClient

from config.colors import CMD_LOG
import os

load_dotenv()
TOKEN = os.environ['TOKEN']
MONGO_URI = os.environ['MONGO_URI']


class Bot:
    bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=Intents.all())

    for filename in os.listdir("./handlers"):
        if filename.endswith(".py"):
            bot.load_extension(f"handlers.{filename[:-3]}")

    for filename in os.listdir("./events"):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"events.{filename[:-3]}")

    bot.run(TOKEN)
