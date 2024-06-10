import tkinter as tk
from tkinter import messagebox
import heapq
import time


class Cube:
    EDGE_ORIENTATIONS = {
        'R': 0, 'G': 0, 'W': 0, 'O': 0, 'B': 0, 'Y': 0,
        'r': 1, 'g': 1, 'w': 1, 'o': 1, 'b': 1, 'y': 1,
    }

    CORNER_ORIENTATIONS = {
        'R': 0, 'G': 0, 'W': 0, 'O': 0, 'B': 0, 'Y': 0,
        'r': 1, 'g': 1, 'w': 1, 'o': 1, 'b': 1, 'y': 1,
        'X': 2, 'x': 2, 'A': 2, 'a': 2, 'U': 2, 'u': 2,
    }

    SOLVED_STATES = [
        "RRRRRRRRRGGGGGGGGGWWWWWWWWWOOOOOOOOOBBBBBBBBBYYYYYYYYY",
        "OOOOOOOOOYYYYYYYYYRRRRRRRRRGGGGGGGGGWWWWWWWWWBBBBBBBBB",
        "GGGGGGGGGRRRRRRRRROOOOOOOOOWWWWWWWWWYYYYYYYYYBBBBBBBBB",
        "WWWWWWWWWGGGGGGGGGYYYYYYYYYRRRRRRRRROOOOOOOOOWBBBBBBBBB",
        "BBBBBBBBBWWWWWWWWWOOOOOOOOOGGGGGGGGGYYYYYYYYYRRRRRRRRR",
        "YYYYYYYYYOOOOOOOOOBBBBBBBBBWWWWWWWWWGGGGGGGGGRRRRRRRRR"
    ]

    def __init__(self, state):
        self.state = state

    def is_solved(self):
        return self.state in self.SOLVED_STATES

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

    def get_corners(self):
        if isinstance(self.state, str) and len(self.state) >= 19:
            corners = [
                self.state[0], self.state[1], self.state[2],
                self.state[3], self.state[4], self.state[5],
                self.state[6], self.state[7], self.state[8],
            ]
            return corners
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

    def rotate_up_clockwise(self):
        state = list(self.state)
        temp = state[0]
        state[0] = state[2]
        state[2] = state[3]
        state[3] = state[1]
        state[1] = temp

        temp = state[4]
        state[4] = state[7]
        state[7] = state[6]
        state[6] = state[5]
        state[5] = temp

        return ''.join(state)

    def rotate_up_counter_clockwise(self):
        state = list(self.state)
        temp = state[0]
        state[0] = state[1]
        state[1] = state[3]
        state[3] = state[2]
        state[2] = temp

        temp = state[4]
        state[4] = state[5]
        state[5] = state[6]
        state[6] = state[7]
        state[7] = temp

        return ''.join(state)

    def rotate_right_clockwise(self):
        state = list(self.state)
        temp = state[0]
        state[0] = state[1]
        state[1] = state[5]
        state[5] = state[4]
        state[4] = temp

        temp = state[2]
        state[2] = state[3]
        state[3] = state[7]
        state[7] = state[6]
        state[6] = temp

        temp = state[8]
        state[8] = state[9]
        state[9] = state[13]
        state[13] = state[12]
        state[12] = temp

        temp = state[10]
        state[10] = state[11]
        state[11] = state[15]
        state[15] = state[14]
        state[14] = temp

        temp = state[16]
        state[16] = state[17]
        state[17] = state[19]
        state[19] = state[18]
        state[18] = temp

        return ''.join(state)

    def rotate_right_counter_clockwise(self):
        state = list(self.state)
        temp = state[0]
        state[0] = state[4]
        state[4] = state[5]
        state[5] = state[1]
        state[1] = temp

        temp = state[2]
        state[2] = state[6]
        state[6] = state[7]
        state[7] = state[3]
        state[3] = temp

        temp = state[8]
        state[8] = state[12]
        state[12] = state[13]
        state[13] = state[9]
        state[9] = temp

        temp = state[10]
        state[10] = state[14]
        state[14] = state[15]
        state[15] = state[11]
        state[11] = temp

        temp = state[16]
        state[16] = state[18]
        state[18] = state[19]
        state[19] = state[17]
        state[17] = temp

        return ''.join(state)

    def get_edge_orientation_heuristic(self):
        orientations = [self.EDGE_ORIENTATIONS[edge] for edge in self.get_edges()]
        return sum(orientations)

    def get_corner_orientation_heuristic(self):
        orientations = [self.CORNER_ORIENTATIONS[corner] for corner in self.get_corners()]
        return sum(orientations)

    def get_manhattan_distance(self):
        distance = self.get_edge_orientation_heuristic() + self.get_corner_orientation_heuristic()
        return distance

    def __lt__(self, other):
        return self.get_manhattan_distance() < other.get_manhattan_distance()


def get_move_to(cube, target):
    if cube.state == target:
        return []

    queue = [(cube.get_manhattan_distance(), 0, cube)]
    heapq.heapify(queue)
    visited = set()

    while queue:
        _, moves, current_cube = heapq.heappop(queue)
        visited.add(current_cube.state)

        for neighbor in current_cube.get_neighbors():
            if neighbor.state == target:
                return moves + 1

            if neighbor.state not in visited:
                visited.add(neighbor.state)
                heapq.heappush(queue, (neighbor.get_manhattan_distance() + moves + 1, moves + 1, neighbor))

    return -1


"""""
def is_solved(cube):
    return cube.is_solved()


def solve_cube(cube):
    start_time = time.time()
    moves = get_move_to(cube, cube.SOLVED_STATES[0])cl
    end_time = time.time()

    if moves == -1:
        messagebox.showinfo("Rubik's Cube Solver", "Unable to solve the cube.")
    else:
        messagebox.showinfo("Rubik's Cube Solver", f"Solved the cube in {moves} moves in {end_time - start_time} seconds.")


if __name__ == "__main__":
    # Test the solver
    test_cube = Cube("RRRRRRRRRGGGGGGGGGWWWWWWWWWOOOOOOOOOBBBBBBBBBYYYYYYYYY")
    solve_cube(test_cube)
"""