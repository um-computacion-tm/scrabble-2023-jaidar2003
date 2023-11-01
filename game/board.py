from game.square import Square

class PlacementOutOfBounds(Exception):
    pass


class WordNotValid(Exception):
    pass


class WordOutOfBounds(Exception):
    pass

class Board:

    COLS = 15
    ROWS = 15

    TRIPLE_WORD_SCORE = ((0, 0), (7, 0), (14, 0), (0, 7), (14, 7), (0, 14), (7, 14), (14, 14))
    DOUBLE_WORD_SCORE = ((1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3),
                        (10, 4), (13, 13), (12, 12), (11, 11), (10, 10))

    TRIPLE_LETTER_SCORE = ((1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5),
                        (13, 9))
    DOUBLE_LETTER_SCORE = ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12),
                        (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8),
                        (14, 3), (14, 11))

    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
        self.grid = [[Square(word_multiplier=2) for _ in range(columns)] for _ in range(rows)]

    def display(self):
        for row in self.grid:
            print(' '.join(row))

    def is_valid_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def place_tile(self, tile, row, col):
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            return False  
        square = self.grid[row][col]
        if square.has_tile():
            return False  
        square.insert_letter(tile)
        return True
    
    def get_square(self, row, col):
        if self.is_valid_position(row, col):
            square = self.grid[row][col]
            if isinstance(square, Square) and square.has_letter():
                return square
        return None

    def get_tile(self, row, col):
        if self.is_valid_position(row, col):
            square = self.grid[row][col]
            if isinstance(square, Square) and square.has_letter():
                return square.get_letter()
        return None
    
    def board_empty(self):
        return not self.grid[7][7].has_tile()
    
    def premium_squares(self):
        for row, col in self.TRIPLE_WORD_SCORE:
            self.grid[row][col].set_word_multiplier(3)

        for row, col in self.DOUBLE_WORD_SCORE:
            self.grid[row][col].set_word_multiplier(2)

        for row, col in self.TRIPLE_LETTER_SCORE:
            self.grid[row][col].set_letter_multiplier(3)

        for row, col in self.DOUBLE_LETTER_SCORE:
            self.grid[row][col].set_letter_multiplier(2)

    def set_square_multiplier(self, row, col, word_multiplier=None, letter_multiplier=None):
        if self.is_valid_position(row, col):
            square = self.grid[row][col]
            if word_multiplier is not None:
                square.set_word_multiplier(word_multiplier)
            if letter_multiplier is not None:
                square.set_letter_multiplier(letter_multiplier)      

    def print_board(self):
        print('\n  |' + ''.join([f' {str(row_index).rjust(2)} ' for row_index in range(15)]))
        for row_index, row in enumerate(self.grid):
            print(
                str(row_index).rjust(2) +
                '| ' +
                ' '.join([repr(square) for square in row])
            )