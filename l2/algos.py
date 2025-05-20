import copy
import time


def minimax(game, heuristic_id, depth, maximizing_player, visited_nodes=0):
    start_time = time.time()
    visited_nodes += 1
    player = 'B' if maximizing_player else 'W'
    possible_moves = game.get_all_valid_moves(player)

    if depth == 0 or not possible_moves:
        return game.evaluate(heuristic_id), None, visited_nodes, time.time() - start_time

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move[0][0], move[0][1], move[1][0], move[1][1])
            eval, _, nodes, _ = minimax(game_copy, heuristic_id, depth - 1, False, visited_nodes)
            visited_nodes += nodes
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move, visited_nodes, time.time() - start_time

    else:
        min_eval = float('inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move[0][0], move[0][1], move[1][0], move[1][1])
            eval, _, nodes, _ = minimax(game_copy, heuristic_id, depth - 1, True, visited_nodes)
            visited_nodes += nodes
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move, visited_nodes, time.time() - start_time



def alpha_beta(game, heuristic_id, depth, maximizing_player, alpha=float('-inf'), beta=float('inf'), visited_nodes=0):
    start_time = time.time()
    visited_nodes += 1
    player = 'B' if maximizing_player else 'W'
    possible_moves = game.get_all_valid_moves(player)

    if depth == 0 or not possible_moves:
        return game.evaluate(heuristic_id), None, visited_nodes, time.time() - start_time

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move[0][0], move[0][1], move[1][0], move[1][1])
            eval, _, nodes, _ = alpha_beta(game_copy, heuristic_id, depth - 1, False, alpha, beta, visited_nodes)
            visited_nodes += nodes
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move, visited_nodes, time.time() - start_time

    else:
        min_eval = float('inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move[0][0], move[0][1], move[1][0], move[1][1])
            eval, _, nodes, _ = alpha_beta(game_copy, heuristic_id, depth - 1, True, alpha, beta, visited_nodes)
            visited_nodes += nodes
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move, visited_nodes, time.time() - start_time

