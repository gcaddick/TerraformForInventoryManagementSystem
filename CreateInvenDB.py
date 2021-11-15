import sqlite3

conn = sqlite3.connect("InventoryDatabase.db")
print("Opened database successfully")

conn.execute('CREATE TABLE Inventory (prod_ID TEXT, prod_name TEXT, price TEXT, desc TEXT, quantity TEXT, auth TEXT, prod_url TEXT)')
print("Table created successfully")
conn.close()