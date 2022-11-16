import os
import random
import sys
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from tools import tools, item_handling

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


async def is_team(ctx):
    return ctx.author.id in [387984284734062592, 379223333734187009, 275291823222816768]


class Owneronly(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @commands.Cog.listener()
    async def on_ready(self):
        print('owneronly.py -> on_ready()')

        time_on_die = None
        user_name = None
        user_discrim = None
        channel = None

        collection = db["DieMessage"]
        msg = collection.find({"_id": 1})
        for a in msg:
            channel = a["channel_id"]
            user_name = a["user_name"]
            user_discrim = a["user_discrim"]
            time_on_die = a["time_on_die"]

        collection.update_one({"_id": 1}, {"$set": {"channel_id": 839492558396456990}})

        time_now = datetime.now()
        restart_time = (time_now - time_on_die).total_seconds()

        em = discord.Embed(color=0xadcca6, description=(
            f"**{user_name}#{user_discrim}** it took me {round(restart_time, 2)}s to restart."))

        ch = self.bot.get_channel(channel)
        await ch.send(embed=em)

    @discord.slash_command(
        name="vsay",
        description="Only Dok#4440 can do this. Command will only show up in this server.",
        default_member_permissions=discord.Permissions(permissions=8),
        guild_only = True,
        guild_ids=[803957895603027978]
    )
    @commands.check(is_team)
    async def vsay(self, ctx, *, message: discord.Option(str)):
        emotes = [847124036206592020, 847124109875478591,
                  847124082541854781, 847124132746756159]

        emote = random.choice(emotes)
        await ctx.send(f"{self.bot.get_emoji(emote)} `{tools.get_version()}` — {message}")
        await ctx.respond("Message sent.", ephemeral=True)

    botconfig = discord.SlashCommandGroup("botconfig", "Settings for Project Ax bot admins.",
                                          default_member_permissions=discord.Permissions(permissions=32),
                                          guild_ids=[803957895603027978],
                                          guild_only=True,
                                          )
    add = botconfig.create_subgroup("add", "Add something to the database")
    edit = botconfig.create_subgroup("edit", "Edit something in the database")
    remove = botconfig.create_subgroup("remove", "Remove something from the database")

    @botconfig.command(
        name="die",
        description="Restarts the bot. Add the 'pull' parameter to update."
    )
    @commands.check(is_team)
    async def die(self, ctx):
        em = discord.Embed(color=0xadcca6)
        time_on_die = datetime.now()

        collection = db["DieMessage"]
        collection.update_one({"_id": 1}, {
            "$set": {"channel_id": ctx.channel.id, "user_name": ctx.author.name,
                     "user_discrim": ctx.author.discriminator, "time_on_die": time_on_die}}, upsert=True)

        em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** updating Project Ax.."
        await ctx.respond(embed=em)
        os.execv(sys.executable, ['python'] + sys.argv)

    @add.command(
        name="item",
        description="Adds a new item to all inventories. Use with CAUTION."
    )
    @commands.check(is_team)
    async def add_item(self, ctx, *,
                       name: discord.Option(str, description="One word. e.g. 'one two' becomes one_two."),
                       description: discord.Option(str, description="Provide a description for this item."),
                       cost: discord.Option(int, description="Whole, positive number."),
                       image_url: discord.Option(str, description="Only accepts IMGUR links."),
                       emote_id: discord.Option(str, description="ONLY ID (series of numbers)"),
                       item_type: discord.Option(choices=["collectable", "consumable", "sellable"]),
                       sell_value: discord.Option(int, description="Only if item has type 'sellable'") = 0,
                       quote: discord.Option(str, description="Quote reason why this item was added?") = None
                       ):

        if item_type != "sellable":
            sell_value = 0
        try:
            db["Items"].insert_one({"_id": name.lower(), "description": description,
                                    "cost": cost, "image_url": image_url, "emote_id": int(emote_id),
                                    "item_type": item_type, "sell_value": sell_value, "quote": quote})

            # update existing inventories (dangerous)
            db["Inventory"].update_many({name: {"$exists": False}}, {"$set": {name.lower(): 0}})

            # edit item_list in db["Items"]
            item_list = item_handling.inventory_list()
            item_list.append(name.lower())
            db["Items"].update_one({"_id": "item_definitions"}, {"$set": {"item_list": item_list}})

        except Exception as error:
            await ctx.respond(f"Something went wrong. Do not try again.\n"
                              f"{error}")

            return

        em = discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** "
                                                       f"added {self.bot.get_emoji(int(emote_id))} **{name}** "
                                                       f"as a new item.")
        await ctx.respond(embed=em)

        await ctx.respond(f"Perform `/botconfig die` for changes to take effect.",
                          ephemeral=True)

    @edit.command(
        name = "item",
        description = "Edit an item in the database."
    )
    async def edit_item(self, ctx, *,
                        item: discord.Option(choices=item_handling.inventory_list()[5:], description="Which item do you want to edit?"),
                        description: discord.Option(str, description="Edit the item's description") = None,
                        cost: discord.Option(int, description="Change the /shop cost") = 0,
                        image_url: discord.Option(str, description="Only accepts IMGUR links.") = None,
                        emote_id: discord.Option(str, description="ONLY ID (series of numbers)") = None,
                        item_type: discord.Option(choices=["collectable", "consumable", "sellable"]) = None,
                        sell_value: discord.Option(int, description="Only if item has type 'sellable'") = 0,
                        quote: discord.Option(str, description="Quote reason why this item was added?") = None
                        ):
        if item_type != "sellable":
            sell_value = 0

        if description is None and cost == 0 and image_url is None and emote_id is None and item_type is None and sell_value == 0 and quote is None:
            await ctx.respond("Looks like you're changing nothing...\n\n"
                              "*Note: if you're trying to change 'sell_value', "
                              "make sure item_type is set to 'sellable'.*", ephemeral=True)
            return

        em = discord.Embed(color=0xadcca6,
                           description=f"**{ctx.author.name}#{ctx.author.discriminator}** edited values:")

        if description is not None:
            try:
                db["Items"].update_one({"_id": item}, {"$set": {"description": description}})
                em.description += "\n`+ description`: value changed successfully."
            except:
                em.description += "\n`- description`: ERROR: unchanged."

        if cost != 0:
            try:
                db["Items"].update_one({"_id": item}, {"$set": {"cost": cost}})
                em.description += "\n`+ cost`: value changed successfully."
            except:
                em.description += "\n`- cost`: ERROR: unchanged."

        if image_url is not None:
            try:
                db["Items"].update_one({"_id": item}, {"$set": {"image_url": image_url}})
                em.description += "\n`+ image_url`: value changed successfully."
            except:
                em.description += "\n`- image_url`: ERROR: unchanged."

        if emote_id is not None:
            try:
                db["Items"].update_one({"_id": item}, {"$set": {"emote_id": int(emote_id)}})
                em.description += "\n`+ emote_id`: value changed successfully."
            except:
                em.description += "\n`- emote_id`: ERROR: unchanged."

        if item_type is not None:
            try:
                db["Items"].update_one({"_id": item}, {"$set": {"item_type": item_type}})
                em.description += "\n`+ item_type`: value changed successfully."
            except:
                em.description += "\n`- item_type`: ERROR: unchanged."

        if sell_value != 0:
            try:
                db["Items"].update_one({"_id": item}, {"$set": {"sell_value": sell_value}})
                em.description += "\n`+ sell_value`: value changed successfully."
            except:
                em.description += "\n`- sell_value`: ERROR: unchanged."

        if quote is not None:
            try:
                db["Items"].update_one({"_id": item}, {"$set": {"description": description}})
                em.description += "\n`+ quote`: value changed successfully."
            except:
                em.description += "\n`- quote`: ERROR: unchanged."

        em.set_footer(text="do /item [item] to review the changes you made.")
        await ctx.respond(embed=em)

    @add.command(
        name = "weapon",
        description="Adds a new weapon to the database. Use with CAUTION."
    )
    @commands.check(is_team)
    async def add_weapon(self, ctx, *,
                         name: discord.Option(str, description="Name of the weapon"),
                         damage: discord.Option(int),
                         accuracy: discord.Option(int),
                         defense: discord.Option(int)
                         ):
        try:
            db["WeaponStats"].insert_one({"_id": name.lower(), "damage": damage,
                                         "accuracy": accuracy, "defense": defense})

        except Exception as error:
            await ctx.respond(f"Something went wrong. Do not try again.\n"
                              f"{error}")
            return

        await ctx.respond(f"Added *{name}* to the list of weapons.\n"
                          f"Stats: {damage} dmg, {accuracy} %acc, {defense} %def.\n"
                          f"Make sure to edit `profile.py` to let any changes take effect.\n"
                          f"Reboot.")

    # uncomment for reload command lol
    # @botconfig.command(
    #     name="reload",
    #     description="Reloads a module."
    # )
    # async def reload(self, ctx, *, module:discord.Option(choices=["inventory", "profile", "misc", "help"])):
    #     self.bot.reload_extension(f'modules.{module}')
    #     em = discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}**
    #                        module {module} has been reloaded.")
    #     await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Owneronly(client))
