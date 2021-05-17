import sqlite3
import project
from project import db

def create_database():
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    create_database()