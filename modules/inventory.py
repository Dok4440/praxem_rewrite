import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from database import db_items

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
    async def item(self, ctx, *, item: discord.Option(choices=db_items.list_items())):

        item_id = db_items.get_item_id(item)
        item_info = db_items.get_item_all_info(item_id)
        item_amount = db_items.get_user_item_amount(ctx.author.id, item_id)

        description     = item_info[2]
        cost            = item_info[3]
        image_url       = item_info[4]
        emote           = self.bot.get_emoji(item_info[5])
        item_type       = item_info[6]
        sell_value      = item_info[7]
        quote           = item_info[8]
        sellable        = item_info[9]

        top_description = ""
        thumbnail = image_url

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
