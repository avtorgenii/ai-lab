from l2.algos import minimax, alpha_beta
from l2.clobber import Clobber

if __name__ == "__main__":
    game = Clobber(6, 10)
    game.print_board()

    heuristic_id = 1
    depth = 3
    maximizing_player = True
    eval, best_move, visited_nodes, time_taken = minimax(game, heuristic_id, depth, maximizing_player)
    print(f"Minimax: Best move: {best_move}, Evaluation: {eval}, Visited Nodes: {visited_nodes}, Time: {time_taken}")

    if best_move:
        game.make_move(best_move[0][0], best_move[0][1], best_move[1][0], best_move[1][1])
        game.print_board()

    # Example usage of alpha-beta:
    game = Clobber(6, 10)
    heuristic_id = 1
    depth = 3
    maximizing_player = True
    alpha = float('-inf')
    beta = float('inf')
    eval, best_move, visited_nodes, time_taken = alpha_beta(game, heuristic_id, depth, maximizing_player, alpha, beta)
    print(f"Alpha-Beta: Best move: {best_move}, Evaluation: {eval}, Visited Nodes: {visited_nodes}, Time: {time_taken}")

    if best_move:
        game.make_move(best_move[0][0], best_move[0][1], best_move[1][0], best_move[1][1])
        game.print_board()