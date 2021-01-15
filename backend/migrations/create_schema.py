import sqlite3

connection = sqlite3.connect('MyRecipes.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE users (
        UserID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE receitas (
        ReceitaID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        texto TEXT NOT NULL,
        autor INTEGER NOT NULL,
        FOREIGN KEY (autor) REFERENCES users(UserID)
    );
""")



print('Users table created')
connection.close()