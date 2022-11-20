import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

from tools import _json, item_handling, interaction, embeds

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


class Navigation(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @commands.Cog.listener()
    async def on_ready(self):
        print('navigation.py -> on_ready()')

    @discord.slash_command(
        name="map",
        description="Where am I?",
        guild_only=True
    )
    async def map(self, ctx):
        location = None

        profile_collection = db["Profile"].find({"_id": ctx.author.id})
        for i in profile_collection:
            location = i["location"]

        world_map = None
        district_map = None
        area_map = None
        difficulty = None
        description = None
        min_level = None

        maps_collection = db["Maps"].find({"_id": location})
        for x in maps_collection:
            world_map = x["world_map_pointer_img"]
            district_map = x["district_pointer_img"]
            area_map = x["area_map_img"]
            difficulty = x["difficulty"]
            description = x["description"]
            min_level = x["minimum_level"]

        zoom_list = [world_map, district_map, area_map]

        location = location.split(sep=",")
        district = location[0]
        area = location[1]

        await ctx.respond(embed=embeds.maps_embed(ctx, area, district,
                                                  difficulty, description,
                                                  min_level, zoom_list[2]),

                          view=interaction.NavigationButtons(ctx, area, district,
                                                             difficulty, description,
                                                             min_level, zoom_list, self.bot))


def setup(client):
    client.add_cog(Navigation(client))
