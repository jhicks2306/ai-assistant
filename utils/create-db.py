import sqlite3

# Connect to the SQLite database (creates a new database if not exists)
conn = sqlite3.connect('pantry.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the pantry table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pantry (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        in_stock BOOLEAN
    )
''')

# Function to add a new ingredient to the pantry
def add_item(name, in_stock):
    cursor.execute('INSERT INTO pantry (name, in_stock) VALUES (?, ?)',
                   (name, in_stock))
    conn.commit()
    print("Ingredient added successfully!")

# Function to retrieve all items in the pantry
def get_all_items():
    cursor.execute('SELECT * FROM pantry')
    items = cursor.fetchall()
    return items

# Example usage
add_item('Quinoa', True)
add_item('Apples', False)
add_item('Oranges', True)
add_item('Bananas', True)
add_item('Pasta', False)

print("All items in the pantry:")
print(get_all_items())

# Close the cursor and connection
cursor.close()
conn.close()
