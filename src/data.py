import sqlite3

def connect_to_database():
    return sqlite3.connect("gym.db")

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    if len(cursor.fetchall()) == 0:
        cursor.execute("CREATE TABLE journal(date DATE, exercise VARCHAR, set_n INT(8), reps INT(8), weight INT(8))")
    return cursor