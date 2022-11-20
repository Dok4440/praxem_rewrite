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
        maps_json = _json.get_map()

        profile_collection = db["Profile"].find({"_id": ctx.author.id})
        for i in profile_collection:
            location = i["location"].split(sep=",")

        district = location[0]
        area = location[1]

        world_map = maps_json["zoom_level_0"][f"world_map_{district}"]
        district_map = maps_json["zoom_level_1"][f"{district}_pointer_{area}"]
        area_map = maps_json["zoom_level_2"][f"{district}_{area}"]

        zoom_list = [world_map, district_map, area_map]
        print(zoom_list)

        await ctx.respond(embed=embeds.maps_embed(ctx, area, district, zoom_list[2]),
                          view=interaction.NavigationButtons(ctx, area, district, zoom_list, self.bot))


def setup(client):
    client.add_cog(Navigation(client))
