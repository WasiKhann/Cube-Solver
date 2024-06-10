import heapq
import time


class Cube:
    def __init__(self, state):
        if isinstance(state, Cube):
            self.state = list(state.state)
        else:
            self.state = list(state)

    def is_solved(self):
        solved_state = "WWWWWWWWWGGGGGGGGGRRRRRRRRRBBBBBBBBBOOOOOOOOOYYYYYYYYY"
        return self.state == solved_state

    def get_corners(self):
        if isinstance(self.state, str) and len(self.state) >= 27:
            corners = [
                self.state[0], self.state[1], self.state[2],
                self.state[9], '', self.state[10],
                self.state[18], self.state[19], self.state[20],
                self.state[27], self.state[28], self.state[29],
                self.state[36], self.state[37], self.state[38],
                self.state[45], self.state[46], self.state[47],
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

    def get_corner_orientation_heuristic(self):
        # Calculate the corner orientation heuristic value for the current state
        corners = self.get_corners()
        orientations = [corner.get_orientation() for corner in corners]
        # A solved cube has all corners oriented the same way (0), so count how many corners need to be rotated
        return sum([orientation for orientation in orientations if orientation != 0])


def a_star_search(cube, move_limit=100000):
    open_set = [(0, cube)]  # priority queue
    closed_set = set()
    came_from = {}
    g_score = {cube: 0}
    move_count = 0  # Number of moves taken to solve the cube
    solution_moves = []
    start_time = time.time()  # Start time for measuring the solving time

    while open_set and move_count < move_limit:
        _, current = heapq.heappop(open_set)  # pop the cube with the lowest f-score
        if current.is_solved():
            end_time = time.time()  # End time for measuring the solving time
            solving_time = end_time - start_time  # Calculate the solving time
            solution_moves = [move for move in reversed(solution_moves)]  # Reverse the solution moves
            print("Cube solved in {} moves. Solving time: {:.2f}s".format(move_count, solving_time))
            return solution_moves

        closed_set.add(current)

        for neighbor in current.get_neighbors():
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in [cube for _, cube in open_set]:
                heapq.heappush(open_set, (tentative_g_score + neighbor.get_corner_orientation_heuristic(), neighbor))
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score

        move_count += 1

    print("Cube could not be solved in {} moves.".format(move_limit))
    return []


def solve_cube(cube_state):
    cube = Cube(cube_state)
    solution = a_star_search(cube)
    return solution


# Example usage
cube_state = "WWWWWWWWWGGGGGGGGGRRRRRRRRRBBBBBBBBBOOOOOOOOOYYYYYYYYY"
solution = solve_cube(cube_state)
print(solution)
