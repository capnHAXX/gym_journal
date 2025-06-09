import datetime
from data import *

class Set:

    def __init__(self, date = datetime.date.today(), exercise = "misc", set_n = 1, reps = 10, weight = 0):
        self.date = date
        self.exercise = exercise
        self.set_n = set_n
        self.reps = reps
        self.weight = weight
    
    def add_set(self):
        try:
            connection = connect_to_database()
            cursor = create_table(connection)
            cursor.execute("INSERT INTO journal(date, exercise, set_n, reps, weight) VALUES(?, ?, ?, ?, ?)",
                           (self.date, self.exercise, self.set_n, self.reps, self.weight))
            connection.commit()
        except Exception as e:
            raise e
        finally:
            connection.close()
            print("Connection closed.")