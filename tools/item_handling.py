import os

import discord
from dotenv import load_dotenv
from pymongo import MongoClient
from tools import _json

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


def create_inventory(id, main_weapon, secondary_weapon):
    item_list = inventory_list()[5:]

    dictionary = {"_id": id,"main_weapon": main_weapon,"secondary_weapon": secondary_weapon,
                  "main_weapon_xp": 0,"secondary_weapon_xp": 0,"balance": 0}

    for i in range(len(item_list)):
        dictionary[item_list[i]] = 0

    db["Inventory"].insert_one(dictionary)


def inventory_list():
    li = []
    item = db["Items"].find({"_id": "item_definitions"})
    for i in item:
        li = i["item_list"]

    return li


def item_list(type, target):

    if type.lower() == "all items":
        item_names = inventory_list()
    else:
        item_names = db["Items"].find({"item_type": type}).distinct("_id")

    inventory = db["Inventory"].find({"_id": target})
    items = []

    for document in inventory:
        for item in item_names:
            item_name = item.replace("_", " ")
            item_value = document[item]
            items.append(f"{item_name}: {item_value}")

    return items


def get_item_emote(item, bot):
    emote = '❓'

    items = db["Items"].find({"_id": item})
    for i in items:
        emote = bot.get_emoji(i["emote_id"])

    return emote


def decorate_inventory_items(list, bot):
    items_to_pop = []

    for i in range(len(list)):
        li = list[i].split(': ')

        '''# INSERT EMOTE HERE TOO LATER'''
        name = li[0]
        value = li[1]
        emote = get_item_emote(name.replace(" ", "_"), bot)

        li = f"{emote} {name}\n— *Amount: `{value}`*"
        list[i] = li

        '''if value = 0, add to pop list'''
        if int(value) == 0:
            items_to_pop.append(i)

    '''items to remove if value = 0'''
    for i in range(len(items_to_pop)):
        list.pop(items_to_pop[i] - i)

    return list


def decorate_inventory_list(list):
    # main weapon, second weapon, main weapon xp, secondary weapon xp, balance
    for i in range(0, 5):
        list[i] = list[i].split(': ')[1]

    # main and secondary weapon strings
    list[0] = f"*{list[2]} XP* — **{list[0].capitalize()}**"
    list[1] = f"*{list[3]} XP* — **{list[1].capitalize()}**"

    return list


def pager(ctx, type, bot, balance):
    if type == "Consumables":
        items = item_list("consumable", ctx.author.id)
    elif type == "Collectables":
        items = item_list("collectable", ctx.author.id)
    else:
        items = item_list("all items", ctx.author.id)

    items = decorate_inventory_items(items, bot)

    pages = ["page_1"]
    pages_amount = len(items) // 8
    for i in range(pages_amount):
        pages.append(f"page_{i+2}")

    if pages_amount > 0:
        pass
        # for later!

    else:
        pages[0] = ""

        if len(items) == 0:
            if type == "Consumables" or type == "Collectables":
                pages[0] += "You don't have any items of this type."
            else:
                pages[0] += "You don't have any items."
        else:
            for item in items:
                pages[0] += "{}\n\n".format(item)

    em = discord.Embed(color=0xadcca6, title=f"{ctx.author.name}'s Bag",
                       description=f"**Balance: {balance}** 💸")

    em.add_field(name="ITEMS", value=pages[0])
    em.set_thumbnail(url=_json.get_art()["bot_icon_longbow"])
    em.set_footer(text="do /item [item] to see detailed information.")

    return em
