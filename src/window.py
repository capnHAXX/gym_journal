import tkinter as tk
from tkinter import *
from exercise import Set
from data import *

class Window:

    def __init__(self, width, height):
        self.connection = connect_to_database() #see data for more: using sqlite
        self.cursor = create_table(self.connection)
        self.__root = Tk()
        self.__root.title = "Workout Tracker"
        self.__canvas = Canvas(self.__root, bg="Grey", width=width, height=height)
        self.__canvas.pack(fill = BOTH, expand = True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.generate_exercise()
    
    def generate_exercise(self): #creates initial entry fields for date, exercise and total number of sets
        self.date_label = tk.Label(self.__canvas, text="Enter date (YYYY-MM-DD):")
        self.date_label.pack(anchor='w', padx=10, pady=5)
        self.date_entry = tk.Entry(self.__canvas)
        self.date_entry.pack(fill=tk.X, padx=10, pady=5)

        self.exercise_label = tk.Label(self.__canvas, text="Exercise:")
        self.exercise_label.pack(anchor='w', padx=10, pady=5)
        self.exercise_entry = tk.Entry(self.__canvas)
        self.exercise_entry.pack(fill=tk.X, padx=10, pady=5)

        self.total_sets_label = tk.Label(self.__canvas, text="Total Sets:")
        self.total_sets_label.pack(anchor='w', padx=10, pady=5)
        self.total_sets_entry = tk.Entry(self.__canvas)
        self.total_sets_entry.pack(fill=tk.X, padx=10, pady=5)

        generate_button= tk.Button(self.__canvas, text="OK", command=self.generate_sets) #ok button calls save_exercise
        generate_button.pack(anchor='w', padx=10, pady=5)

        self.sets_frame = tk.Frame(self.__canvas)
        self.sets_frame.pack(fill = BOTH, padx = 10, pady = 5)
    
    def generate_sets(self): #initializes exercise object
        
        total_sets = int(self.total_sets_entry.get())     
        if total_sets <= 0:
            raise ValueError("Total Sets must be integer greater than 0") #check to ensure total sets is an integer greater than 0
        
        self.set_entries = []
        for i in range(total_sets):
            set_label = tk.Label(self.sets_frame, text=f"Set #{i+1}")
            set_label.pack(anchor='w', padx=10, pady=5)

            reps_label = tk.Label(self.sets_frame, text="Number of reps")
            reps_label.pack(anchor='w', padx=10, pady=5)
            reps_entry = tk.Entry(self.sets_frame)
            reps_entry.pack(fill=tk.X, padx=10, pady=5)

            weight_label = tk.Label(self.sets_frame, text="Weight in lbs")
            weight_label.pack(anchor='w', padx=10, pady=5)
            weight_entry = tk.Entry(self.sets_frame)
            weight_entry.pack(fill=tk.X, padx=10, pady=5)

            self.set_entries.append((reps_entry, weight_entry))
        
        save_button = tk.Button(self.sets_frame, text = "Save", command=self.save_sets)
        save_button.pack(anchor='w', padx=10, pady=5)

    def save_sets(self):
        
        for i in range(len(self.set_entries)):
            reps = int(self.set_entries[i][0].get())
            weight = int(self.set_entries[i][1].get())
            print(reps, weight)
            s = Set(self.date_entry.get(), self.exercise_entry.get(), i+1, reps, weight)
            s.add_set(self.cursor)
        self.connection.commit()

    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
