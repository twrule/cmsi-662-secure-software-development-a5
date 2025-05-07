import sqlite3


def get_card_count(owner, card):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT card_count FROM user_cards where card_id=? and owner=?''',
                    (card, owner))
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]
    finally:
        con.close()


def get_pokemon_by_owner(owner):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT card_id, card_count FROM user_cards WHERE owner=? AND card_count > 0''',
                    (owner,))
        rows = cur.fetchall()
        return rows
    finally:
        con.close()


def get_pokemon(cards):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        rows = []
        for card in cards:
            cur.execute('''
            SELECT id, name, type, hp, rarity FROM pokemon_base_set WHERE id=?''',
                        (card[0],))
            pokemon_data = cur.fetchone()
            if pokemon_data:
                pokemon = {
                    'id': pokemon_data[0],
                    'name': pokemon_data[1],
                    'type': pokemon_data[2],
                    'hp': pokemon_data[3],
                    'rarity': pokemon_data[4],
                    'card_count': card[1]
                }
                rows.append(pokemon)
        print(rows)
        return rows
    finally:
        con.close()


def do_transfer(source, target, amount, pokemon):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            UPDATE user_cards SET card_count=card_count-? where owner=? and card_id=?''',
                    (amount, source, pokemon))
        cur.execute('''
            SELECT card_count FROM user_cards WHERE owner=? AND card_id=?''',
                    (target, pokemon))
        row = cur.fetchone()
        if row is None:
            cur.execute('''
            INSERT INTO user_cards (owner, card_id, card_count) VALUES (?, ?, ?)''',
                        (target, pokemon, amount))
        else:
            cur.execute('''
            UPDATE user_cards SET card_count=card_count+? WHERE owner=? AND card_id=?''',
                        (amount, target, pokemon))
        con.commit()
        return True
    finally:
        con.close()
