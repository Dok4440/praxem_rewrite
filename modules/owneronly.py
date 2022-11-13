import os
import random
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from tools import tools

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


async def is_owner(ctx):
    return ctx.author.id == 387984284734062592


class Owneronly(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @commands.Cog.listener()
    async def on_ready(self):
        print('owneronly.py -> on_ready()')

        if os.getenv('ISMAIN') == "True":
            msg = db["DieMessage"].find({"_id": 1})
            for a in msg:
                channel = a["channel_id"]
                user_name = a["user_name"]
                user_discrim = a["user_discrim"]
                time_on_die = a["time_on_die"]

            time_now = datetime.now()
            restart_time = (time_now - time_on_die).total_seconds()

            em = discord.Embed(color=0xadcca6, description=(
                f"**{user_name}#{user_discrim}** It took me {round(restart_time, 2)} seconds to restart."))

            ch = self.bot.get_channel(channel)
            await ch.send(embed=em)

    @discord.slash_command(
        name="die",
        description="Only Dok#4440 can do this. Command will only show up in this server.",
        guild_only=True,
        default_member_permissions=discord.Permissions(permissions=8),
        guild_ids=["803957895603027978"]
    )
    @commands.check(is_owner)
    async def die(self, ctx, *, message: discord.Option(str) = None):
        em = discord.Embed(color=0xadcca6)
        time_on_die = datetime.now()

        collection = db["DieMessage"]
        collection.update_one({"_id": 1}, {
            "$set": {"channel_id": ctx.channel.id, "user_name": ctx.author.name,
                     "user_discrim": ctx.author.discriminator, "time_on_die": time_on_die}}, upsert=True)

        if message == "pull":
            if (os.system("sh rAIOmp.sh") / 256) > 1:
                var = os.system("sh rAIOmp.sh")  # this will run os.system() AGAIN.
                await ctx.respond(
                    f"Couldn't run `rAIOmp.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
            else:
                em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Updating Project Ax.."
                await ctx.respond(embed=em)

        else:
            if (os.system("sh rAIOm.sh") / 256) > 1:
                var = os.system("sh rAIOm.sh")  # this will run os.system() AGAIN.
                await ctx.respond(
                    f"Couldn't run `rAIOm.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
            else:
                em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Shutting Down.."
                await ctx.respond(embed=em)

    @die.error
    async def die_error(self, ctx, error):
        await ctx.respond("Error: you're not bot owner. FYI: " +
                          "this command is __only__ available in the official Praxem server, " +
                          "so you won't be bothered by it anywhere else.")

    @discord.slash_command(
        name="vsay",
        description="Only Dok#4440 can do this. Command will only show up in this server.",
        default_member_permissions=discord.Permissions(permissions=8),
        guild_ids=["803957895603027978"]
    )
    async def vsay(self, ctx, *, message: discord.Option(str)):
        emotes = [847124036206592020, 847124109875478591,
                  847124082541854781, 847124132746756159]

        emote = random.choice(emotes)
        await ctx.send(f"{self.bot.get_emoji(emote)} `{tools.get_version()}` — {message}")


def setup(client):
    client.add_cog(Owneronly(client))
