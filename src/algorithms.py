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