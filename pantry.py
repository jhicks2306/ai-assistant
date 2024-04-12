import sqlite3
import csv
import io
from datetime import date, timedelta

class Pantry:
    def __init__(self, db_path):
        self.today = date.today()
        self.conn = sqlite3.connect(str(db_path))
        self.cursor = self.conn.cursor()
    
    def create_item(self, name):
        self.cursor.execute('INSERT INTO pantry (name, date_added) VALUES (?, ?)', (name, self.today))
        self.conn.commit()

    def read_items(self):
        self.cursor.execute('SELECT * FROM pantry')
        items = self.cursor.fetchall()
        return items

    def update_item(self, name_old, name_new):
        item_id = self.get_item_id(name_old)
        if item_id is None:
            print('There is no item in the pantry matching this name')
        else:
            self.cursor.execute('UPDATE pantry SET name = ?, date_added = ? WHERE id = ?', (name_new, self.today, item_id))
            self.conn.commit()

    def delete_item(self, name):
        self.cursor.execute('DELETE FROM pantry WHERE name = ?', (name,))
        self.conn.commit()

    def get_item_id(self, name):  
        self.cursor.execute('SELECT id FROM pantry WHERE name = ?', (name,))
        item = self.cursor.fetchone()
        
        if item:
            return item[0]  # Return the item ID
        else:
            return None  # Return None if item not found

    def create_items(self, names):
        added_items = []
        not_added_items = []
        for name in names:
            try:
                self.create_item(name)
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


    def delete_items(self, names):   
        not_found_items = []
        deleted_items = []

        for name in names:
            self.delete_item(name)
            deleted_items.append(name)
            if self.cursor.rowcount == 0:  # Check if any rows were affected by the delete operation
                not_found_items.append(name)
        
        self.conn.commit()
        
        if not_found_items:
            msg = "The following items were not found in the database and couldn't be deleted:"
            for item in not_found_items:
                msg = msg + "\n" + item
            return msg
        else:
            return f'The following items have been removed from the pantry: {", ".join(deleted_items)}.'  
    
    def to_csv(self):
        """Returns string of items in stock in CSV format."""
        # Execute a SELECT query to fetch all ingredients in stock.
        self.cursor.execute("SELECT name FROM pantry")
        rows = self.cursor.fetchall()
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
    
    def to_string(self):
        """Returns comma separated string of items in the pantry."""
        # Execute a SELECT query to fetch all ingredients in stock.
        self.cursor.execute("SELECT name FROM pantry")

        # Fetch all the rows and extract names
        names = [row[0] for row in self.cursor.fetchall()]
        # Write header
        names_str = ", ".join(names)

        return names_str
