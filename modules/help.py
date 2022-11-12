import discord
from discord.ext import commands
from discord.ext.commands import cog
from tools import embeds
import typing


class Help(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @discord.slash_command(
        name="help",
        description="get some more info about a command or feature",
        guild_only=False )
    async def info(self, ctx, option: discord.Option(choices=["info", "die"])):
        name = None
        description = None
        usage = None
        options = None
        permissions = None

        # uncomment this to show default help
        # if option == "help" or option is None:
        #     await ctx.respond(embed=embeds.help_embed())
        #     return

        if option == "info":
            name = "info"
            description = "Get information about Project Ax, check out the Terms of Service, read who's on the " \
                          "development team or check bot stats like latency, ping & version. You can also " \
                          "generate an invite link to let Praxem join your own server by using `/info invite`."
            usage = "`/info [option]`"
            options = "ping, uptime, team, invite, documentation, version, legal"

        elif option == "die":
            name = "die"
            description = "Shuts down, restarts or updates the Project Ax bot. Add the `pull` parameter " \
                          "to update Praxem by performing 'git pull' to the Github."
            usage = "`/die` or `/die pull`"
            options = "None, pull"
            permissions = "bot_owner, administrator"

        await ctx.respond(embed=embeds.help_command_embed(name, description, usage, options, permissions))



def setup(client):
    client.add_cog(Help(client))