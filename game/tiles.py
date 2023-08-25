import random

class ScrabbleGame:
    def __init__(self, amount, board, bag):
        self.board = board
        self.tilebag = bag
        self.players = []
        for i in range(amount):
            self.players.append(Player(f"Player {i}", self.board, self.tilebag))

class Tile:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

class BagTiles:
    def __init__(self):
        self.tiles = ['A'] * 9 + ['B'] * 2 + ['C'] * 2 + ['D'] * 4 + ['E'] * 12 + ['F'] * 2 + ['G'] * 3 + ['H'] * 2 + ['I'] * 9 + ['J'] * 1 + ['K'] * 1 + ['L'] * 4 + ['M'] * 2 + ['N'] * 6 + ['O'] * 8 + ['P'] * 2 + ['Q'] * 1 + ['R'] * 6 + ['S'] * 4 + ['T'] * 6 + ['U'] * 4 + ['V'] * 2 + ['W'] * 2 + ['X'] * 1 + ['Y'] * 2 + ['Z'] * 1
        random.shuffle(self.tiles)
        self.remaining_tiles = self.tiles.copy()

    def get_tile_value(self, letter):
        return {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
            'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
            'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
            'Y': 4, 'Z': 10
        }[letter]

    def draw_tiles(self, count):
        drawn_tiles = []
        for _ in range(count):
            if self.remaining_tiles:
                drawn_tiles.append(Tile(self.remaining_tiles.pop(), 1))
        return drawn_tiles

    def tiles_remaining(self):
        return len(self.remaining_tiles)


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]

    def display(self):
        for row in self.grid:
            print(' '.join(row))

    def is_valid_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def place_tile(self, tile, row, col):
        if self.is_valid_position(row, col):
            self.grid[row][col] = tile.letter
            return True
        return False

class Square:
    def __init__(self, multiplier: int = 1, letter: Tile = None):
        self.multiplier = multiplier
        self.letter = letter

    def has_letter(self):
        return self.letter is not None

    def has_multiplier(self):
        return self.multiplier > 1

    def insert_letter(self, letter):
        if not self.has_letter():
            self.letter = letter

class Player:
    def __init__(self, name, board, bag):
        self.name = name
        self.board = board
        self.bag = bag
        self.hand = []
        self.score = 0

    def draw_tiles(self, count):
        drawn_tiles = self.bag.draw_tiles(count)
        self.hand.extend(drawn_tiles)
        return drawn_tiles

    def calculate_score(self, word, row, col, direction):
        score = 0
        word_multiplier = 1
        for i, letter in enumerate(word):
            tile_value = self.get_tile_value(letter)
            score += tile_value
        return score

    def get_tile_value(self, letter):
        return self.bag.get_tile_value(letter)

    def exchange_tiles(self, tiles_to_exchange):
        exchanged_tiles = []
        for tile in tiles_to_exchange:
            if tile in self.hand:
                exchanged_tiles.append(tile)
                self.hand.remove(tile)
        new_tiles = self.bag.draw_tiles(len(exchanged_tiles))
        self.hand.extend(new_tiles)
        return exchanged_tiles

class Dictionary:
    def __init__(self, file_path):
        self.words = self.load_words(file_path)

    def load_words(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(word.strip() for word in file)

    def has_word(self, word):
        return word in self.words

if __name__ == "__main__":
    bag = BagTiles()
    board = Board(15, 15)
    player = Player("Player 1", board, bag)