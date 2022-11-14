import os
import discord
import string
import random


def get_version():
    return "v1.6.2"


def get_target(target, id):
    if target is None:
        target = id
    else:
        try: target = target.id
        except: pass
    return target


def ismain():
    if os.getenv('ISMAIN') == "True":
        return True
    else:
        return False


def hierarchy_check(user, target):
    if target.top_role >= user.top_role:
        return 0
    else:
        return 1


def get_friend_id():
    ascii_uc  = string.ascii_uppercase
    ascii_num = string.digits

    string_characters = ascii_uc + ascii_num
    id = ''.join(random.choice(string_characters) for i in range(6))

    return id


def dialogue_splitter(text):
    # max 165 characters, 3 lines (55 characters/line - word splits with spaces)
        n = 55
        split = [text[i:i+n] for i in range(0, len(text), n)]


def decorate_inv_list(list):
    # main weapon, second weapon, main weapon xp, secondary weapon xp, balance
    for i in range(0, 5):
        list[i] = list[i].split(': ')[1]

    # main and secondary weapon strings
    list[0] = f"*{list[2]} XP* — **{list[0].capitalize()}**"
    list[1] = f"*{list[3]} XP* — **{list[1].capitalize()}**"

    return list


def decorate_inv_items(list):
    items_to_pop = []

    for i in range(len(list)):
        li = list[i].split(': ')

        '''# INSERT EMOTE HERE TOO LATER'''
        emote = '🍎'
        name = li[0]
        value = li[1]

        li = f"{emote} {name.capitalize()}\n— *Amount: `{value}`*"
        list[i] = li

        '''if value = 0, add to pop list'''
        if int(value) == 0:
            items_to_pop.append(i)

    '''items to remove if value = 0'''
    for i in range(len(items_to_pop)):
        list.pop(items_to_pop[i]-i)

    return list
