from sys import argv
from connect import create_database
from project import app
from project.models import User


if __name__ == '__main__':
    if (len(argv) > 1):
        if (argv[1] == '-db'):
            with app.app_context():
                create_database()
    app.run()