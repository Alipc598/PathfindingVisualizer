import numpy as np
import time

def heuristic(a, b):
    return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])

def get_neighbors(node, grid):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    neighbors = []
    x, y = node
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[ny][nx] == 0:  
                neighbors.append((nx, ny))
    return neighbors


def astar(start, goal, grid):
    start_time = time.perf_counter()
    #print(f"Start time: {start_time}")  # Debugging print
    nodes_explored = 0

    open_set = set([start])
    closed_set = set()

    came_from = {}

    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        if current == goal:
            path = []
            while current != start:  
                path.append(current)
                current = came_from[current]
            path.append(start)  
            path.reverse()  
            end_time = time.perf_counter()
            #print(f"End time: {end_time}")  # Debugging print
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time


        open_set.remove(current)
        closed_set.add(current)
        nodes_explored += 1

        for neighbor in get_neighbors(current, grid):  
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

    end_time = time.time()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time


def branch_and_bound(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = 0

    queue = [(start, [start])]
    visited = set()

    while queue:
        (vertex, path) = queue.pop(0)
        if vertex in visited:
            continue
        visited.add(vertex)
        nodes_explored += 1

        if vertex == goal:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        for next_node in get_neighbors(vertex, grid): 
            if next_node not in visited:
                new_path = list(path)
                new_path.append(next_node)
                queue.append((next_node, new_path))

    end_time = time.time()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time

def dijkstra(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = 0

    open_set = set([start])
    closed_set = set()

    came_from = {}

    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0

    while open_set:
        current = min(open_set, key=lambda x: g_score[x])
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored += 1

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time

def greedy_best_first_search(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = 0

    open_set = set([start])
    closed_set = set()

    came_from = {}

    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        open_set.remove(current)
        closed_set.add(current)
        nodes_explored += 1

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue

            if neighbor not in open_set:
                open_set.add(neighbor)
                came_from[neighbor] = current
                f_score[neighbor] = heuristic(neighbor, goal)

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
            return path, len(closed_set), execution_time

        open_set.remove(current)
        closed_set.add(current)

        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            jump_point = get_jump_point(current, neighbor, grid)
            if not jump_point or jump_point in closed_set:
                continue

            tentative_g_score = g_score[current] + heuristic(current, jump_point)
            if jump_point not in open_set:
                open_set.add(jump_point)
            elif tentative_g_score >= g_score.get(jump_point, float('inf')):
                continue

            came_from[jump_point] = current
            g_score[jump_point] = tentative_g_score
            f_score[jump_point] = g_score[jump_point] + heuristic(jump_point, goal)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return [], len(closed_set), execution_time

# Example usage:
# path, nodes_explored, execution_time = jump_point_search(start, goal, grid)
