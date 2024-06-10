import heapq
import tkinter as tk
from tkinter import messagebox
import time

class Cube:
    def __init__(self, state):
        self.state = list(state)

    def is_solved(self):
        return all(sticker == self.state[0] for sticker in self.state)

    def get_corners(self):
        return [self.state[0], self.state[2], self.state[6], self.state[8],
                self.state[45], self.state[47], self.state[51], self.state[53]]

    def corner_orientation_heuristic(self):
        corners = self.get_corners()
        orientations = {
            'R': 0, 'G': 0, 'W': 0, 'O': 0, 'B': 0, 'Y': 0
        }

        for corner in corners:
            if corner in orientations:
                orientations[corner] += 1

        return sum(orientations.values())

    def rotate_right_clockwise(self):
        temp = self.state[2]
        self.state[2] = self.state[8]
        self.state[8] = self.state[26]
        self.state[26] = self.state[20]
        self.state[20] = temp

        temp = self.state[5]
        self.state[5] = self.state[7]
        self.state[7] = self.state[25]
        self.state[25] = self.state[23]
        self.state[23] = temp

        temp = self.state[6]
        self.state[6] = self.state[14]
        self.state[14] = self.state[18]
        self.state[18] = self.state[10]
        self.state[10] = temp

        temp = self.state[9]
        self.state[9] = self.state[11]
        self.state[11] = self.state[17]
        self.state[17] = self.state[15]
        self.state[15] = temp

        temp = self.state[0]
        self.state[0] = self.state[24]
        self.state[24] = self.state[16]
        self.state[16] = self.state[2]
        self.state[2] = temp

        return self.state

    def rotate_right_counter_clockwise(self):
        temp = self.state[2]
        self.state[2] = self.state[20]
        self.state[20] = self.state[26]
        self.state[26] = self.state[8]
        self.state[8] = temp

        temp = self.state[5]
        self.state[5] = self.state[23]
        self.state[23] = self.state[25]
        self.state[25] = self.state[7]
        self.state[7] = temp

        temp = self.state[6]
        self.state[6] = self.state[10]
        self.state[10] = self.state[18]
        self.state[18] = self.state[14]
        self.state[14] = temp

        temp = self.state[9]
        self.state[9] = self.state[15]
        self.state[15] = self.state[17]
        self.state[17] = self.state[11]
        self.state[11] = temp

        temp = self.state[0]
        self.state[0] = self.state[2]
        self.state[2] = self.state[16]
        self.state[16] = self.state[24]
        self.state[24] = temp

        return self.state

    def get_neighbors(self):
        neighbors = []
        cube_copy = Cube(''.join(self.state))

        cube_copy.rotate_right_clockwise()
        neighbors.append(cube_copy)

        cube_copy = Cube(''.join(self.state))
        cube_copy.rotate_right_counter_clockwise()
        neighbors.append(cube_copy)

        return neighbors

    def get_move_to(self, neighbor):
        if neighbor.rotate_right_clockwise() == self.state:
            return "R"
        elif neighbor.rotate_right_counter_clockwise() == self.state:
            return "R'"

        return ""

    def __lt__(self, other):
        return self.corner_orientation_heuristic() < other.corner_orientation_heuristic()

def a_star_search(start):
    if start.is_solved():
        return []

    open_list = []
    heapq.heapify(open_list)
    heapq.heappush(open_list, (start.corner_orientation_heuristic(), start))

    closed_set = set()

    came_from = {}
    g_score = {start: 0}
    f_score = {start: start.corner_orientation_heuristic()}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current.is_solved():
            path = []
            while current in came_from:
                move = current.get_move_to(came_from[current])
                path.append(move)
                current = came_from[current]
            path.reverse()
            return path

        closed_set.add(current)

        for neighbor in current.get_neighbors():
            tentative_g_score = g_score[current] + 1

            if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + neighbor.corner_orientation_heuristic()
                if (f_score[neighbor], neighbor) not in open_list:
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

def solve_cube():
    cube_state = entry.get()

    if len(cube_state) != 54:
        messagebox.showerror("Error", "Invalid cube state! Please enter a valid state.")
        return

    cube = Cube(cube_state)

    start_time = time.time()
    solution = a_star_search(cube)
    end_time = time.time()

    if solution is None:
        messagebox.showerror("Error", "No solution found!")
    else:
        messagebox.showinfo("Solution", f"Solution: {' '.join(solution)}\nTime: {end_time - start_time:.5f} seconds")

window = tk.Tk()
window.title("Cube Solver")

label = tk.Label(window, text="Enter the cube state:")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Solve", command=solve_cube)
button.pack()

window.mainloop()
