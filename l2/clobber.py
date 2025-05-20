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
            elif (row + 1, col) in self.white_positions:
                moves.append((row + 1, col))
            elif (row, col - 1) in self.white_positions:
                moves.append((row, col - 1))
            elif (row, col + 1) in self.white_positions:
                moves.append((row, col + 1))
        elif (row, col) in self.white_positions:
            if (row - 1, col) in self.black_positions:
                moves.append((row - 1, col))
            elif (row + 1, col) in self.black_positions:
                moves.append((row + 1, col))
            elif (row, col - 1) in self.black_positions:
                moves.append((row, col - 1))
            elif (row, col + 1) in self.black_positions:
                moves.append((row, col + 1))

        return moves

    def get_all_valid_moves(self, player):
        moves = []
        if player == 'B':
            pieces = self.black_positions
        else:
            pieces = self.white_positions
        for r, c in pieces:
            moves.extend([((r, c), target) for target in self.get_valid_moves_for_tile(r, c)])
        return moves

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
        """
        :param heuristic_id: Can be 1, 2 or 3, check Clobber class for details on them
        :return: Evaluation of current game state, if the number is closer to -inf than to +inf - blacks are in favor, otherwise whites
        """
        heuristics = {
            1: self.heuristic_1,
            2: self.heuristic_2,
            3: self.heuristic_3,
        }

        return heuristics[heuristic_id]()

    def heuristic_1(self):
        """
        Material difference.  Counts the difference
        between the number of white and black pieces.
        """
        return len(self.black_positions) - len(self.white_positions)

    def heuristic_2(self):
        """
        Mobility. Counts the difference in the number of possible moves between black and white.
        """
        black_moves = 0
        white_moves = 0
        for r, c in self.black_positions:
            moves = self.get_valid_moves_for_tile(r, c)
            if moves:
                black_moves += len(moves)
        for r, c in self.white_positions:
            moves = self.get_valid_moves_for_tile(r, c)
            if moves:
                white_moves += len(moves)
        return black_moves - white_moves

    def heuristic_3(self):
        """
        Combination of material and mobility with weights.
        """
        material_weight = 2  # Weight for material difference
        mobility_weight = 1  # Weight for mobility difference
        material_diff = self.heuristic_1()
        mobility_diff = self.heuristic_2()
        return (material_weight * material_diff) + (mobility_weight * mobility_diff)


if __name__ == "__main__":
    game = Clobber(6, 10)
    game.print_board()
