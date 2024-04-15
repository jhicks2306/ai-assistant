import sqlite3
from datetime import date

today = date.today()

# Connect to the SQLite database (creates a new database if not exists)
conn = sqlite3.connect('pantry.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the shopping_list table
cursor.execute('''
    CREATE TABLE shopping_list (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        date_added DATE
    )'''
)

# Function to add a new ingredient to the shopping_list
def add_item(name, date_added):
    cursor.execute('INSERT INTO shopping_list (name, date_added) VALUES (?, ?)',
                   (name, date_added))
    conn.commit()
    print("Ingredient added successfully!")

# Function to retrieve all items in the shopping_list
def get_all_items():
    cursor.execute('SELECT * FROM shopping_list')
    items = cursor.fetchall()
    return items

# Example usage
add_item('aubergine', today)
add_item('spinach', today)

print("All items in the shopping_list:")
print(get_all_items())

# Close the cursor and connection
cursor.close()
conn.close()
