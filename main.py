from time import time
import numpy as np

# Project for AI class
# Tec de Monterrey
# Benjamín Ávila Rosas
# Sept, 2022.

N = 3
target_state = []
# initial_state_array = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # 8-puzzle solution
initial_state_array = [2, 3, 0, 1, 6, 8, 4, 7, 5]
max_depth = 10
# initial_state_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]  # 15-puzzle solution
# initial_state_array = [0, 1, 3, 4, 5, 2, 6, 7, 10, 11, 12, 8, 9, 13, 14, 15]
# max_depth = 12
# initial_state_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 0]  # 24-puzzle solution
# initial_state_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 0, 18, 19, 21, 22, 23, 24, 20]
solution_node = None
steps_made = 0

# -- UNINFORMED PUZZLE SOLUTION --
# My uninformed puzzle solution uses Depth Limited Search Algorithm. The max_depth must be the amount of steps required
# to solve the puzzle, in case you assign a smaller max_depth, puzzle won't be able to be solved and in case max_depth
# is bigger, puzzle will be solved but with unnecessary movements. Program also requires to assign the puzzle initial
# state as an array and puzzle size with variable N at top of file. If N = 3, puzzle will have 3*3 spaces, that means it
# can sort up to (N*N)-1 tiles + a blank space. You might also need to uncomment the uninformed_8puzzle() method at
# the bottom of the file.

# Example:
# N = 3
# initial_state_array = [0, 1, 3, 5, 2, 6, 4, 7, 8]
# max_depth = 6


# -- INFORMED PUZZLE SOLUTION --
# My informed puzzle solution uses Greedy Best-First Algorithm. Program requires to assign the initial state of puzzle
# and puzzle size with variable N at top of file. If N = 3, puzzle will have 3*3 spaces, that means it can sort up to
# (N*N)-1 tiles + a blank space. You might also need to uncomment the uninformed_8puzzle() method at the bottom of
# the file.

# Example:
# N = 3
# initial_state_array = [0, 1, 3, 5, 2, 6, 4, 7, 8]


class SearchNode:
    def __init__(self, puzzle_state, heuristic_value, step, parent, children, target):
        self.puzzle_state = puzzle_state
        self.heuristic_value = heuristic_value
        self.step = step
        self.parent = parent
        self.children = children
        self.target = target

    def expand_possible_movements_dls(self):
        global solution_node, max_depth, steps_made

        location = search_blank_space(self.puzzle_state)
        available_movements = get_available_movements(location)

        for i in range(4):
            if available_movements[i] == 1:
                new_puzzle_state, target = move_tile(self.puzzle_state, location, i + 1)

                new_node = SearchNode(new_puzzle_state, self.heuristic_value, self.step + 1, self, [], target)
                self.children.append(new_node)

                if target == 1:
                    solution_node = new_node
                    break

        if solution_node is None and self.step <= max_depth:
            steps_made = self.step
            for x in range(len(self.children)):
                self.children[x].expand_possible_movements_dls()

    def expand_possible_movements_gbfs(self):
        global solution_node

        shortest_distance = 999999
        closest_node = None
        location = search_blank_space(self.puzzle_state)
        available_movements = get_available_movements(location)

        for i in range(4):
            if available_movements[i] == 1:
                new_puzzle_state, target = move_tile(self.puzzle_state, location, i + 1)
                new_state_manhattan_distance = get_manhattan_distance(new_puzzle_state, target_state)

                new_node = SearchNode(new_puzzle_state, new_state_manhattan_distance, self.step + 1, self, [], target)
                self.children.append(new_node)

        for i in range(len(self.children)):
            if self.children[i].heuristic_value < shortest_distance:
                shortest_distance = self.children[i].heuristic_value
                closest_node = self.children[i]

        print("--> STEP #" + str(closest_node.step))
        if closest_node.heuristic_value == 0:
            # Found solution
            solution_node = closest_node
            print_puzzle(closest_node.puzzle_state)
        else:
            # Keep searching for solution from the closest node found
            print_puzzle(closest_node.puzzle_state)
            print("Current Manhattan Distance: " + str(closest_node.heuristic_value) + "\n")
            closest_node.expand_possible_movements_gbfs()


def swap_values(puzzle_state, original_position, desired_position):
    original_value = puzzle_state[original_position[1], original_position[0]]
    desired_value = puzzle_state[desired_position[1], desired_position[0]]

    new_puzzle_state = puzzle_state.copy()
    new_puzzle_state[desired_position[1], desired_position[0]] = original_value
    new_puzzle_state[original_position[1], original_position[0]] = desired_value

    return new_puzzle_state


def get_manhattan_distance(current_state, final_state):
    initial = current_state.copy()
    total_distance = 0

    for i in range(N):
        for j in range(N):
            x1, y1 = find_target_position_for_tile(initial[i][j], final_state)
            x2, y2 = i, j
            tile_manhattan_distance = abs(x1 - x2) + abs(y1 - y2)

            total_distance += tile_manhattan_distance

    return total_distance


def find_target_position_for_tile(value, final_state):
    x1 = y1 = 0

    for i in range(N):
        for j in range(N):
            if final_state[i][j] == value:
                x1 = i
                y1 = j
                break

    return x1, y1


def check_puzzle_state(current_state, final_state):
    global N

    valid = 1

    for x in range(N):
        for y in range(N):
            if current_state[x][y] != final_state[x][y]:
                valid = 0
                break

    return valid


def move_tile(puzzle_state, location, direction):
    # 1 --> Left
    # 2 --> Right
    # 3 --> Up
    # 4 --> Down
    desired_location = []

    if direction == 1:
        desired_location = [location[0] - 1, location[1]]

    elif direction == 2:
        desired_location = [location[0] + 1, location[1]]

    elif direction == 3:
        desired_location = [location[0], location[1] - 1]

    elif direction == 4:
        desired_location = [location[0], location[1] + 1]

    new_puzzle_state = swap_values(puzzle_state, location, desired_location)

    target = check_puzzle_state(new_puzzle_state, target_state)
    return new_puzzle_state, target


def get_available_movements(location):
    global N
    n = N - 1

    # available_movements = [0, 0, 0, 0] --> no movements allowed
    # available_movements = [1, 0, 0, 0] --> left movement allowed
    # available_movements = [0, 1, 0, 0] --> right movement allowed
    # available_movements = [0, 0, 1, 0] --> upward movement allowed
    # available_movements = [0, 0, 0, 1] --> down movement allowed
    # available_movements = [1, 1, 1, 1] --> all movements allowed

    x = location[0]
    y = location[1]

    # CORNERS MOVEMENTS ALLOWED
    if x == 0 and y == 0:
        available_movements = [0, 1, 0, 1]  # right & down
    elif x == 0 and y == n:
        available_movements = [0, 1, 1, 0]  # right & up
    elif x == n and y == 0:
        available_movements = [1, 0, 0, 1]  # left & down
    elif x == n and y == n:
        available_movements = [1, 0, 1, 0]  # left & up

    # BORDERS MOVEMENTS ALLOWED
    elif x == 0:
        available_movements = [0, 1, 1, 1]  # right, up & down
    elif x == n:
        available_movements = [1, 0, 1, 1]  # left, up & down
    elif y == 0:
        available_movements = [1, 1, 0, 1]  # right, left & down
    elif y == n:
        available_movements = [1, 1, 1, 0]  # right, left & up

    # ANYWHERE ELSE MOVEMENTS ALLOWED
    else:
        available_movements = [1, 1, 1, 1]  # left, right, up & down

    return available_movements


def search_blank_space(puzzle_state):
    inverted_location = np.where(puzzle_state == 0)
    location = [inverted_location[1], inverted_location[0]]

    return location


def create_puzzle_from_array(array):
    global N

    matrix = np.reshape(array, (N, N))

    return matrix


def create_target_puzzle_array():
    tiles_number = N * N
    target_puzzle_numbers = []

    for i in range(1, tiles_number):
        target_puzzle_numbers.append(i)

    target_puzzle_numbers.append(0)
    return target_puzzle_numbers


def print_puzzle(puzzle_state):
    global N

    for x in range(N):
        row = ""

        for y in range(N):
            temp_row = row
            number = puzzle_state[x][y]
            formatted_number = ""

            if len(str(number)) == 1:
                formatted_number = "  " + str(number)
            elif len(str(number)) == 2:
                formatted_number = " " + str(number)
            elif len(str(number)) == 3:
                formatted_number = str(number)

            row = temp_row + formatted_number + " "

        print(row)

    print("")


def uninformed_8puzzle():
    global target_state, solution_node, steps_made

    print("\n**** SOLVING PUZZLE WITH DEPTH LIMITED SEARCH *****")
    initial_state, already_solved = init_puzzle()
    if already_solved == 0:
        new_node = SearchNode(initial_state, 0, 1, None, [], 0)
        new_node.expand_possible_movements_dls()

        if solution_node is not None:
            current_node = solution_node
            states_list = []

            while current_node.parent is not None:
                states_list.append(current_node.puzzle_state)
                current_node = current_node.parent

            states_list.append(current_node.puzzle_state)

            for i in range(1, len(states_list)):
                backward_position = len(states_list) - i - 1
                print("--- STEP #" + str(i) + " ---")
                print_puzzle(states_list[backward_position])
        else:
            print("Puzzle wasn't possible to solve with " + str(max_depth) + " movements")

    else:
        print("Puzzle is already solved")


def informed_n_puzzle():
    global target_state, solution_node, steps_made

    print("\n**** SOLVING PUZZLE WITH A* ALGORITHM SEARCH *****")
    initial_state, already_solved = init_puzzle()
    if already_solved == 0:
        manhattan_distance = get_manhattan_distance(initial_state, target_state)
        new_node = SearchNode(initial_state, manhattan_distance, 0, None, [], 0)
        new_node.expand_possible_movements_gbfs()

    else:
        print("Puzzle is already solved")


def init_puzzle():
    global target_state, solution_node, steps_made

    initial_state = create_puzzle_from_array(initial_state_array)

    target_state_array = create_target_puzzle_array()
    target_state = create_puzzle_from_array(target_state_array)

    print("\n --- INITIAL STATE ---")
    print_puzzle(initial_state)

    already_solved = check_puzzle_state(initial_state, target_state)
    return initial_state, already_solved


start_time = time()

# uninformed_8puzzle()
informed_n_puzzle()

finish_time = time()
execution_duration = finish_time - start_time
print("Puzzle Solution Search took: " + str(execution_duration * 1000) + " milliseconds")
