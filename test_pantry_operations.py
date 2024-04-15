import sqlite3
import pytest

# Import functions from the module
from food_list import connect_to_db, create_item, read_items, update_item, delete_item, create_items, delete_items

@pytest.fixture
def temp_db():
    # Set up a temporary in-memory database for testing
    conn, cursor = connect_to_db(':memory:')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pantry (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            in_stock BOOLEAN
        )
    ''')
    yield conn, cursor
    # Close the database connection after each test
    conn.close()

def test_create_item(temp_db):
    conn, cursor = temp_db
    # Test creating a single item
    create_item('Flour', True, conn, cursor)
    items = read_items(conn, cursor)
    assert len(items) == 1
    assert items[0][1] == 'flour'
    assert items[0][2] is 1

def test_read_items(temp_db):
    conn, cursor = temp_db
    # Test reading items from the database
    create_item('Sugar', True, conn, cursor)
    create_item('Salt', False, conn, cursor)
    items = read_items(conn, cursor)
    assert len(items) == 2

def test_update_item(temp_db):
    conn, cursor = temp_db
    # Test updating an item in the database
    create_item('Milk', True, conn, cursor)
    update_item('milk', 'Soy Milk', False, conn, cursor)
    items = read_items(conn, cursor)
    assert items[0][1] == 'soy milk'
    assert items[0][2] is 0

def test_delete_item(temp_db):
    conn, cursor = temp_db
    # Test deleting an item from the database
    create_item('Eggs', True, conn, cursor)
    delete_item('eggs', conn, cursor)
    items = read_items(conn, cursor)
    assert len(items) == 0

def test_create_items(temp_db):
    conn, cursor = temp_db
    # Test creating multiple items at once
    create_items(['Tomatoes', 'Onions', 'Garlic'], conn, cursor)
    items = read_items(conn, cursor)
    assert len(items) == 3

def test_delete_items(temp_db):
    conn, cursor = temp_db
    # Test deleting multiple items at once
    create_items(['Tomatoes', 'Onions', 'Garlic', 'Potato'], conn, cursor)
    delete_items(['tomatoes', 'potato', 'onions'], conn, cursor)
    items = read_items(conn, cursor)
    assert len(items) == 1
