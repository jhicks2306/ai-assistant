import sqlite3
import csv
import io

def connect_to_db(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    return conn, cursor
    
def create_item(name, in_stock, conn, cursor):
    name = name.lower()
    cursor.execute('INSERT INTO pantry (name, in_stock) VALUES (?, ?)', (name, in_stock))
    conn.commit()


def read_items(conn, cursor):
    cursor.execute('SELECT * FROM pantry')
    items = cursor.fetchall()
    return items

def update_item(name_old, name_new, in_stock, conn, cursor):
    name_old = name_old.lower()
    name_new = name_new.lower()
    item_id = get_item_id_by_name(name_old, conn, cursor)
    if item_id is None:
        print('There is no item in the pantry matching this name')
    else:
        cursor.execute('UPDATE pantry SET name = ?, in_stock = ? WHERE id = ?', (name_new, in_stock, item_id))
        conn.commit()

def delete_item(name, conn, cursor):
    name = name.lower()
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
            create_item(name, in_stock, conn, cursor)
            added_items.append(name.lower())
        except sqlite3.IntegrityError:
            not_added_items.append(name.lower())
    
    if not_added_items and added_items:
        return f'Following items were added to the pantry: {", ".join(added_items)}.\
              These items were already in the pantry: {not_added_items}.'
    if not_added_items:
        return f'The following items are already logged in the pantry: {", ".join(not_added_items)}.'
    if added_items:
        return f'The following items have been added to the pantry: {", ".join(added_items)}.'  


def delete_items(names, conn, cursor):   
    not_found_items = []
    deleted_items = []

    for name in names:
        name = name.lower()
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
    # Execute a SELECT query to fetch all rows ingredients in stock.
    cursor.execute("SELECT * FROM pantry WHERE in_stock == True")
    rows = cursor.fetchall()
    # Write the data to a CSV-formatted string
    csv_output = io.StringIO()
    writer = csv.writer(csv_output)

    # Write header
    writer.writerow(['ID', 'Name', 'In Stock'])

    # Write rows
    for row in rows:
        converted_row = row[0], row[1], bool(row[2])
        writer.writerow(converted_row)

    # Get the CSV-formatted string
    csv_string = csv_output.getvalue()

    # Close the StringIO object
    csv_output.close()

    return csv_string
