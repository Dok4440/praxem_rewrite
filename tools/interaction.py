import discord
from discord.ui import Button, View, Modal
from tools import wembeds, item_handling


class YesNoButtons(View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
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
        super().__init__(timeout=120)
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


class BagOptions(discord.ui.View):
    def __init__(self, ctx, pr_client, balance):
        super().__init__(timeout=90)
        self.ctx = ctx
        self.bot = pr_client
        self.balance = balance

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=None)

    @discord.ui.select(
        placeholder = "All items",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="All items",
                description="Show all items in your bag."
            ),
            discord.SelectOption(
                label="Consumables",
                description="Show all consumable bag items."
            ),
            discord.SelectOption(
                label="Collectables",
                description="Show your collection of rare items."
            )
        ]
    )
    async def select_callback(self, select, interaction):
        await interaction.response.edit_message(embed=item_handling.pager(self.ctx, select.values[0],
                                                                          self.bot, self.balance))