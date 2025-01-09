import sqlite3
from creatures import Dinosaur

def create_connection():
    return sqlite3.connect('database.db')

def create_table():
    with create_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                discord_id INTEGER NOT NULL UNIQUE,
                dino_count INTEGER
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventories (
                id INTEGER PRIMARY KEY,
                discord_id INTEGER,
                dino_name TEXT,
                inv_num INTEGER,
                dino_level INTEGER
            )
        ''')
        conn.commit()

def add_user(discord_id, dino_count=0):
    with create_connection() as conn:
        conn.execute('''
            INSERT INTO users (discord_id, dino_count)
            VALUES (?, ?)
            ON CONFLICT(discord_id) DO UPDATE SET
                dino_count=excluded.dino_count
        ''', (discord_id, dino_count))
        conn.commit()

def get_users():
    with create_connection() as conn:
        cursor = conn.execute('SELECT discord_id FROM users')
        # Change to MD array
        row = cursor.fetchall()
        return row[0] if row else []
    
def add_dino(discord_id, dino: Dinosaur):
    with create_connection() as conn:
        conn.execute('''
            INSERT INTO inventories (discord_id, dino_name, inv_num, dino_level)
            VALUES (?, ?, ?, ?)
        ''', (discord_id, dino.species, 0, dino.level))
        conn.commit()

def get_inventory(discord_id):
    with create_connection() as conn:
        cursor = conn.execute('SELECT dino_name, dino_level FROM inventories WHERE discord_id=?', (discord_id,))
        # Change to MD array
        row = cursor.fetchall()
        return row if row else None

def get_inventory_string(id):
    rows = get_inventory(id)
    retString = ""
    for i in range(0, len(rows)):
        retString += f'{rows[i][0]}   lv{rows[i][1]} \n'
    return retString