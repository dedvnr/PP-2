import csv
from connect import connect


# Create table
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) UNIQUE,
        phone VARCHAR(20) UNIQUE
    )
    """
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# Insert from CSV
def insert_from_csv(filename='contacts.csv'):
    sql = """
    INSERT INTO phonebook (first_name, phone)
    VALUES (%s, %s)
    ON CONFLICT (first_name) DO NOTHING
    """

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(sql, (row['first_name'], row['phone']))

    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported successfully")


# Insert manually
def insert_from_console():
    first_name = input("Enter first name: ")
    phone = input("Enter phone number: ")

    sql = """
    INSERT INTO phonebook (first_name, phone)
    VALUES (%s, %s)
    ON CONFLICT (first_name) DO NOTHING
    """

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    cur.execute(sql, (first_name, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added")


# Show all
def search_all():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")

    rows = cur.fetchall()

    print(f"{'ID':<5} {'Name':<20} {'Phone':<20}")
    print("-" * 45)

    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")

    cur.close()
    conn.close()


# Update contact
def update_contact():
    search_all()

    contact_id = input("Enter ID to update: ")
    print("1 - Update name")
    print("2 - Update phone")

    choice = input("Choose: ")

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    if choice == '1':
        new_name = input("Enter new name: ")
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE id = %s",
            (new_name, contact_id)
        )
    elif choice == '2':
        new_phone = input("Enter new phone: ")
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE id = %s",
            (new_phone, contact_id)
        )
    else:
        print("Invalid choice")

    conn.commit()
    cur.close()
    conn.close()


# Search by name
def search_by_name():
    name = input("Enter name: ")

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s",
        ('%' + name + '%',)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# Search by phone prefix
def search_by_phone_prefix():
    prefix = input("Enter prefix: ")

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + '%',)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# Delete
def delete_by_name():
    name = input("Enter name to delete: ")

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE first_name = %s",
        (name,)
    )

    conn.commit()

    print("Deleted:", cur.rowcount)

    cur.close()
    conn.close()


# Menu
def main():
    create_table()

    while True:
        print("""
1. Import CSV
2. Add contact
3. Update
4. Show all
5. Search by name
6. Search by phone prefix
7. Delete
0. Exit
""")

        choice = input("Choose: ")

        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            search_all()
        elif choice == '5':
            search_by_name()
        elif choice == '6':
            search_by_phone_prefix()
        elif choice == '7':
            delete_by_name()
        elif choice == '0':
            break


if __name__ == "__main__":
    main()