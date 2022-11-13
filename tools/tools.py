import os
import discord
import string
import random


def get_version():
    return "v1.5.1"


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
