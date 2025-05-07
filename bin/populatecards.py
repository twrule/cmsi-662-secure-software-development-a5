import sqlite3

con = sqlite3.connect('bank.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS user_cards')
cur.execute('''
    CREATE TABLE user_cards (
        owner text, card_id integer, card_count integer,
        foreign key(owner) references users(email),
        foreign key(card_id) references pokemon_base_set(id))''')
cur.execute(
    "INSERT INTO user_cards VALUES (?, ?, ?)",
    ('alice@example.com', 1, 3))
cur.execute(
    "INSERT INTO user_cards VALUES (?, ?, ?)",
    ('alice@example.com', 35, 2))
cur.execute(
    "INSERT INTO user_cards VALUES (?, ?, ?)",
    ('bob@example.com', 92, 4))
con.commit()
con.close()
print("Users have cards")
