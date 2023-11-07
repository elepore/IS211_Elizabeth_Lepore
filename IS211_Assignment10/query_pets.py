
import sqlite3

def query_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        person_id = input("Please enter a person's ID number or '-1' to exit: ")
        if person_id == '-1':
            break

        try:
            person_id = int(person_id)
        except ValueError:
            print("ID must be a number.")
            continue
        cursor.execute("SELECT * FROM person WHERE id = ?", (person_id,))
        person_data = cursor.fetchone()

        if person_data:
            first_name, last_name, age = person_data[1:4]
            print(f"{first_name} {last_name}, {age} years old")

            cursor.execute('''
            SELECT pet.name, pet.breed, pet.age, pet.dead
            FROM pet
            INNER JOIN person_pet ON pet.id = person_pet.pet_id
            WHERE person_pet.person_id = ?
            ''', (person_id,))
            pets_data = cursor.fetchall()

            for pet in pets_data:
                name, breed, age, dead = pet
                status = "dead" if dead else "alive"
                print(f"{first_name} {last_name} owned {name}, a {breed}, that was {age} years old ({status})")
        else:
            print("Person not found.")

    conn.close()

if __name__ == "__main__":
    db_path = "pets.db"
    query_data(db_path)
