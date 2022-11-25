print()
print("---------")
print("PRAXEM RESTART")
print("---------")

import logging
import os
from database import tables, db_items

import discord
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.ERROR)
pr_client = discord.Bot(intents=discord.Intents.all())
load_dotenv('.env')

# sync praxem database
tables.sync_database()


@pr_client.event
async def on_ready():
    print('Project Ax is online.')

    if os.getenv('ISMAIN') == "True":
        game = discord.Game("/help")
    else:
        game = discord.Game("BETA")

    await pr_client.change_presence(status=discord.Status.do_not_disturb, activity=game)


@pr_client.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error, ephemeral=True)
        print("Cooldown error logged.")

    elif isinstance(error, commands.CheckFailure):
        await ctx.respond("Error: you're not bot admin. FYI: " +
                          "this command is __only__ available in the official Praxem server, " +
                          "so you won't be bothered by it anywhere else.", ephemeral=True)

        print("Check failure error logged.")

    else:
        await ctx.respond(error, ephemeral=True)
        raise error


for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        pr_client.load_extension(f'modules.{filename[:-3]}')

pr_client.run(os.getenv('TOKEN'))
