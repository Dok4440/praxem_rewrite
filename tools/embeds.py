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
