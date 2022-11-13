# from tools.combat import miss_counter
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import discord
from tools import _db, _json

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


def w_page(weapon: str, av, fetchClient):
    stats_list  = _db.get_weapon_stats_list(weapon.lower())
    emote       = fetchClient.get_emoji(_json.get_emote_id(weapon))
    weapon_name = weapon.lower().capitalize()
    weapon_art  = _json.get_art()[weapon]

    em=discord.Embed(color=0xadcca6, title=f"{emote} {weapon_name}")
    em.set_author(name="Let's choose some weapons!", icon_url=av)
    em.add_field(name="Stats", value=stats_list)
    em.set_thumbnail(url=weapon_art)
    # em.set_footer(text="If you want this weapon, click the button below.")

    return em
