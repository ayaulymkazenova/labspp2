import psycopg2
import csv

# =======================
# CONNECT TO DATABASE
# =======================
def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="my_phonebook",
        user="postgres",
        password="1234"
    )
8
# =======================
# CREATE TABLE
# =======================
def create_table():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS my_phonebook (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        phone VARCHAR(20) NOT NULL
                    );
                """)
                conn.commit()
        print("Table created (if not exists).")
    except Exception as e:
        print("Error creating table:", e)

# =======================
# INSERT FROM CONSOLE
# =======================
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO my_phonebook (name, phone) VALUES (%s, %s)",
                            (name, phone))
                conn.commit()
        print("User added!")
    except Exception as e:
        print("Insert error:", e)

# =======================
# INSERT FROM CSV
# =======================
def insert_from_csv(path):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                with open(path, "r") as file:
                    reader = csv.reader(file)

                    for row in reader:
                        if len(row) < 2:
                            continue
                        if row[0].lower() == "name":  # skip header
                            continue

                        cur.execute("INSERT INTO my_phonebook (name, phone) VALUES (%s, %s)",
                                    (row[0], row[1]))

                conn.commit()
        print("CSV imported!")
    except Exception as e:
        print("CSV import error:", e)

# =======================
# UPDATE USER
# =======================
def update_user():
    name = input("Enter existing name: ")

    print("\nWhat do you want to update?")
    print("1. Name")
    print("2. Phone")
    print("3. Both")

    choice = input("Choose: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:

                if choice == "1":
                    new_name = input("New name: ")
                    cur.execute("UPDATE my_phonebook SET name=%s WHERE name=%s",
                                (new_name, name))

                elif choice == "2":
                    new_phone = input("New phone: ")
                    cur.execute("UPDATE my_phonebook SET phone=%s WHERE name=%s",
                                (new_phone, name))

                elif choice == "3":
                    new_name = input("New name: ")
                    new_phone = input("New phone: ")
                    cur.execute("UPDATE my_phonebook SET name=%s, phone=%s WHERE name=%s",
                                (new_name, new_phone, name))

                else:
                    print("Invalid option.")
                    return

                conn.commit()
                print("Updated!")

    except Exception as e:
        print("Update error:", e)

# =======================
# QUERY FUNCTIONS
# =======================
def query_all():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM my_phonebook")
                rows = cur.fetchall()
                for r in rows:
                    print(r)
    except Exception as e:
        print("Query error:", e)

def query_by_name():
    name = input("Enter name to search: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM my_phonebook WHERE name=%s", (name,))
                print(cur.fetchall())
    except Exception as e:
        print("Query error:", e)

def query_by_phone():
    phone = input("Enter phone to search: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM my_phonebook WHERE phone=%s", (phone,))
                print(cur.fetchall())
    except Exception as e:
        print("Query error:", e)

def search_like():
    text = input("Enter part of the name: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM my_phonebook WHERE name ILIKE %s",
                            ('%' + text + '%',))
                print(cur.fetchall())
    except Exception as e:
        print("Search error:", e)

# =======================
# DELETE USER
# =======================
def delete_user():
    print("\nDelete by:")
    print("1. Name")
    print("2. Phone")
    choice = input("Choose: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:

                if choice == "1":
                    name = input("Name to delete: ")
                    cur.execute("DELETE FROM my_phonebook WHERE name=%s", (name,))

                elif choice == "2":
                    phone = input("Phone to delete: ")
                    cur.execute("DELETE FROM my_phonebook WHERE phone=%s", (phone,))

                else:
                    print("Invalid option.")
                    return

                conn.commit()
                print("Deleted!")

    except Exception as e:
        print("Delete error:", e)

# =======================
# MAIN MENU
# =======================
def menu():
    create_table()

    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Insert (console)")
        print("2. Insert (CSV)")
        print("3. Update user")
        print("4. View all")
        print("5. Search by name")
        print("6. Search by phone")
        print("7. Search by part of name (LIKE)")
        print("8. Delete user")
        print("9. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv(input("Enter CSV path: "))
        elif choice == "3":
            update_user()
        elif choice == "4":
            query_all()
        elif choice == "5":
            query_by_name()
        elif choice == "6":
            query_by_phone()
        elif choice == "7":
            search_like()
        elif choice == "8":
            delete_user()
        elif choice == "9":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()
