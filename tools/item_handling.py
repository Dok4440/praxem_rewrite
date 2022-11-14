import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


def create_inventory(id, main_weapon, secondary_weapon):
    db["Inventory"].insert_one({"_id": id,
                                "main_weapon": main_weapon,
                                "secondary_weapon": secondary_weapon,
                                "main_weapon_xp": 0,
                                "secondary_weapon_xp": 0,
                                "balance": 0,
                                "apple": 0,
                                "teleporting_potion": 0
                                })


def inventory_list():
    return ["main_weapon", "secondary_weapon", "main_weapon_xp",
            "secondary_weapon_xp", "balance", "apple", "teleporting_potion"]


def decorate_inventory_items(list):
    items_to_pop = []

    for i in range(len(list)):
        li = list[i].split(': ')

        '''# INSERT EMOTE HERE TOO LATER'''
        emote = '🍎'
        name = li[0]
        value = li[1]

        li = f"{emote} {name.capitalize()}\n— *Amount: `{value}`*"
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
