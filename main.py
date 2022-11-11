import discord
import os
import logging
from discord.ext import commands
from pymongo import MongoClient
# from tools import _db, embeds
from dotenv import load_dotenv

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

intents = discord.Intents.default()
intents.members = True
logging.basicConfig(level=logging.INFO)


def get_prefix(bot, message):
    global dbclient
    if not message.guild:
        return commands.when_mentioned_or("ax ")(bot, message)
    prefix = "ax "
    collection = db["Prefix"]
    for x in collection.find({"server_id":message.guild.id}):
        prefix=x["prefix"]
    return commands.when_mentioned_or(prefix)(bot, message)


client = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True)

client.remove_command("help")


@client.event
async def on_ready():
    print('Bot is online.')
    game = discord.Game("ax help")
    await client.change_presence(status=discord.Status.online, activity=game)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

load_dotenv('.env')
client.run(os.getenv('TOKEN'))
