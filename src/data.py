import sqlite3
import csv

def connect_to_database():
    print("Connected to gym.db")
    return sqlite3.connect("gym.db")

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    if len(cursor.fetchall()) == 0:
        cursor.execute("CREATE TABLE journal(date DATE, exercise VARCHAR, set_n INT(8), reps INT(8), weight INT(8))")
    return cursor

def generate_csv(connection):
    cursor = connection.cursor()
    
    print("Generating CSV...")
    cursor.execute("SELECT * FROM journal")
    journal_data = cursor.fetchall()

    with open("journal.csv","w", newline="", encoding="utf-8") as open_csv:
        csv_writer = csv.writer(open_csv)
        csv_writer.writerow([header[0] for header in cursor.description])
        csv_writer.writerows(journal_data)
    
    print("Journal CSV generate. Please store CSV in safe location.")