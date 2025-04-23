import psycopg2

# Connecting to PostgreSQL server
conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="dfgh4639ryei0288ksk4",  # Enter your password
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 1. Search by pattern (by name or phone)
def search_phonebook(pattern):
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s OR phone ILIKE %s", ('%' + pattern + '%', '%' + pattern + '%'))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No records found.")

# 2. Add or update a user or phone number
def insert_or_update_user(name, phone):
    cur.execute("SELECT 1 FROM phonebook WHERE name = %s", (name,))
    if cur.fetchone():  # If the user exists
        cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (phone, name))
        print(f"The phone number for {name} has been updated.")
    else:  # If the user does not exist
        cur.execute("INSERT INTO phonebook(name, phone) VALUES (%s, %s)", (name, phone))
        print(f"{name} has been added.")
    
    # View the updated table
    view_updated_table()

# 3. Add multiple users (bulk insert)
def bulk_insert_users(names, phones):
    for name, phone in zip(names, phones):
        if phone.isdigit() and len(phone) in range(10, 16):  # Check phone number validity
            cur.execute("INSERT INTO phonebook(name, phone) VALUES (%s, %s)", (name, phone))
        else:
            print(f"Invalid phone number: {phone} ({name})")
    conn.commit()
    print("All data has been added.")
    
    # View the updated table
    view_updated_table()

# 4. Fetch data with pagination (limit, offset)
def get_phonebook_page(limit, offset):
    cur.execute("SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No more records.")

# 5. Delete data by name or phone
def delete_by_name_or_phone(value):
    cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s", (value, value))
    conn.commit()
    print(f"All records for {value} have been deleted.")
    
    # View the updated table
    view_updated_table()

# 6. Show updated table
def view_updated_table():
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    print("\nUpdated Phonebook:")
    for row in rows:
        print(row)

# Main menu
while True:
    print("\n===== PHONEBOOK MENU =====")
    print("1. Search by pattern")
    print("2. Add or update user")
    print("3. Add multiple users")
    print("4. Fetch data with pagination")
    print("5. Delete data")
    print("6. View updated table")
    print("0. Exit")

    choice = input("Choose: ")
    if choice == "1":
        pattern = input("Enter the pattern: ")
        search_phonebook(pattern)
    elif choice == "2":
        name = input("Enter the user's name: ")
        phone = input("Enter the phone number: ")
        insert_or_update_user(name, phone)
    elif choice == "3":
        names = input("Enter names (comma-separated): ").split(",")
        phones = input("Enter phones (comma-separated): ").split(",")
        bulk_insert_users(names, phones)
    elif choice == "4":
        limit = int(input("Number of records to display (limit): "))
        offset = int(input("Starting offset (offset): "))
        get_phonebook_page(limit, offset)
    elif choice == "5":
        value = input("Which name or phone would you like to delete? ")
        delete_by_name_or_phone(value)
    elif choice == "6":
        view_updated_table()
    elif choice == "0":
        break
    else:
        print("Invalid choice!")

# Close connection
cur.close()
conn.close()
