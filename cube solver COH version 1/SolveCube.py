import tkinter as tk
from tkinter import messagebox
from CubeCOH import Cube, a_star_solver
from CubeCOH import retrieve_corners_from_string
import time

def solve_cube():
    input_string = entry.get()
    cube = Cube(retrieve_corners_from_string(input_string))

    success, move_count, solution_moves, solving_time = a_star_solver(cube)

    if success:
        result_label.config(text=f"Moves: {move_count}\nTime: {solving_time:.2f} seconds\nSolution: {solution_moves}")
        show_result()
    else:
        messagebox.showinfo("Result", "No solution found.")

# Create the main window
window = tk.Tk()
window.title("Rubik's Cube Solver")

# Create the input box
entry_label = tk.Label(window, text="Enter scrambled Rubik's Cube input string:")
entry_label.pack()
entry = tk.Entry(window)
entry.pack()

# Create the computation button
button = tk.Button(window, text="Solve", command=solve_cube)
button.pack()

# Create the result display window (a separate top-level window)
result_window = tk.Toplevel(window)
result_window.title("Result")

# Hide the result display window initially
result_window.withdraw()

# Function to show the result display window
def show_result():
    result_window.deiconify()

# Create a label to display the result
result_label = tk.Label(result_window, text="Solution will be displayed here")
result_label.pack()

# Create a button to close the result display window
close_button = tk.Button(result_window, text="Close", command=result_window.withdraw)
close_button.pack()

# Set the command to show the result display window when the computation is done
solve_cube.__globals__["show_result"] = show_result

# Start the GUI main loop
window.mainloop()