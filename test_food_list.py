import unittest
import sqlite3
from datetime import date
from food_list import FoodList

class TestFoodList(unittest.TestCase):
    def setUp(self):
        self.db_path = ":memory:"
        self.table = "foods"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f'''CREATE TABLE {self.table} (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        date_added DATE
    )''')
        print(f"Table {self.table} created successfully")
        self.food_list = FoodList(self.db_path, self.table, self.conn, self.cursor)

    def tearDown(self):
        self.cursor.execute(f"DROP TABLE {self.table}")
        self.conn.close()

    def test_create_item(self):
        self.food_list.create_item("apple")
        self.cursor.execute(f"SELECT * FROM {self.table}")
        items = self.cursor.fetchall()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][1], "apple")

    def test_read_items(self):
        self.cursor.execute(f"INSERT INTO {self.table} (name, date_added) VALUES (?, ?)", ("apple", date.today()))
        self.cursor.execute(f"INSERT INTO {self.table} (name, date_added) VALUES (?, ?)", ("banana", date.today()))
        items = self.food_list.read_items()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0][1], "apple")
        self.assertEqual(items[1][1], "banana")

    def test_update_item(self):
        self.food_list.create_item("apple")
        self.food_list.update_item("apple", "orange")
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE name = 'orange'")
        item = self.cursor.fetchone()
        self.assertIsNotNone(item)
        self.assertEqual(item[1], "orange")

    def test_delete_item(self):
        self.food_list.create_item("apple")
        self.food_list.delete_item("apple")
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE name = 'apple'")
        item = self.cursor.fetchone()
        self.assertIsNone(item)
    
    def test_get_item(self):
        self.food_list.create_item("apple")
        item_id = self.food_list.get_item_id("apple")
        self.assertIsNotNone(item_id)
        item_id = self.food_list.get_item_id("non_existing_item")
        self.assertIsNone(item_id)

    def test_create_items(self):
        self.food_list.create_items(["apple", "banana", "orange"])
        self.cursor.execute(f"SELECT * FROM {self.table}")
        items = self.cursor.fetchall()
        self.assertEqual(items[0][1], "apple")
        self.assertEqual(items[1][1], "banana")
        self.assertEqual(items[2][1], "orange")

    def test_delete_items(self):
        self.cursor.execute(f"INSERT INTO {self.table} (name, date_added) VALUES (?, ?)", ("apple", date.today()))
        self.cursor.execute(f"INSERT INTO {self.table} (name, date_added) VALUES (?, ?)", ("banana", date.today()))
        self.food_list.delete_items(["apple", "banana"])
        items = self.cursor.fetchall()
        self.cursor.execute(f"SELECT * FROM {self.table}")
        self.assertEqual(items, [])

    def test_to_string(self):
        self.food_list.create_item("apple")
        self.food_list.create_item("banana")
        self.food_list.create_item("orange")
        items_str = self.food_list.to_string()
        self.assertEqual(items_str, "apple, banana, orange")


