import sqlite3

def connect_to_database():
    return sqlite3.connect("gym.db")

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    if len(cursor.fetchall()) == 0:
        cursor.execute("CREATE TABLE journal(date, exercise, set_n, reps, weight)")
    return cursor