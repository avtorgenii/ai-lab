from l2.algos import minimax, alpha_beta
from l2.clobber import Clobber


def game_loop(rows, cols, heuristic_id, depth, alpha_beta_algo=False):
    game = Clobber(rows, cols)
    game.print_board()

    moves = 0

    maximizing_player = True
    while not game.is_over("B" if maximizing_player else "W"):
        if not alpha_beta_algo:
            eval, best_move, visited_nodes, time_taken = minimax(game, heuristic_id, depth, maximizing_player)
        else:
            eval, best_move, visited_nodes, time_taken = alpha_beta(game, heuristic_id, depth, maximizing_player)
        print(
            f"Minimax: Best move: {best_move}, Evaluation: {eval}, Visited Nodes: {visited_nodes}, Time: {time_taken:.2f}s")

        if best_move:
            maximizing_player = not maximizing_player  # flip player
            game.make_move(best_move[0][0], best_move[0][1], best_move[1][0], best_move[1][1])
            moves += 1
            game.print_board()

            valid_move = False
            start_row, start_col, end_row, end_col = None, None, None, None
            while not valid_move:
                start_row, start_col = input(
                    "Enter row and col of tile you want to move. Split them with coma.: \n").split(",")
                start_row, start_col = int(start_row), int(start_col)

                if game.is_players_tile(start_row, start_col, "B" if maximizing_player else "W"):
                    end_row, end_col = input(
                        "Enter row and col of tile to which you want to move. Split them with coma.: \n").split(",")
                    end_row, end_col = int(end_row), int(end_col)

                    valid_moves = game.get_valid_moves_for_tile(start_row, start_col)

                    if (end_row, end_col) in valid_moves:
                        valid_move = True

            game.make_move(start_row, start_col, end_row, end_col)
            moves += 1
            game.print_board()
            maximizing_player = not maximizing_player  # flip player again
        else:
            break

    if maximizing_player:
        print(f"You Won! Total rounds: {moves // 2 + 1}")
    else:
        print(f"Minimax Won! Total rounds: {moves // 2 + 1}")


def ai_game_loop(rows, cols, ai1_params, ai2_params):
    """
    Plays a game of Clobber between two AI agents.
    AI1 is configured by ai1_params and plays as 'B' (Black).
    AI2 is configured by ai2_params and plays as 'W' (White).

    Args:
        rows (int): Number of rows on the board.
        cols (int): Number of columns on the board.
        ai1_params (dict): Parameters for AI 1 (plays as 'B').
                           Expected keys: 'heuristic_id' (int),
                                          'depth' (int),
                                          'alpha_beta_algo' (bool),
                                          'suboptimal_chance' (float, optional, 0.0 to 1.0).
        ai2_params (dict): Parameters for AI 2 (plays as 'W').
                           Expected keys: 'heuristic_id' (int),
                                          'depth' (int),
                                          'alpha_beta_algo' (bool),
                                          'suboptimal_chance' (float, optional, 0.0 to 1.0).
    """
    game = Clobber(rows, cols)
    game.print_board()

    moves = 0
    ai1_turn = True

    while True:
        current_player_char = "B" if ai1_turn else "W"

        if ai1_turn:
            params = ai1_params
            agent_name_base = "AI 1 (B)"
            is_maximizing_for_this_turn = True
        else:
            params = ai2_params
            agent_name_base = "AI 2 (W)"
            is_maximizing_for_this_turn = False

        heuristic_id = params['heuristic_id']
        depth = params['depth']
        use_alpha_beta = params['alpha_beta_algo']
        # Get suboptimal_chance from params, to be passed to the algorithm
        current_suboptimal_chance = params.get('suboptimal_chance', 0.0)

        agent_name_log = (f"{agent_name_base}, H:{heuristic_id}, D:{depth}, "
                          f"{'AlphaBeta' if use_alpha_beta else 'Minimax'}, "
                          f"SuboptimalChance:{current_suboptimal_chance * 100:.0f}%")

        print(f"\n--- Game Round {moves // 2 + 1} ({current_player_char}'s turn) ---")

        if game.is_over(current_player_char):
            print(f"{agent_name_log} has no available moves.")
            winner_name = "AI 2 (W)" if ai1_turn else "AI 1 (B)"
            loser_name = "AI 1 (B)" if ai1_turn else "AI 2 (W)"
            print(f"Game Over! {loser_name} is blocked. {winner_name} Wins!")
            print(f"Total moves made in game: {moves}")
            break

        print(f"Thinking for {agent_name_log}...")

        eval_score, best_move, visited_nodes, time_taken, was_random_choice = 0, None, 0, 0.0, False

        if not use_alpha_beta:
            eval_score, best_move, visited_nodes, time_taken, was_random_choice = minimax(
                game, heuristic_id, depth, is_maximizing_for_this_turn,
                suboptimal_chance=current_suboptimal_chance, is_root_call=True
            )
        else:
            eval_score, best_move, visited_nodes, time_taken, was_random_choice = alpha_beta(
                game, heuristic_id, depth, is_maximizing_for_this_turn,
                suboptimal_chance=current_suboptimal_chance, is_root_call=True
            )

        if best_move:
            if was_random_choice:
                print(f"{agent_name_log}: Chose RANDOM suboptimal move {best_move} (Eval: {eval_score:.2f})")
            else:
                print(
                    f"{agent_name_log}: Chose move {best_move} with Evaluation: {eval_score:.2f}, "
                    f"Visited Nodes: {visited_nodes}, Time: {time_taken:.4f}s"
                )
            game.make_move(best_move[0][0], best_move[0][1], best_move[1][0], best_move[1][1])
            moves += 1
            game.print_board()
            ai1_turn = not ai1_turn
        else:
            print(f"{agent_name_log} could not find a move or chose not to.")
            winner_name = "AI 2 (W)" if ai1_turn else "AI 1 (B)"
            loser_name = "AI 1 (B)" if ai1_turn else "AI 2 (W)"
            print(f"Game Over! {loser_name} did not make a move. {winner_name} Wins!")
            print(f"Total moves made in game: {moves}")
            break


if __name__ == "__main__":
    """AI vs. Player"""
    # rows = 6
    # cols = 5
    # depth = 3
    # heuristic_id = 1
    # game_loop(rows, cols, heuristic_id, depth, alpha_beta_algo=True)



    """AI vs. AI"""
    # AI1: Stronger, deterministic
    ai1_config = {'heuristic_id': 5, 'depth': 3, 'alpha_beta_algo': True, 'suboptimal_chance': 0.0}

    # AI2: Weaker, uses simpler heuristic, lower depth, and 20% chance of random move
    ai2_config = {'heuristic_id': 3, 'depth': 2, 'alpha_beta_algo': False, 'suboptimal_chance': 0.2}

    # Start the game between the two AIs
    ai_game_loop(rows=6, cols=5, ai1_params=ai1_config, ai2_params=ai2_config)
