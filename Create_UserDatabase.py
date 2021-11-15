import sqlite3

conn = sqlite3.connect("UserDatabase.db")
print("Opened database successfully")

conn.execute('CREATE TABLE Users (user_id TEXT, email TEXT, first_name TEXT, last_name TEXT, pword TEXT, date_joined TEXT, address TEXT, city TEXT, role TEXT)')
print("Table created successfully")
conn.close()