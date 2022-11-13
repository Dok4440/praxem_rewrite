import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from tools import _db, _json, tools, embeds
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import asyncio
import requests
import string

import tools.tools

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


class Profile(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @commands.Cog.listener()
    async def on_ready(self):
        print('profile.py -> on_ready()')

    @discord.slash_command(
        name = "profile",
        description = "view your Project Ax profile",
        guild_only = True
    )
    async def profile(self, ctx):

        target = ctx.author.id

        # CHECK IF PROFILE EXISTS
        check = db["Profile"].count_documents({"_id": target})
        if check == 0:
            em = discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** "
                                                           f"I couldn't find any profile linked to your account. "
                                                           f"You currently __cannot__ make one as the bot is in its "
                                                           f"beta stage.")

            await ctx.respond(embed=em)
            return

        age = "N/A"
        district = "N/A"
        friend_id = "N/A"
        gender = "N/A"
        height = "N/A"
        world = "N/A"
        xp = "N/A"
        bio = "N/A"

        profile = db["Profile"].find({"_id": target})
        for b in profile:
            age = b["age"]
            district = b["district"]
            friend_id = b["friend_id"]
            gender = b["gender"]
            height = b["height"]
            world = b["world"]
            xp = b["xp"]
            bio = b["bio"]

        main_weapon = _db.get_weapons(target)[0]
        secondary_weapon = _db.get_weapons(target)[1]

        if bio == "":
            bio = "no bio set, configure this with /settings"

        """ badges """
        badges_string = ""
        badges = ""

        try:
            badges = _db.get_badges(target)
            badges = _db.split_badges(badges)

            for i in range(0, len(badges)):
                badges_string += f"{self.bot.get_emoji(_json.get_emote_id(badges[i]))} "
        except:
            pass

        em = discord.Embed(description=f"Bio: {bio}\n{badges_string}", color=0xadcca6)
        em.set_author(name=f"{ctx.author.name}'s profile", url=ctx.author.avatar)

        em.add_field(name="Info Card",  value=f"Gender: {gender}\n"
                                              f"Height: {height}\n"
                                              f"Age: {age}\n "
                                              f"Friend ID: {friend_id}", inline=False)

        em.add_field(name="Region",     value=f"World: {world}\n"
                                              f"District: {district}", inline=False)

        em.add_field(name="Level",      value=f"Player Level: `{xp}`\n"
                                              f"Primary Weapon: `{main_weapon}`\n"
                                              f"Secondary Weapon: `{secondary_weapon}`", inline=False)


        try:
            em.set_thumbnail(url=_json.get_art()[badges[0]])
        except:
            em.set_thumbnail(url=_json.get_art()["bot_icon_greatsword"])

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Profile(client))
