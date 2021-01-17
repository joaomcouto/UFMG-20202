from sys import argv
from connect import create_database
from project import app


if __name__ == '__main__':
    if (len(argv) > 1):
        if (argv[1] == '-db'):
            create_database()
    app.run()