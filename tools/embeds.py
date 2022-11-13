import discord
from tools import _json


def help_embed():
    em = discord.Embed(color=0xadcca6, title="Project Ax")
    em.add_field(name="info", value="just use `/` commands lol", inline=False)
    em.set_footer(text=f"do \"/help <command>\" to see info about a specific command.")
    em.set_thumbnail(url=_json.get_art()["bot_icon_longsword"])

    return em


def help_command_embed(name, description, usage, options, permissions):
    em = discord.Embed(color=0xadcca6, title="/" + name, description=description)
    em.add_field(name="Usage", value=usage, inline=False)

    if options is not None:
        em.add_field(name="options", value=options, inline=False)

    if permissions is not None:
        em.set_footer(text=f"Permissions required: {permissions}")

    return em


'''errors'''
def error_1(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** Something went wrong.")
    return em


def error_2(a,b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** The command was canceled.")
    return em


def error_3(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** Couldn't find that command.")
    return em


def error_4(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** Couldn't find that module.")
    return em


def error_5(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** I couldn't ban that user. Make sure **my role** and **your highest role** are above the highest role of the user you are trying to ban.")
    return em


def error_6(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** I couldn't kick that user. Make sure **my role** and **your highest role** are above the highest role of the user you are trying to kick.")
    return em


def error_7(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** I couldn't find a warning with that ID listed, please try again.")
    return em


def error_8(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** You can't warn yourself, silly.")
    return em


def error_9(a, b, target):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** Looks like {target.display_name} doesn't have any warnings yet, looks clean boss.")
    return em

