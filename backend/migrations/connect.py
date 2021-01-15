import sqlite3

conn = sqlite3.connect('MyRecipes.db')
print("conectado")
conn.close()
