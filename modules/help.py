import discord
from discord.ext import commands
from discord.ext.commands import cog
from tools import embeds, item_handling
import typing


class Help(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @discord.slash_command(
        name="help",
        description="get some more info about a command or feature",
        guild_only=False )
    async def info(self, ctx, option: discord.Option(choices=["bag", "info", "item", "profile", "report"])):
        name = None
        description = None
        usage = None
        options = None
        permissions = None

        # uncomment this to show default help
        # if option == "help" or option is None:
        #     await ctx.respond(embed=embeds.help_embed())
        #     return

        if option == "bag":
            name = "bag"
            description = "Shows all the items you have in one place. You can sort 'sellable', 'collectable' " \
                          "and 'consumable'. If you don't have an item it will not be shown. Use /item to get " \
                          "information about **all** items."
            usage = "`/bag`"

        elif option == "info":
            name = "info"
            description = "Get information about Project Ax, check out the Terms of Service, read who's on the " \
                          "development team or check bot stats like latency, ping & version. You can also " \
                          "generate an invite link to let Praxem join your own server by using `/info invite`."
            usage = "`/info [option]`"
            options = ["ping", "uptime", "team", "invite", "documentation", "version", "legal"]

        elif option == "item":
            name = "item"
            description = "View detailed information about an item."
            usage = "`/item [item]`"
            options = item_handling.inventory_list()[5:]

        elif option == "profile":
            name = "profile"
            description = "Check your profile. If you don't have a profile yet, this command will automatically run " \
                          "you through the steps to create one."
            usage = "`/profile`"

        elif option == "report":
            name = "report"
            description = "Report a user to the official Project Ax staff team. We will review your report " \
                          "as soon as possible."
            usage = "`/report @user [reason]`"
            options = ["user", "reason"]

        await ctx.respond(embed=embeds.help_command_embed(name, description, usage, options, permissions))


def setup(client):
    client.add_cog(Help(client))