import tkinter as tk
from tkinter import *
from exercise import Set


class Window:

    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Workout Tracker"
        self.__root.minsize(width, height)
        self.__canvas = Canvas(self.__root, bg="Grey", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.main_screen()
    
    def main_screen (self):
        welcome = tk.Label(self.__canvas, text="Welcome!")
        welcome.pack(side=TOP)
        exercise_button = tk.Button(self.__canvas, text="Enter Exercerise", command=self.generate_exercise)
        exercise_button.pack(anchor=W)
        chart_button = tk.Button(self.__canvas, text="View Progress")
        chart_button.pack(anchor=E)
        delete_button = tk.Button(self.__canvas, text="Delete Last Entry")
        delete_button.pack(anchor=S)

    #def generate_chart

    def generate_exercise(self): #creates initial entry fields for date, exercise and total number of sets
        for widget in self.__canvas.winfo_children():
            widget.destroy()
        date_label = tk.Label(self.__canvas, text="Enter date (YYYY-MM-DD):")
        date_label.pack(anchor='w', padx=10, pady=5)
        date_entry = tk.Entry(self.__canvas)
        date_entry.pack(fill=tk.X, padx=10, pady=5)

        exercise_label = tk.Label(self.__canvas, text="Exercise:")
        exercise_label.pack(anchor='w', padx=10, pady=5)
        exercise_entry = tk.Entry(self.__canvas)
        exercise_entry.pack(fill=tk.X, padx=10, pady=5)

        total_sets_label = tk.Label(self.__canvas, text="Total Sets:")
        total_sets_label.pack(anchor='w', padx=10, pady=5)
        total_sets_entry = tk.Entry(self.__canvas)
        total_sets_entry.pack(fill=tk.X, padx=10, pady=5)

        generate_button = tk.Button(self.__canvas, text="OK", command=lambda: self.generate_sets(date_entry, exercise_entry, total_sets_entry)) #ok button calls save_exercise
        generate_button.pack(anchor='w', padx=10, pady=5)
        cancel_button = tk.Button(self.__canvas, text="Cancel", command=self.cancel)
        cancel_button.pack(anchor='w', padx=10, pady=5)

        self.sets_frame = Frame(self.__canvas)
        self.sets_frame.pack(fill = BOTH, padx = 10, pady = 5)
    
    def cancel(self):
        for widget in self.__canvas.winfo_children():
            widget.destroy()
        self.main_screen()
    
    def generate_sets(self, date_entry, exercise_entry, total_sets_entry): #initializes exercise object
        
        total_sets = int(total_sets_entry.get())     
        if total_sets <= 0:
            raise ValueError("Total Sets must be integer greater than 0") #check to ensure total sets is an integer greater than 0
        
        set_entries = []
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

            set_entries.append((reps_entry, weight_entry))
        
        save_button = tk.Button(self.sets_frame, text = "Save", command=lambda: self.save_sets(set_entries, date_entry, exercise_entry))
        save_button.pack(anchor='w', padx=10, pady=5)

    def save_sets(self, set_entries, date_entry, exercise_entry):
        for i in range(len(set_entries)):
            reps = int(set_entries[i][0].get())
            weight = int(set_entries[i][1].get())
            print(reps, weight)
            s = Set(date_entry.get(), exercise_entry.get(), i+1, reps, weight)
            s.add_set()
        

    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
