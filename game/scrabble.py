from game.board import Board
from game.player import Player
from game.models import Dictionary
from game.tilebag import Tilebag

class WordNotValid(Exception):
    pass

class ScrabbleGame:
    def __init__(self, amount):
        self.board = Board(15, 15)
        self.current_player_index = 0
        self.tilebag = Tilebag()
        self.players = []
        self.dictionary = Dictionary('dictionaries/dictionary.txt')
        for i in range(amount):
            self.players.append(Player())

    def calculate_word_score(self, word):
        score = 0
        for tile in word:
            score += tile.individual_score()
        return score

    def word_score(self, word: list):
        score = 0
        word_multipliers = 1
        for square in word:
            if hasattr(square, 'word_multiplier') and square.word_multiplier is not None:
                word_multipliers *= square.word_multiplier
                square.multiplier_is_up()
            score += square.individual_score()
        return score * word_multipliers

    def change_player_index(self):
        if self.current_player_index == len(self.players) - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    def place_word(self, word, starting_row, starting_column, direction):
        self.last_word = []
        if not self.check_word_validity(word):
            raise WordNotValid
        if direction.lower() == 'horizontal':
            self.place_horizontal(word, starting_row, starting_column)
        elif direction.lower() == 'vertical':
            self.place_vertical(word, starting_row, starting_column)

    def place_horizontal(self, word, starting_row, starting_column):
        current_row = starting_row
        current_col = starting_column

        for tile in word:
            if current_col >= 15:
                raise WordNotValid("The word does not fit on the board.")

            square = self.board.grid[current_row][current_col]

            if square.has_letter() and square.letter != tile:
                raise WordNotValid("The word interferes with another word on the board.")

            square.insert_letter(tile)  # Insertar la letra en el tablero
            current_col += 1

        self.last_word = word

    def place_vertical(self, word, starting_row, starting_column):
        current_row = starting_row
        current_col = starting_column

        for tile in word:
            if current_row >= 15:
                raise WordNotValid("The word does not fit on the board.")

            square = self.board.grid[current_row][current_col]

            if square.has_letter() and square.letter != tile:
                raise WordNotValid("The word interferes with another word on the board.")

            square.insert_letter(tile)  # Insertar la letra en el tablero
            current_row += 1

        self.last_word = word
        return True


    def get_scores(self):
        scores = {}
        for player in self.players:
            scores[player.get_name()] = player.get_score()
        return scores
    
    def check_word_validity(self, word):
        check = ""
        for letter in word:
            check += letter.get_letter()
        return self.dictionary.has_word(check.lower())

    def check_first_turn(self):
        return self.board.board_empty()

    def check_left_square(self, row, col):
        if col > 0:
            return self.board.grid[row][col - 1].has_letter()
        return False

    def check_right_square(self, row, col):
        if col < self.board.cols - 1:
            return not self.board.grid[row][col + 1].has_letter()
        return False

    def check_up_square(self, row, col):
        if row > 0:
            return self.board.grid[row - 1][col].has_letter()
        return False

    def check_down_square(self, row, col):
        if row < self.board.rows - 1:
            return self.board.grid[row + 1][col].has_letter()
        return False

    def check_word_left(self, row, col):
        while col > 0 and self.board.grid[row][col - 1].has_letter():
            col -= 1
        return col > 0 and self.board.grid[row][col].has_letter()

