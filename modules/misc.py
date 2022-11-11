import discord
import time, datetime
from discord.ext import commands
from discord.ui import Button, View
from tools import tools

bot_launch_time=time.time()


class Miscellaneous(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @commands.Cog.listener()
    async def on_ready(self):
        print('misc.py -> on_ready()')

    @discord.slash_command(
        name="info",
        description="Info about Praxem.",
        guild_only=False,
        default_member_permissions=discord.Permissions(permissions=0))
    async def info(self, ctx, option: discord.Option(choices=["ping", "uptime", "stats", "invite",
                                                              "documentation", "version", "legal"])):
        if option == "ping":
            await ctx.respond(f"Project Ax bot latency: {round(self.bot.latency*1000, 2)} ms")

        elif option == "uptime":
            uptime = str(datetime.timedelta(seconds=int(round(time.time() - bot_launch_time))))
            em = discord.Embed(color=0xadcca6, description=uptime)
            v = tools.get_version()
            em.set_author(name=f"Project Ax {v}", icon_url= self.bot.user.avatar)
            await ctx.respond(embed=em)

        elif option == "stats":
            em = discord.Embed(color=0xadcca6)
            v = tools.get_version()
            em.set_author(name=f"Project Ax {v}", icon_url=self.bot.user.avatar)
            em.add_field(name="**__Team__**",
                         value="**Dok#4440** - Software Development\n**JuicyBblue#4847** - Artwork\n**Axie★#3083** - Project Design",
                         inline=False)
            em.add_field(name="**__Contributors__**", value="Yuan Mizuna#9666", inline=False)
            await ctx.respond(embed=em)

        elif option == "invite":
            em = discord.Embed(
                description=f"**{ctx.author.name}#{ctx.author.discriminator}** Click the button below to invite Praxem to your server.",
                color=0xadcca6)
            invite_button = Button(label="Invite Me!", url="http://www.praxem.wikidot.com/invite")
            view = View()
            view.add_item(invite_button)
            await ctx.respond(embed=em, view=view)

        elif option == "documentation":
            em = discord.Embed(title="Documentation", description="soon.", color=0xadcca6)
            await ctx.respond(embed=em)

        elif option == "version":
            em = discord.Embed(color=0xadcca6, description=f"praxem: `{tools.get_version()}`\npy-cord: `{discord.__version__}`")
            await ctx.respond(embed=em)

        elif option == "legal":
            em = discord.Embed(color=0xadcca6, title="Legal", description=f"http://praxem.wikidot.com/legal\nhttp://praxem.wikidot.com/privacy\nhttp://praxem.wikidot.com/terms")
            em.set_footer( text="Note that by using any commands on Praxem, or by accessing the links above you automatically agree to the Privacy Policy and Terms and Conditions.")
            await ctx.respond(embed=em)


def setup(pr_client):
    pr_client.add_cog(Miscellaneous(pr_client))
