import discord
from discord.ui import Button, View, Modal
from tools import wembeds


class YesNoButtons(View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.clickedYes = False

    @discord.ui.button(label="Yes!", style=discord.ButtonStyle.green, emoji="✅")
    async def yes_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedYes = True
        self.stop()

    @discord.ui.button(label="Nope.", style=discord.ButtonStyle.grey, emoji="❌")
    async def no_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.stop()

    # async def on_timeout(self):
    #     await self.ctx.

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use these buttons, they're someone else's!", ephemeral=True)
            return False
        else:
            return True


class WeaponNavButtons(View):
    def __init__(self, ctx, weapon_list, pr_client):
        super().__init__(timeout=500)
        self.ctx = ctx
        self.bot = pr_client

        self.weapons = weapon_list
        self.page = 0
        self.weapon = self.weapons[self.page]

    @discord.ui.button(label="back", style=discord.ButtonStyle.blurple, emoji="◀️")
    async def back_button_callback(self, button, interaction):
        if self.page == 0:
            self.page = len(self.weapons)-1
        else:
            self.page -= 1

        self.weapon = self.weapons[self.page]
        await interaction.response.edit_message(embed=wembeds.w_page(self.weapon, self.ctx.author.avatar, self.bot))

    @discord.ui.button(label="Choose this weapon!", style=discord.ButtonStyle.blurple)
    async def confirm_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.stop()

    @discord.ui.button(label="next", style=discord.ButtonStyle.blurple, emoji="▶️")
    async def next_button_callback(self, button, interaction):
        if self.page == len(self.weapons) - 1:
            self.page = 0
        else:
            self.page += 1

        self.weapon = self.weapons[self.page]
        await interaction.response.edit_message(embed=wembeds.w_page(self.weapon, self.ctx.author.avatar, self.bot))

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use these buttons, they're someone else's!", ephemeral=True)
            return False
        else:
            return True


class Report(Modal):
    def __init__(self, ctx, user_id, channel, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.user_id = user_id
        self.channel = channel

        self.add_item(discord.ui.InputText(label="User (ID)", value=f"{self.user_id}"))
        self.add_item(discord.ui.InputText(label="Reason", style=discord.InputTextStyle.long))

    async def callback(self, interaction):
        embed = discord.Embed(title="User Report")
        embed.add_field(name="User", value=self.children[0].value, inline=False)
        embed.add_field(name="Reason", value=self.children[1].value, inline=False)
        embed.set_footer(text=f"by {self.ctx.author.id} - {self.ctx.author.name}#{self.ctx.author.discriminator}")
        await self.channel.send(embeds=[embed])
        await interaction.response.send_message("User successfully reported!", ephemeral=True)