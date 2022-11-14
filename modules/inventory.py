import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

from tools import interaction, wembeds, _json, _db, tools

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


class Inventory(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @commands.Cog.listener()
    async def on_ready(self):
        print('inventory.py -> on_ready()')

    @discord.slash_command(
        name = "inventory",
        description = "View your inventory",
        guild_only = True
    )
    async def inventory(self, ctx):
        target = ctx.author.id

        check = db["Inventory"].count_documents({"_id": target})
        if check == 0:
            em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Create one with `/profile`")
            await ctx.respond(embed=em)
            return

        # inventory = db["Inventory"].find_one({"_id": target})
        inventory_document = db["Inventory"].find({"_id": target})
        inventory_empty_list = _db.inv_list()

        inventory_list = []

        '''GENERATE LIST'''
        for value in inventory_document:
            for item in inventory_empty_list:
                item_name = item.replace("_", " ")
                item_value = value[item]
                inventory_list.append(f"{item_name}: {item_value}")

        # inventory_list = ['main_weapon: %%', 'secondary_weapon: %%',
        #                   'main_weapon_xp: 0', 'secondary_weapon_xp: 0', 'balance: 0', ....]
        '''DECORATE'''
        inventory_list = tools.decorate_inv_list(inventory_list)

        '''DEFINE ITEMS'''
        main_weapon = inventory_list[0]
        secondary_weapon = inventory_list[1]
        balance = inventory_list[4]

        '''ITEM PAGES'''
        items = inventory_list[5:]
        items = tools.decorate_inv_items(items)

        '''as long as there are no pages (5 per page)'''
        page_1 = ""
        for item in items:
            page_1 += "{}\n\n".format(item)

        '''CREATE EMBED'''
        em=discord.Embed(color=0xadcca6, title=f"{ctx.author.name}'s Inventory",
                         description=f"{main_weapon}\n"
                                     f"{secondary_weapon}\n\n"
                                     f"**Balance: {balance}** 💸")

        em.add_field(name="ITEMS", value=page_1)
        em.set_thumbnail(url=_json.get_art()["bot_icon_longbow"])
        em.set_footer(text="do /item [item] to see detailed information.")

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Inventory(client))