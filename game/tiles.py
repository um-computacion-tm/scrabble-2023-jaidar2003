import random

class ScrabbleGame:
    def __init__(self, amount):
        self.board = Board(rows=15, cols=15)
        self.tilebag = Tilebag()
        self.players = []
        self.dictionary = Dictionary('dictionaries/dictionary.txt')
        for i in range(amount):
            self.players.append(Player())

    def word_score(self, word: list):
        score = 0
        word_multipliers = 1  # Inicializamos a 1 para multiplicar por 1 si no hay multiplicadores de palabra
        for square in word:
            if square.word_multiplier is not None:
                word_multipliers *= square.word_multiplier
                square.multiplier_is_up()
            score += square.individual_score()
        return score * word_multipliers

    

class Tile:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.letter == other.letter and self.value == other.value
        return False

    def __repr__(self):
        return f"Tile(letter='{self.letter}', value={self.value})"

    def get_value(self):
        return self.value

    def get_letter(self):
        return self.letter

LETTER_COUNT = {
    'A': (1, 12),
    'E': (1, 12),
    'O': (1, 9),
    'I': (1, 6),
    'S': (1, 6),
    'N': (1, 5),
    'L': (1, 4),
    'R': (1, 5),
    'U': (1, 5),
    'T': (1, 12),
    'D': (2, 5),
    'G': (2, 2),
    'C': (3, 4),
    'B': (3, 2),
    'M': (3, 2),
    'P': (3, 2),
    'H': (4, 2),
    'F': (4, 1),
    'V': (4, 1),
    'Y': (4, 1),
    'CH': (5, 1),
    'Q': (5, 1),
    'J': (6, 1),
    'LL': (6, 1),
    'Ñ': (6, 1),
    'RR': (6, 1),
    'X': (6, 1),
    'Z': (7, 1)
}

class DrawingMoreThanAvailable(Exception):
    pass

class Tilebag:
    def __init__(self):
        self.tiles = []
        for letter, (quantity, score) in LETTER_COUNT.items():
            tile = Tile(letter, quantity)
            self.tiles.extend([tile] * score)
        random.shuffle(self.tiles)

    def take(self, count):
        random.shuffle(self.tiles)
        if count > len(self.tiles):
            raise DrawingMoreThanAvailable
        tiles = [self.tiles.pop() for _ in range(count)]
        return tiles

    def put(self, tiles):
        self.tiles.extend(tiles)


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
    def __init__(self, multiplier: int = 1, letter: Tile = None, word_multiplier: int = 1):
        self.multiplier = multiplier
        self.letter = letter
        self.word_multiplier = word_multiplier  # Agrega el atributo word_multiplier

    def has_letter(self):
        return self.letter is not None

    def has_multiplier(self):
        return self.multiplier > 1

    def insert_letter(self, letter):
        if not self.has_letter():
            self.letter = letter

    def multiplier_is_up(self):
        if self.word_multiplier > 1:
            self.word_multiplier -= 1

    def individual_score(self):
        return self.letter.get_value() * self.multiplier

    def __repr__(self):
        return f"Square(multiplier={self.multiplier}, letter={self.letter}, word_multiplier={self.word_multiplier})"


class Player:
    def __init__(self):
        self.score = 0
        self.tiles = []

    def increase_score(self, points):
        self.score += points

    def draw_tiles(self, bag: Tilebag, num_tiles):
        self.tiles.extend(bag.take(num_tiles))

    def exchange_tile(self, tile, bag: Tilebag):
        for i, current_tile in enumerate(self.tiles):
            if current_tile == tile:
                exchanged_tile = self.tiles.pop(i)
                bag.put([exchanged_tile])
                break

        self.tiles.extend(bag.take(1))


class Dictionary:
    def __init__(self, file_path):
        self.words = self.load_words(file_path)

    def load_words(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(word.strip() for word in file)

    def has_word(self, word):
        return word in self.words



if __name__ == "__main__":
    bag = Tilebag()
    board = Board(15, 15)
    player = Player()