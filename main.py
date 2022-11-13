import logging
import os

import discord
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
pr_client = discord.Bot(intents=discord.Intents.all())


@pr_client.event
async def on_ready():
    print('Bot is online.')
    game = discord.Game("/help")
    await pr_client.change_presence(status=discord.Status.do_not_disturb, activity=game)


for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        pr_client.load_extension(f'modules.{filename[:-3]}')

load_dotenv('.env')
pr_client.run(os.getenv('TOKEN'))
