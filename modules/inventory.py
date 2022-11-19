import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

from tools import _json, item_handling, interaction

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
        name="bag",
        description="View your bag.",
        guild_only=True
    )
    async def bag(self, ctx):
        target = ctx.author.id

        check = db["Inventory"].count_documents({"_id": target})
        if check == 0:
            em = discord.Embed(color=0xadcca6,
                               description=f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Create one with `/profile`")
            await ctx.respond(embed=em)
            return

        balance = 0

        item = db["Inventory"].find({"_id": ctx.author.id})
        for i in item:
            balance = i["balance"]

        await ctx.respond(embed=item_handling.pager(ctx, "all items", self.bot, balance),
                          view=interaction.BagOptions(ctx, self.bot, balance))

    @discord.slash_command(
        name="item",
        description="View detailed information about an item",
        guild_only=True
    )
    async def item(self, ctx, *, item: discord.Option(choices=item_handling.inventory_list())):
        item_amount = 0
        inventory = db["Inventory"].find({"_id": ctx.author.id})
        for i in inventory:
            item_amount = i[item]

        description = "N/A - no `db[Items]` ?"
        cost = 0
        thumbnail = _json.get_art()["bot_icon_longbow"]
        emote = "❓"
        item_type = "no_type_found"
        sell_value = 0
        quote = ""
        top_description = ""
        sellable = False

        try:
            items = db["Items"].find({"_id": item})
            for info in items:
                description = info["description"]
                cost = info["cost"]
                thumbnail = info["image_url"]
                emote = self.bot.get_emoji(info["emote_id"])
                item_type = info["item_type"]
                sell_value = info["sell_value"]
                quote = info["quote"]
                sellable = info["sellable"]

        except Exception:
            pass

        if sell_value == 0 or not sellable:
            sell_value = "can't be sold"

        if item_amount > 1:
            amount_string = f"You have this item {item_amount} times."
        elif item_amount == 1:
            amount_string = f"You have this item {item_amount} time."
        else:
            amount_string = f"You don't have this item."

        if quote != "" and quote is not None:
            top_description = f"> *{quote}*\n\n{amount_string}"
        else:
            top_description = amount_string

        ''' CREATE EMBED'''
        em = discord.Embed(color=0xadcca6, title=f"{emote} {item.replace('_', ' ')}",
                           description=top_description)

        em.add_field(name="Value", value=f"`/shop` cost: **{cost}**\n`/sell` value: **{sell_value}**", inline=False)
        em.add_field(name="Description", value=description, inline=False)
        em.set_thumbnail(url=thumbnail)
        em.set_footer(text=f"type: {item_type}")

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Inventory(client))
