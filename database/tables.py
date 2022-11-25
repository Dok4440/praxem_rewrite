from database import database

create_profile_table = """
CREATE TABLE IF NOT EXISTS profile (
    user_id INTEGER PRIMARY KEY NOT NULL,
    gender TEXT NOT NULL,
    height TEXT NOT NULL,
    friend_id TEXT NOT NULL,
    age INTEGER NOT NULL,
    xp INTEGER NOT NULL,
    bio TEXT NOT NULL,
    badges TEXT
)
"""

create_items_table = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    cost INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    emote_id INTEGER NOT NULL,
    item_type TEXT NOT NULL,
    sell_value INTEGER NOT NULL,
    item_quote TEXT,
    sellable INTEGER
);
"""

create_maps_table = """
CREATE TABLE IF NOT EXISTS maps (
    name TEXT PRIMARY KEY NOT NULL,
    district_pointer_img TEXT NOT NULL,
    world_map_pointer_img TEXT NOT NULL,
    area_map_img TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    minimum_level INTEGER
);
"""

create_weapons_table = """
CREATE TABLE IF NOT EXISTS weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    damage INTEGER NOT NULL,
    accuracy INTEGER NOT NULL,
    defense INTEGER NOT NULL
);
"""

create_inventory_items_table = """
CREATE TABLE IF NOT EXISTS inventory_items (
    profile_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER,
    
    FOREIGN KEY (profile_id) REFERENCES profile (user_id),
    FOREIGN KEY (item_id) REFERENCES items (id)
)
"""

create_inventory_weapons_table = """
CREATE TABLE IF NOT EXISTS inventory_weapons (
    profile_id INTEGER NOT NULL,
    weapon_id INTEGER NOT NULL,
    
    FOREIGN KEY (profile_id) REFERENCES profile (user_id),
    FOREIGN KEY (weapon_id) REFERENCES weapons (id)
)
"""

create_locations_table = """
CREATE TABLE IF NOT EXISTS locations (
    profile_id INTEGER NOT NULL,
    map_name TEXT NOT NULL,
    
    FOREIGN KEY (profile_id) REFERENCES profile (user_id),
    FOREIGN KEY (map_name) REFERENCES maps (name)
)
"""

create_reload_info_table = """
CREATE TABLE IF NOT EXISTS reload_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER NOT NULL,
    user_name TEXT NOT NULL
)
"""


def sync_database():
    connection = database.create_connection()

    database.execute_query(connection, create_profile_table)
    database.execute_query(connection, create_items_table)
    database.execute_query(connection, create_maps_table)
    database.execute_query(connection, create_weapons_table)
    database.execute_query(connection, create_inventory_items_table)
    database.execute_query(connection, create_inventory_weapons_table)
    database.execute_query(connection, create_locations_table)
    database.execute_query(connection, create_reload_info_table)

    print("On startup: database synced.")
