import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import heapq
import random
from math import ceil

myID, game_map = hlt.get_init()
hlt.send_init("Axente Server Bot v1.0")

# Helper functions
def reset_visited_mat(visited):
    for i in range(len(visited)):
        for j in range(len(visited[0])):
            visited[i][j] = False

def check_is_frontier(square):
    check_owner = square.owner != myID
    check_neighbors = False

    for direction in [NORTH, SOUTH, WEST, EAST]:
        neighbor = game_map.get_target(square, direction)
        if neighbor.owner == myID:
            check_neighbors = True
            break

    return check_owner and check_neighbors

def check_close_to_frontier(square):
    return any(game_map.get_target(square, direction).owner != myID for direction in [NORTH, SOUTH, WEST, EAST])

def get_score(square):
    if square.owner == myID:
        return -1

    production_score = square.production
    strength_penalty = square.strength / max(1, square.production)

    proximity_bonus = 0
    neutral_bonus = 0
    enemy_bonus = 0
    for neighbor, _ in get_neighbors(square):
        if neighbor.owner == 0:
            neutral_bonus += 2
        elif neighbor.owner != myID:
            enemy_bonus += 3

    proximity_bonus = neutral_bonus + enemy_bonus

    border_proximity_bonus = 0
    if any(neighbor.owner != myID for neighbor, _ in get_neighbors(square)):
        border_proximity_bonus += 5

    score = (production_score * 5) - (strength_penalty * 3) + (proximity_bonus * 3) + border_proximity_bonus

    return score

def strength_after_steps(square, steps):
    return square.strength + steps * square.production

def get_neighbors(square):
    directions = [NORTH, SOUTH, WEST, EAST]
    return [(game_map.get_target(square, direction), direction) for direction in directions]

# Manhattan distance
def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def a_star_search(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                current, direction = came_from[current]
                path.append((current, direction))
            path.reverse()
            return path

        for neighbor, direction in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = (current, direction)
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def find_goal_square(square):
    neighbors = get_neighbors(square)
    for neighbor, _ in neighbors:
        if neighbor.owner != myID:
            return neighbor
    return None

def find_closest_frontier(square):
    directions = [NORTH, SOUTH, WEST, EAST]
    moves = [(square, d) for d in directions]
    distances = [0, 0, 0, 0]
    margins = [game_map.height // 2, game_map.width // 2]

    for i in range(4):
        while moves[i][0].owner == myID and distances[i] < margins[i // 2]:
            moves[i] = (game_map.get_target(moves[i][0], moves[i][1]), moves[i][1])
            distances[i] += 1

    distances_to_enemies = [0, 0, 0, 0]
    max_difference = 8

    for i in range(4):
        if distances[i] != margins[i // 2]:
            if moves[i][0].owner == 0:
                while distances_to_enemies[i] < max_difference and moves[i][0].owner == 0:
                    moves[i] = (game_map.get_target(moves[i][0], moves[i][1]), moves[i][1])
                    distances_to_enemies[i] += 1
        else:
            distances_to_enemies[i] = max_difference

    min_distance = distances[0] + distances_to_enemies[0]
    min_index = 0
    for i in range(1, 4):
        if min_distance > distances[i] + distances_to_enemies[i]:
            min_distance = distances[i] + distances_to_enemies[i]
            min_index = i

    return moves[min_index][1]

def get_neigh_and_op_dir(square, steps):
    directions = [(NORTH, SOUTH), (SOUTH, NORTH), (WEST, EAST), (EAST, WEST)]

    locs = []
    for direction, opposite in directions:
        neighbor_square = game_map.get_target(square, direction)
        if (
            neighbor_square and
            0 <= neighbor_square.x < game_map.width and
            0 <= neighbor_square.y < game_map.height and
            neighbor_square.owner == myID and
            not visited[neighbor_square.x][neighbor_square.y]
        ):
            locs.append((neighbor_square, opposite))

    if not locs:
        return locs
    
    locs.sort(key=lambda x: strength_after_steps(x[0], steps), reverse=True)
    return locs

def find_moves_for_two_strongest_neighbors(locs, biggest, square, steps):
    moves = []
    last = len(locs) - 1
    while last > 0:
        if strength_after_steps(biggest[0], steps) + strength_after_steps(locs[last][0], steps) > square.strength:
            if steps != 0:
                moves.append(Move(biggest[0], STILL))
            else:
                moves.append(Move(biggest[0], biggest[1]))
            moves.append(Move(locs[last][0], locs[last][1]))
            break
        last -= 1
    return moves

def find_moves_for_three_strongest_neighbors(locs, biggest, square, steps):
    moves = []
    last = len(locs) - 1
    while last > 1:
        if (strength_after_steps(biggest[0], steps) +
            strength_after_steps(locs[1][0], steps) +
            strength_after_steps(locs[last][0], steps)) > square.strength:
            if steps != 0:
                moves.append(Move(biggest[0], STILL))
            else:
                moves.append(Move(biggest[0], biggest[1]))
            moves.append(Move(locs[1][0], locs[1][1]))
            moves.append(Move(locs[last][0], locs[last][1]))
            break
        last -= 1
    return moves

def check_if_move_is_possible(square, steps):
    moves = []
    locs = get_neigh_and_op_dir(square, steps)
    if not locs:
        return moves

    biggest = locs[0]
    if strength_after_steps(biggest[0], steps) > square.strength:
        if steps != 0:
            moves.append(Move(biggest[0], STILL))
        else:
            moves.append(Move(biggest[0], biggest[1]))
    else:
        moves = find_moves_for_two_strongest_neighbors(locs, biggest, square, steps)
        if not moves:
            moves = find_moves_for_three_strongest_neighbors(locs, biggest, square, steps)

    for move in moves:
        visited[move.square.x][move.square.y] = True
    return moves

# Main loop
while True:
    moves = []
    game_map.get_frame()
    max_size = ceil(max(game_map.width, game_map.height) * 1.1)
    visited = [[False for _ in range(max_size)] for _ in range(max_size)]
    reset_visited_mat(visited)

    scores = []
    for square in game_map:
        if check_is_frontier(square):
            scores.append(square)
    scores.sort(key=get_score, reverse=True)

    while scores:
        loc = scores.pop(0)
        moves_for_edge = check_if_move_is_possible(loc, 0)
        if not moves_for_edge:
            moves_for_edge = check_if_move_is_possible(loc, 1)
        if moves_for_edge:
            moves.extend(moves_for_edge)
        else:
            best_moves = get_neigh_and_op_dir(loc, 1)
            if not best_moves:
                continue
            best_move = best_moves[0]
            best_neighbours = get_neigh_and_op_dir(best_move[0], 0)
            if not best_neighbours:
                continue
            best_neighbour = best_neighbours[0]
            if strength_after_steps(best_move[0], 1) + best_neighbour[0].strength > loc.strength:
                moves.append(Move(best_move[0], STILL))
                moves.append(Move(best_neighbour[0], best_neighbour[1]))
                visited[best_move[0].x][best_move[0].y] = True
                visited[best_neighbour[0].x][best_neighbour[0].y] = True

    for square in game_map:
        if square.owner == myID:
            if check_close_to_frontier(square):
                if not visited[square.x][square.y]:
                    moves.append(Move(square, STILL))
            else:
                if square.strength >= 5 * square.production:
                    goal_square = find_goal_square(square)
                    if goal_square:
                        path = a_star_search(square, goal_square)
                        if path:
                            moves.append(Move(square, path[0][1]))
                        else:
                            moves.append(Move(square, STILL))
                    else:
                        moves.append(Move(square, find_closest_frontier(square)))
                else:
                    moves.append(Move(square, STILL))
            visited[square.x][square.y] = True

    hlt.send_frame(moves)
