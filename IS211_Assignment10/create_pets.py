import sqlite3

pets_db_path = 'pets.db'
conn = sqlite3.connect(pets_db_path)
cursor = conn.cursor()

schema_sql = """
CREATE TABLE IF NOT EXISTS person (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    age INTEGER
);

CREATE TABLE IF NOT EXISTS pet (
    id INTEGER PRIMARY KEY,
    name TEXT,
    breed TEXT,
    age INTEGER,
    dead INTEGER
);

CREATE TABLE IF NOT EXISTS person_pet (
    person_id INTEGER,
    pet_id INTEGER
);
"""

cursor.executescript(schema_sql)
conn.commit()
conn.close()
