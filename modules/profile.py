import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

from tools import interaction, wembeds, _json, _db, tools, item_handling

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


class Profile(commands.Cog):
    def __init__(self, pr_client):
        self.bot = pr_client

    @commands.Cog.listener()
    async def on_ready(self):
        print('profile.py -> on_ready()')

    @discord.slash_command(
        name="profile",
        description="View your Project Ax profile",
        guild_only=True
    )
    async def profile(self, ctx):

        target = ctx.author.id

        # CHECK IF PROFILE EXISTS
        check = db["Profile"].count_documents({"_id": target})
        if check == 0:
            em = discord.Embed(color=0xadcca6,
                               description=f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Do you want to create one?")
            em.set_footer(text="Note that by creating a profile, you agree to the Project Ax terms and privacy policy.")

            view = interaction.YesNoButtons(ctx)
            await ctx.respond(embed=em, view=view)
            await view.wait()

            if view.clickedYes:
                '''main weapon'''
                weapon_list = ['longsword', 'katana', 'dagger', 'greatsword', 'sledgehammer', 'mace']
                main_weapon = ""

                view = interaction.WeaponNavButtons(ctx, weapon_list, self.bot)
                await ctx.edit(content="**PRIMARY WEAPON**",
                               embed=wembeds.w_page(weapon_list[0], ctx.author.avatar, self.bot), view=view)
                await view.wait()

                main_weapon = view.weapon

                view = interaction.YesNoButtons(ctx)
                await ctx.edit(content=None, embed=discord.Embed(color=0xadcca6,
                                                                 description=f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to pick **{main_weapon}** as your main weapon?"),
                               view=view)
                await view.wait()

                if view.clickedYes:
                    '''secondary weapon'''
                    weapon_list = ['bow', 'longbow']
                    secondary_weapon = ""

                    view = interaction.WeaponNavButtons(ctx, weapon_list, self.bot)
                    await ctx.edit(content="**SECONDARY WEAPON**",
                                   embed=wembeds.w_page(weapon_list[0], ctx.author.avatar, self.bot), view=view)
                    await view.wait()

                    secondary_weapon = view.weapon

                    view = interaction.YesNoButtons(ctx)
                    await ctx.edit(content=None, embed=discord.Embed(color=0xadcca6,
                                                                     description=f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to pick **{secondary_weapon}** as your secondary weapon?"),
                                   view=view)
                    await view.wait()

                    if view.clickedYes:
                        '''database appending & finalizing'''
                        '''INVENTORY'''
                        item_handling.create_inventory(target, main_weapon, secondary_weapon)

                        '''PROFILE'''
                        maleFemaleRatio = [1, 2]
                        female_height = ["4'7", "4'8", "4'9", "4'10", "4'11", "5'", "5'1", "5'2", "5'3", "5'4", "5'5",
                                         "5'6", "5'7", "5'8"]
                        male_height = ["4'9", "4'10", "4'11", "5'", "5'11", "6'", "6'1", "5'4", "5'5", "5'6", "5'7",
                                       "5'8", "5'9", "5'10"]
                        age = ['18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']
                        choice = random.choice(maleFemaleRatio)

                        if choice == 1:
                            gender = "Male"
                            height = random.choice(male_height)
                            age = random.choice(age)
                        else:
                            gender = "Female"
                            height = random.choice(female_height)
                            age = random.choice(age)

                        '''GENERATE RANDOM FRIEND CODE'''
                        friend_id = "N/A"
                        a = 1
                        while a == 1:
                            friend_id = tools.get_friend_id()
                            if not _db.check_friend_id(friend_id):
                                a += 1

                        _db.create_profile(target, gender, height, friend_id, age)

                        '''CLEANUP'''
                        # canceled
                        em = discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Profile creation done!")
                        await ctx.edit(embed=em)

                        '''LOGS'''
                        print()
                        print("----")
                        print(f"Created profile for user {ctx.author.name}#{ctx.author.discriminator} - {ctx.author.id}")
                        print(f"Created inventory for profile.")
                        print("----")

                    else:
                        em = discord.Embed(color=0xadcca6, description=f"Profile creation canceled.")
                        await ctx.edit(embed=em)
                        return
                else:
                    # canceled
                    em = discord.Embed(color=0xadcca6, description=f"Profile creation canceled.")
                    await ctx.edit(embed=em)
                    return
            else:
                # canceled
                em = discord.Embed(color=0xadcca6, description=f"Profile creation canceled.")
                await ctx.edit(embed=em)
                return

        #################################
        ### IF PROFILE ALREADY EXISTS ###
        #################################
        age = "N/A"
        location = "N/A"
        friend_id = "N/A"
        gender = "N/A"
        height = "N/A"
        xp = "N/A"
        bio = "N/A"

        profile = db["Profile"].find({"_id": target})
        for b in profile:
            age = b["age"]
            location = b["location"]
            friend_id = b["friend_id"]
            gender = b["gender"]
            height = b["height"]
            xp = b["xp"]
            bio = b["bio"]

        main_weapon = _db.get_weapons(target)[0]
        secondary_weapon = _db.get_weapons(target)[1]

        main_weapon_emote = self.bot.get_emoji(_json.get_emote_id(main_weapon))
        secondary_weapon_emote = self.bot.get_emoji(_json.get_emote_id(secondary_weapon))

        if bio == "":
            bio = "no bio set, configure this with /settings"

        """ badges """
        badges_string = ""
        badges = ""

        try:
            badges = _db.get_badges(target)
            badges = _db.split_badges(badges)

            for i in range(0, len(badges)):
                badges_string += f"{self.bot.get_emoji(_json.get_emote_id(badges[i]))} "
        except:
            pass

        em = discord.Embed(title=f"{ctx.author.name}'s Profile {badges_string}",
                           description=f"Lv. {xp}\n "
                                       f"[-----------](http://praxem.wikidot.com/start)\n"
                                       f"{bio}\n\n"
                                       f"🌍 {location}\n\n"
                                       f"Gender: {gender}\n"
                                       f"Height: {height}\n"
                                       f"Age: {age}\n\n"
                                       f"**{main_weapon}** {main_weapon_emote} & **{secondary_weapon}** {secondary_weapon_emote}\n"
                                       f"[-----------](http://praxem.wikidot.com/start)", color=0xadcca6)

        em.set_thumbnail(url=_json.get_art()["bot_icon_greatsword"])
        em.set_footer(text=f"Friend ID: {friend_id}")

        # try:
        #     em.set_thumbnail(url=_json.get_art()[badges[0]])
        # except:
        #     pass

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Profile(client))
