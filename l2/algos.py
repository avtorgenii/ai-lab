import copy
import time
import random


def minimax(game, heuristic_id, depth, maximizing_player,
            suboptimal_chance=0.0, is_root_call=True, visited_nodes=0):
    start_time = time.time()
    current_total_visited = visited_nodes + 1

    player = 'B' if maximizing_player else 'W'
    possible_moves = game.get_all_valid_moves(player)

    # Suboptimal random choice logic, only for the root call of an AI's turn
    if is_root_call and suboptimal_chance > 0 and random.random() < suboptimal_chance:
        if possible_moves:
            chosen_move = random.choice(possible_moves)
            # Evaluate the state after this random move for logging/consistency
            game_copy_suboptimal = copy.deepcopy(game)
            game_copy_suboptimal.make_move(chosen_move[0][0], chosen_move[0][1], chosen_move[1][0], chosen_move[1][1])
            eval_for_suboptimal = game_copy_suboptimal.evaluate(heuristic_id)

            return eval_for_suboptimal, chosen_move, 1, time.time() - start_time, True

    if depth == 0 or not possible_moves:
        return game.evaluate(
            heuristic_id), None, current_total_visited, time.time() - start_time, False

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move[0][0], move[0][1], move[1][0], move[1][1])

            eval_child, _, nodes_from_child_subtree, _, _ = minimax(
                game_copy, heuristic_id, depth - 1, False,
                0.0, False, 0
            )
            current_total_visited += nodes_from_child_subtree
            if eval_child > max_eval:
                max_eval = eval_child
                best_move = move
        return max_eval, best_move, current_total_visited, time.time() - start_time, False
    else:
        min_eval = float('inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move[0][0], move[0][1], move[1][0], move[1][1])
            eval_child, _, nodes_from_child_subtree, _, _ = minimax(
                game_copy, heuristic_id, depth - 1, True,
                0.0, False, 0
            )
            current_total_visited += nodes_from_child_subtree
            if eval_child < min_eval:
                min_eval = eval_child
                best_move = move
        return min_eval, best_move, current_total_visited, time.time() - start_time, False


def alpha_beta(game, heuristic_id, depth, maximizing_player, alpha=float('-inf'), beta=float('inf'),
               suboptimal_chance=0.0, is_root_call=True, visited_nodes_accumulator=0):
    start_time = time.time()
    current_total_visited = visited_nodes_accumulator + 1

    player = 'B' if maximizing_player else 'W'
    possible_moves = game.get_all_valid_moves(player)

    # Suboptimal random choice logic, only for the root call of an AI's turn
    if is_root_call and suboptimal_chance > 0 and random.random() < suboptimal_chance:
        if possible_moves:
            chosen_move = random.choice(possible_moves)
            game_copy_suboptimal = copy.deepcopy(game)
            game_copy_suboptimal.make_move(chosen_move[0][0], chosen_move[0][1], chosen_move[1][0], chosen_move[1][1])
            eval_for_suboptimal = game_copy_suboptimal.evaluate(heuristic_id)
            return eval_for_suboptimal, chosen_move, 1, time.time() - start_time, True

    if depth == 0 or not possible_moves:
        return game.evaluate(
            heuristic_id), None, current_total_visited, time.time() - start_time, False

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move[0][0], move[0][1], move[1][0], move[1][1])
            eval_child, _, nodes_from_child_subtree, _, _ = alpha_beta(
                game_copy, heuristic_id, depth - 1, False, alpha, beta,
                0.0, False, 0
            )
            current_total_visited += nodes_from_child_subtree
            if eval_child > max_eval:
                max_eval = eval_child
                best_move = move
            alpha = max(alpha, eval_child)
            if beta <= alpha:
                break
        return max_eval, best_move, current_total_visited, time.time() - start_time, False
    else:
        min_eval = float('inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(move[0][0], move[0][1], move[1][0], move[1][1])
            eval_child, _, nodes_from_child_subtree, _, _ = alpha_beta(
                game_copy, heuristic_id, depth - 1, True, alpha, beta,
                0.0, False, 0
            )
            current_total_visited += nodes_from_child_subtree
            if eval_child < min_eval:
                min_eval = eval_child
                best_move = move
            beta = min(beta, eval_child)
            if beta <= alpha:
                break
        return min_eval, best_move, current_total_visited, time.time() - start_time, False
