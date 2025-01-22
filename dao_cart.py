# import json
# import os.path
# import sqlite3


# def connect(path):
#     exists = os.path.exists(path)
#     __conn = sqlite3.connect(path)
#     if not exists:
#         create_tables(__conn)
#     __conn.row_factory = sqlite3.Row
#     return __conn


# def create_tables(conn):
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS carts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL UNIQUE,
#             contents TEXT,
#             cost REAL
#         )
#     ''')
#     conn.commit()


# def get_cart(username: str) -> list:
#     conn = connect('carts.db')
#     cursor = conn.cursor()
#     if cursor:
#         cursor.execute('SELECT * FROM carts WHERE username = ?', (username,))
#     else:
#         return []
    
#     cart = cursor.fetchall()
#     temp_cart = []
#     for row in cart:
#         temp_cart.append(row)
    
#     final_cart = []
#     for item in temp_cart:
#         final_cart.append(item)
    
#     cursor.close()
#     conn.close()
#     return final_cart


# def add_to_cart(username: str, product_id: int):
#     conn = connect('carts.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
#     contents = cursor.fetchone()
#     if contents is None:
#         contents = []
#     else:
#         contents = eval(contents['contents'])
#     contents.append(product_id)
#     cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
#                    (username, str(contents), 0))
#     conn.commit()


# def remove_from_cart(username: str, product_id: int):
#     conn = connect('carts.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
#     contents = cursor.fetchone()
#     if contents is None:
#         return
#     contents = eval(contents['contents'])
#     contents.remove(product_id)
#     cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
#                    (username, str(contents), 0))
#     conn.commit()


# def delete_cart(username: str):
#     conn = connect('carts.db')
#     cursor = conn.cursor()
#     cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
#     conn.commit()







import json
import os.path
import sqlite3

def connect(path):
    # Enable Write-Ahead Logging (WAL) for better concurrency
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode = WAL')
    return conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT,
            cost REAL
        )
    ''')
    conn.commit()


def get_cart(username: str) -> list:
    # Retrieve only necessary fields
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        return []
    return json.loads(result['contents'])  # Simplified to reduce processing



def add_to_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row:
        contents = json.loads(row['contents'])  # Replace eval with json.loads
    else:
        contents = []

    # Update contents
    contents.append(product_id)
    cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                   (username, json.dumps(contents), 0))
    conn.commit()
    cursor.close()
    conn.close()


def remove_from_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row:
        contents = json.loads(row['contents'])  # Replace eval with json.loads
        if product_id in contents:
            contents.remove(product_id)

        # Update contents
        cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                       (username, json.dumps(contents), 0))
        conn.commit()
    cursor.close()
    conn.close()


def delete_cart(username: str):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
    conn.commit()
    cursor.close()
    conn.close()






