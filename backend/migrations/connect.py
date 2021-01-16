import sqlite3

connection = sqlite3.connect('MyRecipes.db')
print("conectado")
connection.close()
