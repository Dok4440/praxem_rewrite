import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

from tools import interaction, traveler

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
        location = traveler.get_current_location(ctx)
        area_dictionary = traveler.get_current_area(location)

        world_map = area_dictionary["world_map"]
        district_map = area_dictionary["district_map"]
        area_map = area_dictionary["area_map"]
        difficulty = area_dictionary["difficulty"]
        description = area_dictionary["description"]
        min_level = area_dictionary["min_level"]

        zoom_list = [world_map, district_map, area_map]

        location = location.split(sep=",")
        district = location[0]
        area = location[1]

        await ctx.respond(embed=traveler.one_map_embed(ctx, area, district,
                                                       difficulty, description,
                                                       min_level, zoom_list[2]),

                          view=interaction.NavigationButtons(ctx, area, district,
                                                             difficulty, description,
                                                             min_level, zoom_list, self.bot))

    @discord.slash_command(
        name = "travel",
        description = "Travel to another area.",
        guild_only = True
    )
    async def travel(self, ctx):
        location = traveler.get_current_location(ctx).split(sep=",")
        district = location[0]

        current_district_area_list = traveler.get_district_areas(district)
        current_area = location[1]

        await ctx.respond(embed=traveler.travel_map_embed(ctx, current_district_area_list[0], district, current_area),
                          view=interaction.TravelButtons(ctx, current_district_area_list, district, current_area))


def setup(client):
    client.add_cog(Navigation(client))
