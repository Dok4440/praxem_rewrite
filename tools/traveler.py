import os

import discord
from dotenv import load_dotenv
from pymongo import MongoClient
from tools import _json

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


def cost_calculation(current_location, destination):

    current_district = current_location.split(sep=",")[0]
    destination_district = destination.split(sep=",")[0]

    cost = 4                # default travel cost (within district)

    if current_district != destination_district:
        cost += 21          # inter-district travel cost

    return cost


def get_current_location(ctx):
    location = None

    profile_collection = db["Profile"].find({"_id": ctx.author.id})
    for i in profile_collection:
        location = i["location"]

    return location


def get_current_area(location):
    area_dictionary = {}

    maps_collection = db["Maps"].find({"_id": location})
    for x in maps_collection:
        area_dictionary = {
            "world_map": x["world_map_pointer_img"],
            "district_map": x["district_pointer_img"],
            "area_map": x["area_map_img"],
            "difficulty": x["difficulty"],
            "description": x["description"],
            "min_level": x["minimum_level"]
        }

    return area_dictionary


def get_district_areas(district):
    area_list = []

    maps_collection = db["Maps"].find({})
    for x in maps_collection:
        if x["_id"].startswith(district):
            area_list.append({
                "location": x["_id"],
                "world_map": x["world_map_pointer_img"],
                "district_map": x["district_pointer_img"],
                "area_map": x["area_map_img"],
                "difficulty": x["difficulty"],
                "description": x["description"],
                "min_level": x["minimum_level"]
            })

    return area_list


def one_map_embed(ctx, area, district, difficulty, description, min_level, zoom):

    area = area.replace("_", " ")
    district = district.replace("_", " ")
    district = " ".join([
        word.capitalize()
        for word in district.split(" ")
    ])

    em = discord.Embed(color=0xadcca6, title=f"{ctx.author.name}'s location",
                       description=f"🌍 **__{district}__** *— lv. {min_level} zone*")

    em.add_field(name=f"Area: {area.capitalize()}", value=f"{description}"
                                                          f"\n\nDanger: **{difficulty}**"
                                                          f"\n[Drops, materials, actions, etc. JSON here]")
    em.set_image(url=zoom)

    return em


def travel_map_embed(ctx, area_dictionary, district, current_area):
    area = area_dictionary["location"].split(sep=",")[1]
    district_map = area_dictionary["district_map"]
    difficulty = area_dictionary["difficulty"]
    description = area_dictionary["description"]
    min_level = area_dictionary["min_level"]

    if area == current_area:
        title = f"{ctx.author.name}'s current location"
    else:
        title = "Travel here?"

    area = area.replace("_", " ")
    district = district.replace("_", " ")
    district = " ".join([
        word.capitalize()
        for word in district.split(" ")
    ])

    em = discord.Embed(color=0xadcca6, title=title,
                       description=f"🌍 **__{district}__** *— lv. {min_level} zone*")

    em.add_field(name=f"Area: {area.capitalize()}", value=f"{description}"
                                                          f"\n\nDanger: **{difficulty}**"
                                                          f"\n[Drops, materials, actions, etc. JSON here]")
    em.set_image(url=district_map)

    return em


