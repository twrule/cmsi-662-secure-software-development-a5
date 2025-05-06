import sqlite3
import csv

# Connect to the database
con = sqlite3.connect('bank.db')

# Create the pokemon_base_set table if it doesn't exist
cur = con.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS pokemon_base_set (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        hp INTEGER NOT NULL,
        rarity TEXT NOT NULL
    )
''')
cur = con.cursor()

# Open the CSV file and insert data
with open('bin/pokemon_setup/pokemon_base_set.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cur.execute(
            "INSERT INTO pokemon_base_set (id, name, type, hp, rarity) VALUES (?, ?, ?, ?, ?)",
            (row['id'], row['name'], row['type'], row['hp'], row['rarity'])
        )

# Commit the changes and close the connection
con.commit()
con.close()

print("Pokémon Base Set data loaded from CSV")
