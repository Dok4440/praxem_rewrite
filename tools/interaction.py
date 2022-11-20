import discord
from discord.ui import Button, View, Modal
from tools import wembeds, item_handling, embeds


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


class NavigationButtons(View):
    def __init__(self, ctx, area, district, zoom_list, pr_client):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.bot = pr_client

        self.area = area
        self.district = district
        self.zoom_list = zoom_list
        self.zoom_level = 2
        self.zoom = self.zoom_list[self.zoom_level]

    @discord.ui.button(label="Zoom In", style=discord.ButtonStyle.gray,
                       emoji="<:PA_zoom_in:1043919918673952832>", disabled=True,
                       custom_id="zoomin")
    async def zoomin_button_callback(self, button, interaction):
        if not self.zoom_level == len(self.zoom_list) - 1:
            self.zoom_level += 1

        zoomin_button = button
        zoomout_button = [x for x in self.children if x.custom_id == "zoomout"][0]

        zoomout_button.disabled = False
        zoomout_button.style = discord.ButtonStyle.blurple

        if self.zoom_level == len(self.zoom_list) - 1:
            zoomin_button.disabled = True
            zoomin_button.style = discord.ButtonStyle.grey

        self.zoom = self.zoom_list[self.zoom_level]
        await interaction.response.edit_message(embed=embeds.maps_embed(self.ctx, self.area,
                                                                        self.district, self.zoom), view=self)

    @discord.ui.button(label="Zoom Out", style=discord.ButtonStyle.blurple,
                       emoji="<:PA_zoom_out:1043919920620109874>", custom_id="zoomout")
    async def zoomout_button_callback(self, button, interaction):
        if not self.zoom_level == 0:
            self.zoom_level -= 1

        zoomin_button = [x for x in self.children if x.custom_id == "zoomin"][0]
        zoomout_button = button

        zoomin_button.disabled = False
        zoomin_button.style = discord.ButtonStyle.blurple

        if self.zoom_level == 0:
            zoomout_button.disabled = True
            zoomout_button.style = discord.ButtonStyle.grey

        self.zoom = self.zoom_list[self.zoom_level]
        await interaction.response.edit_message(embed=embeds.maps_embed(self.ctx, self.area,
                                                                        self.district, self.zoom), view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use these buttons, they're someone else's!",
                                                    ephemeral=True)
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

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use this menu, it's someone else's!", ephemeral=True)
            return False
        else:
            return True

    @discord.ui.select(
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="All items",
                default=True,
                description="Show all items in your bag.",
                emoji="❓"
            ),
            discord.SelectOption(
                label="Consumables",
                description="Show all consumable bag items.",
                emoji="<:PA_consumables:1043084119619407922>"
            ),
            discord.SelectOption(
                label="Collectables",
                description="Show your collection of rare items.",
                emoji="<:PA_collectables:1043084121053872168>"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        await interaction.response.edit_message(embed=item_handling.pager(self.ctx, select.values[0],
                                                                          self.bot, self.balance))