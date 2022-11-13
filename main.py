import logging
import os

import discord
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
pr_client = discord.Bot(intents=discord.Intents.all())
load_dotenv('.env')


@pr_client.event
async def on_ready():
    print('Bot is online.')

    if os.getenv('ISMAIN') == "True":
        game = discord.Game("/help")
    else:
        game = discord.Game("BETA")

    await pr_client.change_presence(status=discord.Status.do_not_disturb, activity=game)


for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        pr_client.load_extension(f'modules.{filename[:-3]}')

pr_client.run(os.getenv('TOKEN'))
