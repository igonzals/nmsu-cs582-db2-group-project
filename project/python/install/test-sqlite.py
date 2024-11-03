# /mnt/python/test-sqlite.py

import sqlite3

# Path to the SQLite database file
db_path = "/mnt/data/test.db"

# Connect to SQLite database (it will create test.db if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a sample table named "test"
cursor.execute('''
CREATE TABLE IF NOT EXISTS test (
  id INTEGER PRIMARY KEY,
  name TEXT
)
''')

# Insert some sample data
cursor.execute("INSERT INTO test (name) VALUES ('SQLite is well!')")
conn.commit()

# Query the data to verify the table and data creation
cursor.execute("SELECT * FROM test")
rows = cursor.fetchall()

# Print the results
for row in rows:
  print(row)

# Close the connection
conn.close()
