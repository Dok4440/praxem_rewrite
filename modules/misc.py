import discord
import time, datetime
from discord.ext import commands
from discord.ui import Button, View
from tools import tools, interaction

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
        guild_only=False)
    async def info(self, ctx, option: discord.Option(choices=["ping", "team", "invite",
                                                              "documentation", "version", "legal"])):
        if option == "ping":
            await ctx.respond(f"Project Ax Latency: {round(self.bot.latency*1000, 2)} ms")

        elif option == "team":
            em = discord.Embed(color=0xadcca6)
            v = tools.get_version()
            em.set_author(name=f"Project Ax {v}", icon_url=self.bot.user.avatar)
            em.add_field(name="**__Team__**",
                         value="**stupidbeaver** - Software Development\n**JuicyBblue#0004** - Artwork\n**Axie#8831** - Project Design",
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

    @discord.slash_command(
        name = "report",
        description = "Report a user for violating the Project Ax terms.",
        guild_only = True
    )
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def report(self, ctx, *, user: discord.Option(discord.Member),
                     reason: discord.Option(input_type=str,
                                            description="Only the Project Ax official Team will see this.",
                                            min_length=10,
                                            max_length=500)):

        user_id = f"{user} - {user.id}"

        embed = discord.Embed(title="User Report")
        embed.add_field(name="User", value=user_id, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"by {ctx.author.id} - {ctx.author.name}#{ctx.author.discriminator}")

        '''#praxem-reports in the official Project Ax server.'''
        report_channel = self.bot.get_channel(int(1041456824894890064))
        await report_channel.send(embeds=[embed])

        await ctx.respond("✅ User successfully reported!\n\n**DO NOT** report in bulk. Spamming reports will result in a Project Ax ban.", ephemeral=True)


def setup(pr_client):
    pr_client.add_cog(Miscellaneous(pr_client))
