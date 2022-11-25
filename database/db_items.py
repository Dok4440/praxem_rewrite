from database import database

try:
    connection = database.create_connection()
    cursor = connection.cursor()
    print("On startup: connection with database established.")
except Exception as e:
    print("Connection error: {}".format(e))


def add_profile(user_id, gender, height, friend_id, age, xp, bio, badges):
    query = """INSERT INTO profile (user_id, gender, height, friend_id, age, xp, bio, badges)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

    cursor.execute(query, (user_id, gender, height, friend_id, age, xp, bio, badges))
    connection.commit()


def add_item(name, description, cost, image_url, emote_id, item_type, sell_value, item_quote=None, sellable=None):
    query = """INSERT INTO items 
    (name, description, cost, image_url, emote_id, item_type, sell_value, item_quote, sellable)
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    cursor.execute(query, (name, description, cost, image_url, emote_id, item_type, sell_value, item_quote, sellable))
    connection.commit()


def remove_item(item_id):
    delete_from_table_items = "DELETE FROM items WHERE id = ?"
    delete_inventory_items = "DELETE FROM inventory_items WHERE item_id = ?"

    cursor.execute(delete_from_table_items, (item_id, ))
    cursor.execute(delete_inventory_items, (item_id, ))

    connection.commit()


def update_item(option, value, item_id):
    query = "UPDATE items SET {}=? WHERE id=?".format(option)
    cursor.execute(query, (value, item_id))
    connection.commit()


def list_items():
    rows = cursor.execute("SELECT name FROM items").fetchall()
    list = []

    for row in rows:
        list.append(row[0])

    return list


def list_items_by_type(item_type):
    rows = cursor.execute("SELECT name FROM items WHERE item_type=?", (item_type, )).fetchall()
    list = []

    for row in rows:
        list.append(row[0])

    return list


def get_item_id(item_name):
    rows = cursor.execute("SELECT id FROM items WHERE name=?", (item_name, )).fetchall()

    for row in rows:
        return row[0]


def get_item_one_info(option, item_id):
    rows = cursor.execute("SELECT {} FROM items WHERE id=?".format(option), (item_id, ))

    for row in rows:
        return row[0]


def get_item_all_info(item_id):
    rows = cursor.execute("SELECT * FROM items WHERE id=?", (item_id, ))

    for row in rows:
        print(row)
        return row


def give_item(profile_id, item_id, added_quantity):
    query = "SELECT quantity FROM inventory_items WHERE profile_id=? AND item_id=?"
    c = cursor.execute(query, (profile_id, item_id))
    previous_quantity = 0

    if cursor.fetchone(): # profile already had x amount of this item
        for i in c:
            previous_quantity = i
        previous_quantity += added_quantity

        query = "UPDATE inventory_items SET quantity=? WHERE profile_id=? AND item_id=?"
        cursor.execute(query, (profile_id, item_id))

    else: # profile didn't have this item yet
        query = "INSERT INTO inventory_items (profile_id, item_id, quantity) VALUES (?, ?, ?)"
        try:
            cursor.execute(query, (profile_id, item_id, added_quantity))
        except Exception as e:
            print(e)

    connection.commit()


def get_user_item_amount(profile_id, item_id):
    query = "SELECT quantity FROM inventory_items WHERE profile_id=? AND item_id=?"
    c = cursor.execute(query, (profile_id, item_id))

    if cursor.fetchone():
        for i in c:
            return i
    else:
        return 0
