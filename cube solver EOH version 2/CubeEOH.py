import tkinter as tk
from tkinter import messagebox
import heapq
import time


class Cube:
    def __init__(self, state):
        if isinstance(state, Cube):
            self.state = list(state.state)
        else:
            self.state = list(state)

    def is_solved(self):
        solved_state = "RRRRRRRRRGGGGGGGGGWWWWWWWWWOOOOOOOOOBBBBBBBBBYYYYYYYYY"
        return self.state == solved_state
    
    def get_edges(self):
        if isinstance(self.state, str) and len(self.state) >= 19:
            edges = [
                self.state[9], self.state[10], self.state[11],
                self.state[18], '', self.state[12],
                self.state[17], self.state[16], self.state[15],
            ]
            return edges
        else:
            return []

    def get_neighbors(self):
        neighbors = []

        # Rotate the top face clockwise
        cube_copy = Cube(self.rotate_up_clockwise())
        neighbors.append(cube_copy)

        # Rotate the top face counterclockwise
        cube_copy = Cube(self.rotate_up_counter_clockwise())
        neighbors.append(cube_copy)

        # Rotate the right face clockwise
        cube_copy = Cube(self.rotate_right_clockwise())
        neighbors.append(cube_copy)

        # Rotate the right face counterclockwise
        cube_copy = Cube(self.rotate_right_counter_clockwise())
        neighbors.append(cube_copy)

        return neighbors
    
    def get_move_to(self, neighbor):
        moves = {
            'rotate_up_clockwise': 'U',
            'rotate_up_counter_clockwise': "U'",
            'rotate_right_clockwise': 'R',
            'rotate_right_counter_clockwise': "R'"
        }

        for method_name, move in moves.items():
            method = getattr(self, method_name)
            if method() == neighbor.state:
                return move

        return None


    def rotate_up_clockwise(self):
        temp = self.state[0]
        self.state[0] = self.state[2]
        self.state[2] = self.state[3]
        self.state[3] = self.state[1]
        self.state[1] = temp

        temp = self.state[4]
        self.state[4] = self.state[7]
        self.state[7] = self.state[6]
        self.state[6] = self.state[5]
        self.state[5] = temp

        return self.state

    def rotate_up_counter_clockwise(self):
        temp = self.state[0]
        self.state[0] = self.state[1]
        self.state[1] = self.state[3]
        self.state[3] = self.state[2]
        self.state[2] = temp

        temp = self.state[4]
        self.state[4] = self.state[5]
        self.state[5] = self.state[6]
        self.state[6] = self.state[7]
        self.state[7] = temp

        return self.state

    def rotate_right_clockwise(self):
        temp = self.state[0]
        self.state[0] = self.state[1]
        self.state[1] = self.state[5]
        self.state[5] = self.state[4]
        self.state[4] = temp

        temp = self.state[2]
        self.state[2] = self.state[3]
        self.state[3] = self.state[7]
        self.state[7] = self.state[6]
        self.state[6] = temp

        temp = self.state[8]
        self.state[8] = self.state[9]
        self.state[9] = self.state[13]
        self.state[13] = self.state[12]
        self.state[12] = temp

        temp = self.state[10]
        self.state[10] = self.state[11]
        self.state[11] = self.state[15]
        self.state[15] = self.state[14]
        self.state[14] = temp

        temp = self.state[16]
        self.state[16] = self.state[17]
        self.state[17] = self.state[19]
        self.state[19] = self.state[18]
        self.state[18] = temp

        return self.state

    def rotate_right_counter_clockwise(self):
        temp = self.state[0]
        self.state[0] = self.state[4]
        self.state[4] = self.state[5]
        self.state[5] = self.state[1]
        self.state[1] = temp

        temp = self.state[2]
        self.state[2] = self.state[6]
        self.state[6] = self.state[7]
        self.state[7] = self.state[3]
        self.state[3] = temp

        temp = self.state[8]
        self.state[8] = self.state[12]
        self.state[12] = self.state[13]
        self.state[13] = self.state[9]
        self.state[9] = temp

        temp = self.state[10]
        self.state[10] = self.state[14]
        self.state[14] = self.state[15]
        self.state[15] = self.state[11]
        self.state[11] = temp

        temp = self.state[16]
        self.state[16] = self.state[18]
        self.state[18] = self.state[19]
        self.state[19] = self.state[17]
        self.state[17] = temp

        return self.state
    
    def get_edge_orientation_heuristic(self):
        # Calculate the edge-orientation heuristic value for the current state
        edges = self.get_edges()
        orientations = [edge.get_orientation() for edge in edges]
        # A solved cube has all edges oriented the same way (0), so count how many edges need to be rotated
        return sum([orientation for orientation in orientations if orientation != 0])



def a_star_solver(cube, move_limit=100000):
    open_set = [(0, cube)]  # priority queue
    closed_set = set()
    move_count = 0  # Number of moves taken to solve the cube
    solution_moves = []
    start_time = time.time()  # Start time for measuring the solving time

    while open_set and move_count < move_limit:
        _, current = heapq.heappop(open_set)  # pop the cube with the lowest f-score
        if current.is_solved():
            end_time = time.time()  # End time for measuring the solving time
            solving_time = end_time - start_time  # Calculate the solving time
            solution_moves = [move for move in reversed(solution_moves)]  # Reverse the list of moves for readability
            return True, move_count, solution_moves, solving_time

        closed_set.add(current)

        for neighbor_state in current.get_neighbors():
            neighbor = Cube(neighbor_state)

            if neighbor in closed_set:
                continue

            # Calculate g-score and h-score
            g_score = move_count + 1  # Calculate g-score
            h_score = neighbor.get_edge_orientation_heuristic()  # Calculate h-score
            f_score = g_score + h_score  # Calculate f-score

            for i, (_, neighbor_in_open_set) in enumerate(open_set):
                if neighbor == neighbor_in_open_set and f_score >= neighbor_in_open_set.get_f_score():
                    break
            else:
                move_count += 1  # Increment the move count
                heapq.heappush(open_set, (f_score, neighbor))
                # Add the current move to the list of solution moves
                solution_moves.append(current.get_move_to(neighbor))

    end_time = time.time()  # End time for measuring the solving time
    solving_time = end_time - start_time  # Calculate the solving time
    return False, move_count, solution_moves, solving_time


def retrieve_edges_from_string(cube_string):
    return list(cube_string)


def solve_cube():
    input_string = entry.get()
    cube = Cube(retrieve_edges_from_string(input_string))

    success, move_count, solution_moves, solving_time = a_star_solver(cube)

    if success:
        messagebox.showinfo(
            "Solution", f"Solved in {move_count} moves ({solving_time:.2f} seconds):\n" + " ".join(solution_moves)
        )
    else:
        messagebox.showerror("Error", "Cube could not be solved.")


root = tk.Tk()
root.title("Rubik's Cube Solver")

# Create GUI elements
tk.Label(root, text="Enter the edge pieces of the Rubik's Cube as a string:").pack()
entry = tk.Entry(root, width=40)
entry.pack()

solve_button = tk.Button(root, text="Solve", command=solve_cube)
solve_button.pack()

root.mainloop()
