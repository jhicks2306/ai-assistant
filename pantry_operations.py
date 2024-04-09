import sqlite3
import csv
import io
from datetime import date, timedelta

today = date.today()

def connect_to_db(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    return conn, cursor
    
def create_item(name, conn, cursor):
    cursor.execute('INSERT INTO pantry (name, date_added) VALUES (?, ?)', (name, today))
    conn.commit()

def read_items(conn, cursor):
    cursor.execute('SELECT * FROM pantry')
    items = cursor.fetchall()
    return items

def update_item(name_old, name_new, conn, cursor):
    item_id = get_item_id_by_name(name_old, conn, cursor)
    if item_id is None:
        print('There is no item in the pantry matching this name')
    else:
        cursor.execute('UPDATE pantry SET name = ?, date_added = ? WHERE id = ?', (name_new, today, item_id))
        conn.commit()

def delete_item(name, conn, cursor):
    cursor.execute('DELETE FROM pantry WHERE name = ?', (name,))
    conn.commit()

def get_item_id_by_name(name, conn, cursor):  
    cursor.execute('SELECT id FROM pantry WHERE name = ?', (name,))
    item = cursor.fetchone()
    
    if item:
        return item[0]  # Return the item ID
    else:
        return None  # Return None if item not found

def create_items(names, conn, cursor):
    added_items = []
    not_added_items = []
    in_stock = True
    for name in names:
        try:
            create_item(name, conn, cursor)
            added_items.append(name)
        except sqlite3.IntegrityError:
            not_added_items.append(name)
    
    if not_added_items and added_items:
        return f'Following items were added to the pantry: {", ".join(added_items)}.\
              These items were already in the pantry: {", ".join(not_added_items)}.'
    if not_added_items:
        return f'The following items are already logged in the pantry: {", ".join(not_added_items)}.'
    if added_items:
        return f'The following items have been added to the pantry: {", ".join(added_items)}.'  


def delete_items(names, conn, cursor):   
    not_found_items = []
    deleted_items = []

    for name in names:
        delete_item(name, conn, cursor)
        deleted_items.append(name)
        if cursor.rowcount == 0:  # Check if any rows were affected by the delete operation
            not_found_items.append(name)
    
    conn.commit()
    
    if not_found_items:
        msg = "The following items were not found in the database and couldn't be deleted:"
        for item in not_found_items:
            msg = msg + "\n" + item
        return msg
    else:
        return f'The following items have been removed from the pantry: {", ".join(deleted_items)}.'  
    
def get_pantry_csv(conn, cursor):
    """Returns list of items in stock in CSV format."""
    # Execute a SELECT query to fetch all ingredients in stock.
    cursor.execute("SELECT name FROM pantry")
    rows = cursor.fetchall()
    # Write the data to a CSV-formatted string
    csv_output = io.StringIO()
    writer = csv.writer(csv_output)

    # Write header
    writer.writerow(['Ingredient'])

    # Write rows
    for row in rows:
        writer.writerow(row)

    # Get the CSV-formatted string
    csv_string = csv_output.getvalue()

    # Close the StringIO object
    csv_output.close()

    return csv_string
