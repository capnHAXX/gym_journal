import tkinter as tk
from tkinter import *
from tkinter import messagebox
from exercise import Set
from data import *
from datetime import datetime


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
        exercise_button.pack(side=LEFT)
        csv_button = tk.Button(self.__canvas, text="Export CSV", command=self.export_to_csv)
        csv_button.pack(side=RIGHT)

    def export_to_csv(self):
        try:
            connection = connect_to_database()
            generate_csv(connection)
        finally:
            connection.close()
            print("Connection closed.")

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

        generate_button = tk.Button(self.__canvas, text="OK", command=lambda: self.generate_exercise_ok(date_entry, exercise_entry, total_sets_entry)) #ok button calls save_exercise
        generate_button.pack(anchor='w', padx=10, pady=5)
        cancel_button = tk.Button(self.__canvas, text="Cancel", command=self.cancel)
        cancel_button.pack(anchor='w', padx=10, pady=5)

        self.sets_frame = Frame(self.__canvas)
        self.sets_frame.pack(fill = BOTH, padx = 10, pady = 5)
    
    def generate_exercise_ok(self, date_entry, exercise_entry, total_sets_entry):
        date_value = date_entry.get()
        exercise_value = exercise_entry.get()
        total_sets_value = int(total_sets_entry.get())
        try:
            datetime.strptime(date_value, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        
        if not exercise_value:
            messagebox.showerror("Input Error", "Exercise field cannot be blank.")
            return
        
        if total_sets_value <= 0:
            messagebox.showerror("Input Error", "Number of sets must be integer larger than 0")
            return


        for widget in self.__canvas.winfo_children():
            widget.destroy()
        self.generate_sets(date_value, exercise_value, total_sets_value)

    def cancel(self):
        for widget in self.__canvas.winfo_children():
            widget.destroy()
        self.main_screen()
    
    def generate_sets(self, date, exercise, total_sets): #initializes exercise object
        self.sets_frame = Frame(self.__canvas)
        self.sets_frame.pack(fill = BOTH, padx = 10, pady = 5)

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
        
        save_button = tk.Button(self.sets_frame, text = "Save", command=lambda: self.save_sets(set_entries, date, exercise))
        save_button.pack(anchor='w', padx=10, pady=5)
        cancel_button = tk.Button(self.__canvas, text="Cancel", command=self.cancel)
        cancel_button.pack(anchor='w', padx=10, pady=5)

    def save_sets(self, set_entries, date, exercise):
        for i in range(len(set_entries)):
            try:
                reps = int(set_entries[i][0].get())
                if reps < 0:
                    messagebox.showerror("Input Error", f"Set #{i+1}: Rep cannot be negative.")
                weight = int(set_entries[i][1].get())
                if weight < 0:
                    messagebox.showerror("Input Error", f"Set #{i+1}: Weight cannot be negative.")
                print(reps, weight)
                s = Set(date, exercise, i+1, reps, weight)
                s.add_set()
            except:
                messagebox.showerror("Input Error", f"Set #{i+1}: Reps and Weight must be valid integers.")
                return
        self.cancel()
        

    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
