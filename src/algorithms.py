import numpy as np
import time

def heuristic(a, b):
    return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])

def line_of_sight(grid, start, end):
    """Check if there's a direct line of sight between start and end"""
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while (x0, y0) != (x1, y1):
        if grid[y0][x0] == 1:
            return False
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return grid[y1][x1] == 0

def get_neighbors(node, grid):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    neighbors = []
    x, y = node
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[ny][nx] == 0:
            neighbors.append((nx, ny))
    return neighbors

def get_neighbors_no_diagonals(node, grid):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Only horizontal and vertical movements
    neighbors = []
    x, y = node
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[ny][nx] == 0:
            neighbors.append((nx, ny))
    return neighbors


def astar(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()

    open_set = set([start])
    closed_set = set()

    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda o: f_score[o])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored.add(current)

        print("\n" + "="*40)
        print(f"Current node: {current}")
        print("="*40)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)
                added_to_open_set = "Yes"
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue
            else:
                added_to_open_set = "No"

            # User-friendly debug prints to understand the decision-making process
            print("-" * 40)
            print(f"Evaluating neighbor: {neighbor}")
            print(f"tentative_g_score: {tentative_g_score}")
            print(f"current g_score of neighbor: {g_score.get(neighbor, float('inf'))}")
            print(f"Added to open set: {added_to_open_set}")

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

            print(f"Updated g_score: {g_score[neighbor]}")
            print(f"Updated f_score: {f_score[neighbor]}")
            print("-" * 40)

        print("Current open set: ", open_set)
        print("Current closed set: ", closed_set)
        print("="*40 + "\n")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time

def branch_and_bound(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()

    queue = [(start, [start])]
    visited = set()

    while queue:
        vertex, path = queue.pop(0)

        print("\n" + "="*40)
        print(f"Current node: {vertex}")
        print(f"Current path: {path}")
        print("="*40)

        if vertex in visited:
            print(f"Node {vertex} already visited, skipping...")
            continue
        visited.add(vertex)
        nodes_explored.add(vertex)

        if vertex == goal:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print("\n----------------------------")
            print("Goal Reached!")
            print(f"Final Path: {path}")
            print(f"Total nodes explored: {len(nodes_explored)}")
            print(f"Execution time: {execution_time:.10f} seconds")
            print("----------------------------")
            return path, nodes_explored, execution_time

        for next_node in get_neighbors(vertex, grid):
            if next_node not in visited:
                new_path = list(path)
                new_path.append(next_node)
                queue.append((next_node, new_path))
                
                # User-friendly debug prints to understand the decision-making process
                print("-" * 40)
                print(f"Evaluating neighbor: {next_node}")
                print(f"Updated path: {new_path}")
                print("-" * 40)

        print("Current queue: ", queue)
        print("Current visited set: ", visited)
        print("="*40 + "\n")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("\n----------------------------")
    print("No Path Found")
    print(f"Total nodes explored: {len(nodes_explored)}")
    print(f"Execution time: {execution_time:.10f} seconds")
    print("----------------------------")
    return [], nodes_explored, execution_time

def dijkstra(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()

    open_set = set([start])
    closed_set = set()

    came_from = {}

    g_score = {start: 0}

    while open_set:
        current = min(open_set, key=lambda o: g_score[o])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored.add(current)

        print("\n" + "="*40)
        print(f"Current node: {current}")
        print("="*40)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)
                added_to_open_set = "Yes"
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue
            else:
                added_to_open_set = "No"

            print("-" * 40)
            print(f"Evaluating neighbor: {neighbor}")
            print(f"tentative_g_score: {tentative_g_score}")
            print(f"current g_score of neighbor: {g_score.get(neighbor, float('inf'))}")
            print(f"Added to open set: {added_to_open_set}")

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score

            print(f"Updated g_score: {g_score[neighbor]}")
            print("-" * 40)

        print("Current open set: ", open_set)
        print("Current closed set: ", closed_set)
        print("="*40 + "\n")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time


def greedy_best_first_search(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()

    open_set = set([start])
    closed_set = set()

    came_from = {}

    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda o: f_score[o])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored.add(current)

        print("\n" + "="*40)
        print(f"Current node: {current}")
        print("="*40)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue

            if neighbor not in open_set:
                open_set.add(neighbor)
                added_to_open_set = "Yes"
            else:
                added_to_open_set = "No"

            print("-" * 40)
            print(f"Evaluating neighbor: {neighbor}")
            print(f"Added to open set: {added_to_open_set}")

            came_from[neighbor] = current
            f_score[neighbor] = heuristic(neighbor, goal)

            print(f"Updated f_score: {f_score[neighbor]}")
            print("-" * 40)

        print("Current open set: ", open_set)
        print("Current closed set: ", closed_set)
        print("="*40 + "\n")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time

def hierarchical_pathfinding(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()

    open_set = set([start])
    closed_set = set()

    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda o: f_score[o])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored.add(current)

        print("\n" + "="*40)
        print(f"Current node: {current}")
        print("="*40)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue

            if current in came_from and line_of_sight(grid, came_from[current], neighbor):
                tentative_g_score = g_score[came_from[current]] + heuristic(came_from[current], neighbor)
            else:
                tentative_g_score = g_score[current] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)
                added_to_open_set = "Yes"
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue
            else:
                added_to_open_set = "No"

            # User-friendly debug prints to understand the decision-making process
            print("-" * 40)
            print(f"Evaluating neighbor: {neighbor}")
            print(f"tentative_g_score: {tentative_g_score}")
            print(f"current g_score of neighbor: {g_score.get(neighbor, float('inf'))}")
            print(f"Added to open set: {added_to_open_set}")

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

            print(f"Updated g_score: {g_score[neighbor]}")
            print(f"Updated f_score: {f_score[neighbor]}")
            print("-" * 40)

        print("Current open set: ", open_set)
        print("Current closed set: ", closed_set)
        print("="*40 + "\n")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time


def jump_point_search(start, goal, grid):
    def get_jump_point(parent, node, grid):
        x, y = node
        px, py = parent
        dx, dy = x - px, y - py

        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])) or grid[y][x] == 1:
            return None

        if node == goal:
            return node

        # Check for forced neighbors
        if dx != 0 and dy != 0:  # Diagonal movement
            if (grid[y][x - dx] == 1 and grid[y - dy][x] == 0) or (grid[y - dy][x] == 1 and grid[y][x - dx] == 0):
                return node
        elif dx != 0:  # Horizontal movement
            if (0 <= y + 1 < len(grid) and grid[y + 1][x] == 0 and grid[y + 1][x - dx] == 1) or (0 <= y - 1 < len(grid) and grid[y - 1][x] == 0 and grid[y - 1][x - dx] == 1):
                return node
        elif dy != 0:  # Vertical movement
            if (0 <= x + 1 < len(grid[0]) and grid[y][x + 1] == 0 and grid[y - dy][x + 1] == 1) or (0 <= x - 1 < len(grid[0]) and grid[y][x - 1] == 0 and grid[y - dy][x - 1] == 1):
                return node

        # Check for jump points recursively
        if dx != 0 and dy != 0:  # Diagonal
            if get_jump_point(node, (x + dx, y), grid) or get_jump_point(node, (x, y + dy), grid):
                return node
        if dx != 0:  # Horizontal
            return get_jump_point(node, (x + dx, y), grid)
        if dy != 0:  # Vertical
            return get_jump_point(node, (x, y + dy), grid)

        return None

    start_time = time.perf_counter()
    open_set = set([start])
    closed_set = set()
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    print("\nStarting Jump Point Search Algorithm")
    print("Initial Open Set: ", open_set)
    
    while open_set:
        current = min(open_set, key=lambda o: f_score[o])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print("\n----------------------------")
            print("Goal Reached!")
            print(f"Final Path: {path}")
            print("----------------------------")
            return path, closed_set, execution_time

        open_set.remove(current)
        closed_set.add(current)

        print("\n" + "="*40)
        print(f"Current node: {current}")
        print("="*40)

        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            jump_point = get_jump_point(current, neighbor, grid)
            if not jump_point or jump_point in closed_set:
                continue

            tentative_g_score = g_score[current] + heuristic(current, jump_point)
            if jump_point not in open_set:
                open_set.add(jump_point)
                added_to_open_set = "Yes"
            else:
                added_to_open_set = "No"
            
            print("-" * 40)
            print(f"Evaluating jump point: {jump_point}")
            print(f"tentative_g_score: {tentative_g_score}")
            print(f"current g_score of jump point: {g_score.get(jump_point, float('inf'))}")
            print(f"Added to open set: {added_to_open_set}")

            came_from[jump_point] = current
            g_score[jump_point] = tentative_g_score
            f_score[jump_point] = g_score[jump_point] + heuristic(jump_point, goal)

            print(f"Updated g_score: {g_score[jump_point]}")
            print(f"Updated f_score: {f_score[jump_point]}")
            print("-" * 40)

        print("Current open set: ", open_set)
        print("Current closed set: ", closed_set)
        print("="*40 + "\n")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("\n----------------------------")
    print("No Path Found")
    print("----------------------------")
    return [], closed_set, execution_time

def dynamic_astar(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()

    open_set = set([start])
    closed_set = set()

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    def update_grid_with_changes(grid, changes):
        for change in changes:
            x, y, new_value = change
            grid[y][x] = new_value

    while open_set:
        current = min(open_set, key=lambda o: f_score[o])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored.add(current)

        print("\n" + "="*40)
        print(f"Current node: {current}")
        print("="*40)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)
                added_to_open_set = "Yes"
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue
            else:
                added_to_open_set = "No"

            # User-friendly debug prints to understand the decision-making process
            print("-" * 40)
            print(f"Evaluating neighbor: {neighbor}")
            print(f"tentative_g_score: {tentative_g_score}")
            print(f"current g_score of neighbor: {g_score.get(neighbor, float('inf'))}")
            print(f"Added to open set: {added_to_open_set}")

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

            print(f"Updated g_score: {g_score[neighbor]}")
            print(f"Updated f_score: {f_score[neighbor]}")
            print("-" * 40)

        print("Current open set: ", open_set)
        print("Current closed set: ", closed_set)
        print("="*40 + "\n")

        # Simulate grid changes
        grid_changes = []
        if grid_changes:
            print("Updating grid with changes...")
            update_grid_with_changes(grid, grid_changes)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time

def theta_star(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()

    open_set = set([start])
    closed_set = set()

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda o: f_score[o])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored.add(current)

        print("\n" + "="*40)
        print(f"Current node: {current}")
        print("="*40)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue

            if (current in came_from and line_of_sight(grid, came_from[current], neighbor)):
                tentative_g_score = g_score[came_from[current]] + heuristic(came_from[current], neighbor)
            else:
                tentative_g_score = g_score[current] + heuristic(current, neighbor)

            if neighbor not in open_set:
                open_set.add(neighbor)
                added_to_open_set = "Yes"
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue
            else:
                added_to_open_set = "No"

            # User-friendly debug prints to understand the decision-making process
            print("-" * 40)
            print(f"Evaluating neighbor: {neighbor}")
            print(f"tentative_g_score: {tentative_g_score}")
            print(f"current g_score of neighbor: {g_score.get(neighbor, float('inf'))}")
            print(f"Added to open set: {added_to_open_set}")

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

            print(f"Updated g_score: {g_score[neighbor]}")
            print(f"Updated f_score: {f_score[neighbor]}")
            print("-" * 40)

        print("Current open set: ", open_set)
        print("Current closed set: ", closed_set)
        print("="*40 + "\n")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time

def bfs(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()
    queue = [(start, [start])]
    visited = set()

    print("\nStarting Breadth-First Search Algorithm")
    print(f"Start node: {start}, Goal node: {goal}")
    print("Initial Queue: ", queue)
    
    while queue:
        (vertex, path) = queue.pop(0)
        if vertex in visited:
            continue
        visited.add(vertex)
        nodes_explored.add(vertex)

        print("\n" + "="*40)
        print(f"Current node: {vertex}")
        print(f"Current path: {path}")
        print("="*40)

        if vertex == goal:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print("\n" + "="*40)
            print("Goal Reached!")
            print(f"Final Path: {path}")
            print(f"Nodes explored: {len(nodes_explored)}")
            print(f"Execution time: {execution_time:.10f} seconds")
            print("="*40)
            return path, nodes_explored, execution_time

        for next_node in get_neighbors_no_diagonals(vertex, grid):
            if next_node not in visited:
                new_path = list(path)
                new_path.append(next_node)
                queue.append((next_node, new_path))
                print("-" * 40)
                print(f"Evaluating neighbor: {next_node}")
                print(f"New path: {new_path}")
                print(f"Queue: {queue}")
                print("-" * 40)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("\n" + "="*40)
    print("No Path Found")
    print("="*40)
    return [], nodes_explored, execution_time

def dfs(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()
    stack = [(start, [start])]
    visited = set()

    print("\nStarting Depth-First Search Algorithm")
    print(f"Start node: {start}, Goal node: {goal}")
    print("Initial Stack: ", stack)
    
    while stack:
        (vertex, path) = stack.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        nodes_explored.add(vertex)

        print("\n" + "="*40)
        print(f"Current node: {vertex}")
        print(f"Current path: {path}")
        print("="*40)

        if vertex == goal:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print("\n" + "="*40)
            print("Goal Reached!")
            print(f"Final Path: {path}")
            print(f"Nodes explored: {len(nodes_explored)}")
            print(f"Execution time: {execution_time:.10f} seconds")
            print("="*40)
            return path, nodes_explored, execution_time

        for next_node in get_neighbors_no_diagonals(vertex, grid):
            if next_node not in visited:
                new_path = list(path)
                new_path.append(next_node)
                stack.append((next_node, new_path))
                print("-" * 40)
                print(f"Evaluating neighbor: {next_node}")
                print(f"New path: {new_path}")
                print(f"Stack: {stack}")
                print("-" * 40)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("\n" + "="*40)
    print("No Path Found")
    print("="*40)
    return [], nodes_explored, execution_time

def swarm_algorithm(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = set()

    open_set = set([start])
    closed_set = set()

    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda o: f_score[o])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored.add(current)

        print("\n" + "="*40)
        print(f"Current node: {current}")
        print("="*40)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)
                added_to_open_set = "Yes"
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue
            else:
                added_to_open_set = "No"

            # User-friendly debug prints to understand the decision-making process
            print("-" * 40)
            print(f"Evaluating neighbor: {neighbor}")
            print(f"tentative_g_score: {tentative_g_score}")
            print(f"current g_score of neighbor: {g_score.get(neighbor, float('inf'))}")
            print(f"Added to open set: {added_to_open_set}")

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

            print(f"Updated g_score: {g_score[neighbor]}")
            print(f"Updated f_score: {f_score[neighbor]}")
            print("-" * 40)

        print("Current open set: ", open_set)
        print("Current closed set: ", closed_set)
        print("="*40 + "\n")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time