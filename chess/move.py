"""
Represent a typical chess game
"""

class ChessMove:

    ranks_to_rows = { "1": 7,
                      "2": 6,
                      "3": 5,
                      "4": 4,
                      "5": 3,
                      "6": 2,
                      "7": 1,
                      "8": 0 }

    files_to_cols = { "a": 0,
                      "b": 1,
                      "c": 2,
                      "d": 3,
                      "e": 4,
                      "f": 5,
                      "g": 6,
                      "h": 7 }

    rows_to_ranks = { v: k for k, v in ranks_to_rows.items() }
    cols_to_files = { v: k for k, v in files_to_cols.items() }

    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wP" and self.end_row == 0) or (
                self.piece_moved == "bP" and self.end_row == 7)

        # en passant
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

        # castle move
        self.is_castle_move = is_castle_move

        self.is_capture = self.piece_captured != "--"
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        """
        Overriding the equals method.
        """
        if isinstance(other, ChessMove):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        """
        Return a valid chess notation
        """
        if self.is_pawn_promotion:
            return self.get_rank_file(self.end_row, self.end_col) + "Q"
        if self.is_castle_move:
            if self.end_col == 1:
                return "0-0-0"
            else:
                return "0-0"
        if self.is_enpassant_move:
            return self.get_rank_file(self.start_row, self.start_col)[0] + "x" + self.get_rank_file(self.end_row,
                                                                                                self.end_col) + " e.p."
        if self.piece_captured != "--":
            if self.piece_moved[1] == "P":
                return self.get_rank_file(self.start_row, self.start_col)[0] + "x" + self.get_rank_file(self.end_row,
                                                                                                    self.end_col)
            else:
                return self.piece_moved[1] + "x" + self.get_rank_file(self.end_row, self.end_col)
        else:
            if self.piece_moved[1] == "P":
                return self.get_rank_file(self.end_row, self.end_col)
            else:
                return self.piece_moved[1] + self.get_rank_file(self.end_row, self.end_col)

        # TODO Disambiguating moves

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __str__(self):
        if self.is_castle_move:
            return "0-0" if self.end_col == 6 else "0-0-0"

        end_square = self.get_rank_file(self.end_row, self.end_col)

        if self.piece_moved[1] == "P":
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            else:
                return end_square + "Q" if self.is_pawn_promotion else end_square

        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square
