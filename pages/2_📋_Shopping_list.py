import streamlit as st
import sqlite3
import pandas as pd
from project_config import ProjectConfig

st.set_page_config(page_title="Shopping list", page_icon="📋")

# Connect to the SQLite database
DB_PATH = ProjectConfig.DB_PATH
conn = sqlite3.connect(DB_PATH)

# Execute SQL query to select all rows from the shopping list table
cur = conn.cursor()
cur.execute("SELECT * FROM pantry") # TODO: Create shopping list table.
rows = cur.fetchall()

# Get column names
col_names = [desc[0] for desc in cur.description]

# Close the cursor and connection
cur.close()
conn.close()

# Convert the rows and add column display names to a pandas dataframe
shopping_df = pd.DataFrame(rows, columns=col_names)
column_mapping = {
                'id': 'id',
                'name': 'Item',
                'date_added': 'Date Added',
            }
# Apply transformations for display purposes.
shopping_df.set_index('id', inplace=True)
shopping_df['name'] = shopping_df['name'].apply(lambda x: x.capitalize())
shopping_df.rename(columns=column_mapping, inplace=True)

### the Shopping list page ###
st.markdown("# Shopping list 📋")

# SAMPLE SHOPPING LIST
shopping_df = pd.DataFrame({'Item': ['Aubergine', 'Lentils', 'Ginger'], 'Purchased': [False, False, False]})

# Render DataFrame
edited_df = st.data_editor(shopping_df, use_container_width=True, hide_index=True)