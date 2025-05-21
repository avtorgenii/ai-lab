class Clobber:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.black_positions = []
        self.white_positions = []

        for r in range(0, self.rows):
            for c in range(0, self.cols):
                if (r + c) % 2 == 0:
                    self.white_positions.append((r, c))
                else:
                    self.black_positions.append((r, c))

    def print_board(self):
        # Column indices
        print("  ", end="")
        for c in range(0, self.cols):
            print(c, end=" | ")

        print()

        # Rows
        for r in range(0, self.rows):
            print(r, end=" ")  # row indices
            for c in range(0, self.cols):
                if (r, c) in self.black_positions:
                    print("B", end=" | ")
                elif (r, c) in self.white_positions:
                    print("W", end=" | ")
                else:
                    print("_", end=" | ")

            print()

    def get_valid_moves_for_tile(self, row, col):
        moves = []
        if (row, col) not in self.black_positions and (row, col) not in self.white_positions:
            return []
        elif (row, col) in self.black_positions:
            if (row - 1, col) in self.white_positions:
                moves.append((row - 1, col))
            if (row + 1, col) in self.white_positions:
                moves.append((row + 1, col))
            if (row, col - 1) in self.white_positions:
                moves.append((row, col - 1))
            if (row, col + 1) in self.white_positions:
                moves.append((row, col + 1))
        elif (row, col) in self.white_positions:
            if (row - 1, col) in self.black_positions:
                moves.append((row - 1, col))
            if (row + 1, col) in self.black_positions:
                moves.append((row + 1, col))
            if (row, col - 1) in self.black_positions:
                moves.append((row, col - 1))
            if (row, col + 1) in self.black_positions:
                moves.append((row, col + 1))

        return moves

    def is_players_tile(self, row, col, player):
        if player == "W":
            return (row, col) in self.white_positions
        elif player == "B":
            return (row, col) in self.black_positions
        else:
            return False

    def get_all_valid_moves(self, player):
        moves = []
        if player == 'B':
            pieces = self.black_positions
        else:
            pieces = self.white_positions
        for r, c in pieces:
            moves.extend([((r, c), target) for target in self.get_valid_moves_for_tile(r, c)])
        return moves

    def is_over(self, current_player):
        return len(self.get_all_valid_moves(current_player)) == 0

    def make_move(self, start_row, start_col, end_row, end_col):
        if (end_row, end_col) in self.get_valid_moves_for_tile(start_row, start_col):
            if (start_row, start_col) in self.black_positions:
                self.black_positions.remove((start_row, start_col))
                self.white_positions.remove((end_row, end_col))
                self.black_positions.append((end_row, end_col))
            elif (start_row, start_col) in self.white_positions:
                self.white_positions.remove((start_row, start_col))
                self.black_positions.remove((end_row, end_col))
                self.white_positions.append((end_row, end_col))

    def evaluate(self, heuristic_id):
        """Positive values favor White, negative favor Black."""
        heuristics = {
            1: self.heuristic_1,
            2: self.heuristic_2,
            3: self.heuristic_3,
            4: self.heuristic_4,
            5: self.heuristic_5,
        }

        return heuristics[heuristic_id]()

    def heuristic_1(self):
        """
        Counts the difference between the number of black and white pieces.
        """
        return len(self.black_positions) - len(self.white_positions)

    def heuristic_2(self):
        """
        Mobility. Counts the difference in the number of possible moves between black and white.
        """
        return len(self.get_all_valid_moves("B")) - len(self.get_all_valid_moves("W"))

    def heuristic_3(self):
        """
        Combination of material and mobility with weights.
        """
        material_weight = 2  # Weight for material difference
        mobility_weight = 1  # Weight for mobility difference
        material_diff = self.heuristic_1()
        mobility_diff = self.heuristic_2()
        return (material_weight * material_diff) + (mobility_weight * mobility_diff)

    def heuristic_4(self):
        """
        Adaptive Heuristic 1: Focus on material in the late game, mobility in the early game.
        """
        current_pieces = len(self.black_positions) + len(self.white_positions)
        game_progress = 1 - (current_pieces / (self.rows * self.cols)) # 0 at start, approaches 1 at end

        material_diff = self.heuristic_1()
        mobility_diff = self.heuristic_2()

        # Adjust weights based on game progress
        # Early game (low game_progress): focus more on mobility
        # Late game (high game_progress): focus more on material
        material_weight = 1 + (game_progress * 3) # Increases from 1 to 4
        mobility_weight = 2 - (game_progress * 1.5) # Decreases from 2 to 0.5 (or less)

        return (material_weight * material_diff) + (mobility_weight * mobility_diff)

    def heuristic_5(self):
        """
        Adaptive Heuristic 2: Emphasizes blocking/trapping opponents.
        Combines material and mobility, but adds a component for "blocked opponent moves".
        """
        material_diff = self.heuristic_1()
        mobility_diff = self.heuristic_2()

        # Calculate how many of the opponent's pieces are stuck
        white_stuck_pieces = sum(1 for r, c in self.white_positions if not self.get_valid_moves_for_tile(r, c))
        black_stuck_pieces = sum(1 for r, c in self.black_positions if not self.get_valid_moves_for_tile(r, c))

        # A positive value means more black pieces are stuck, which is good for White
        stuck_pieces_diff = black_stuck_pieces - white_stuck_pieces

        # Adapt weights based on total pieces left (game state)
        current_pieces = len(self.black_positions) + len(self.white_positions)
        # Ratio of pieces remaining (1.0 at start, approaches 0 at end)
        pieces_remaining_ratio = current_pieces / (self.rows * self.cols)

        # Early game (pieces_remaining_ratio high): balance material, mobility, and some trapping
        # Late game (pieces_remaining_ratio low): trapping becomes more critical, potentially decisive
        material_weight = 2.0
        mobility_weight = 1.0
        # Increase trapping weight as pieces decrease
        trapping_weight = 1.0 + (1 - pieces_remaining_ratio) * 2

        return (material_weight * material_diff) + (mobility_weight * mobility_diff) + (trapping_weight * stuck_pieces_diff)


if __name__ == "__main__":
    game = Clobber(6, 10)
    game.print_board()
