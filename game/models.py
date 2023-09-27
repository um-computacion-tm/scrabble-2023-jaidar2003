import random
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

    def word_score(self, word: list):
        score = 0
        word_multipliers = 1  
        for square in word:
            if square.word_multiplier is not None:
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
        if direction.lower() == 'vertical':
            self.place_vertical(word, starting_row, starting_column)


    def place_horizontal(self, word, starting_row, starting_column):
        current_row = starting_row
        current_col = starting_column

        for tile in word:
            if current_col >= 15:
                raise WordNotValid("La palabra no cabe en el tablero.")

            square = self.board.grid[current_row][current_col]

            if square.has_letter() and square.letter != tile:
                raise WordNotValid("La palabra interfiere con otra en el tablero.")

            square.insert_letter(tile)
            current_col += 1

        self.last_word = word

    def place_vertical(self, word, starting_row, starting_column):
        current_row = starting_row
        current_col = starting_column

        for tile in word:
            if current_row >= 15:
                raise WordNotValid("La palabra no cabe en el tablero.")

            square = self.board.grid[current_row][current_col]

            if square.has_letter() and square.letter != tile:
                raise WordNotValid("La palabra interfiere con otra en el tablero.")

            square.insert_letter(tile)
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
        return self.board.is_board_empty()

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

PLAYERS = 2


class ScrabbleCli:
    def __init__(self):
        self.game = ScrabbleGame(PLAYERS)
        self.game_state = None
        self.VALID_ACTIONS = {
            'pass': self.pass_turn,
            'play': self.play_turn,
            'draw': self.draw_tiles,
            'quit': self.end_game,
            'scores': self.show_scores,
            'tiles': self.show_tiles,
        }

    def player_turn(self):
        action = input("What would you like to do? (play, pass, draw, scores, quit, tiles) ").lower()
        chosen_action = self.VALID_ACTIONS.get(action)
        if chosen_action:
            chosen_action()
        else:
            options = ', '.join(self.VALID_ACTIONS.keys())
            print(f"Action not valid, please choose from: {options}")

    def play_turn(self):
        word = input("Give a word to enter: ").lower()
        row = int(input("State starting row: "))
        column = int(input("State starting column: "))
        direction = input("State direction (horizontal or vertical: )")
        word = self.game.players[self.game.current_player_index].give_requested_tiles(word)
        self.game.place_word(word, row, column, direction)
        self.game.players[self.game.current_player_index].forfeit_tiles(word)
        self.game.players[self.game.current_player_index].increase_score(self.game.word_score(self.game.last_word))
        self.game.change_player_index()

    def pass_turn(self):
        self.game.change_player_index()

    def draw_tiles(self):
        amount = int(input("How many tiles do you want to draw? "))
        self.game.players[self.game.current_player_index].draw_tiles(self.game.tilebag, amount)
        self.game.change_player_index()

    def start_game(self):
        self.game_state_start()
        self.get_player_names()
        self.start_player_tiles()
        while True:
            if self.game.check_first_turn():
                self.first_turn()
                continue
            self.check_tiles()
            if self.game_state == 'over':
                break
            self.player_turn()

    def end_game(self):
        self.game_state = 'over'

    def show_tiles(self):
        tiles = self.game.players[self.game.current_player_index].show_tiles()
        print(tiles)

    def show_scores(self):
        scores = self.game.get_scores()
        for element in scores:
            print("Score for", element, ":", scores[element])

    def check_tiles(self):
        if len(self.game.tilebag.tiles) <= 0:
            self.end_game()

    def game_state_start(self):
        self.game_state = 'ongoing'

    def get_player_names(self):
            for i in range(len(self.game.players)):
                self.game.players[i].set_name(input(f"Player {i + 1} state your name: "))

    def start_player_tiles(self):
        for player in self.game.players:
            player.draw_tiles(self.game.tilebag, 7)

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
    
    def get_remaining_tiles(self):
        return len(self.tiles)

class Rack:
    def __init__(self, bag):
        self.rack = []
        self.bag = bag
        self.initialize()

    def add_to_rack(self):
        self.rack.append(self.bag.take(1)[0])  

    def initialize(self):
        for i in range(7):
            self.add_to_rack()

    def get_rack_str(self):
        return ", ".join(str(item.get_letter()) for item in self.rack)

    def get_rack_arr(self):
        return self.rack

    def remove_from_rack(self, tile):
        self.rack.remove(tile)

    def get_rack_length(self):
        return len(self.rack)

    def replenish_rack(self):
        while self.get_rack_length() < 7 and self.bag.get_remaining_tiles() > 0:
            self.add_to_rack()


class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
        self.grid = [[Square() for _ in range(columns)] for _ in range(rows)]

    def display(self):
        for row in self.grid:
            print(' '.join(row))

    def is_valid_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def place_tile(self, tile, row, col):
        if self.is_valid_position(row, col):
            self.grid[row][col] = tile.letter
            return True
        else:
            return False
    
    def get_square(self, row, col):
        if self.is_valid_position(row, col):
            square = self.grid[row][col]
            if isinstance(square, Square) and square.has_letter():
                return square
        return None  # Return None for empty squares, invalid positions, or non-Square objects

    def is_board_empty(self):
        return not self.grid[7][7].has_tile()
        
    def print_row(self):
        pass


class Square:
    def __init__(self, multiplier: int = 1, letter: Tile = None, word_multiplier: int = 1):
        self.multiplier = multiplier
        self.letter = letter
        self.word_multiplier = word_multiplier 

    def has_letter(self):
        return self.letter is not None

    def has_multiplier(self):
        return self.multiplier > 1
    
    def has_tile(self):  
        return self.has_letter()

    def insert_letter(self, letter):
        if not self.has_letter():
            self.letter = letter

    def multiplier_is_up(self):
        if self.word_multiplier > 1:
            self.word_multiplier -= 1

    def put_tile(self, letter):
        if not self.has_tile():
            self.letter = letter
        self.multiplier_is_up()
    
    def individual_score(self):
        return self.letter.get_value() * self.multiplier

    def __repr__(self):
        return f"Square(multiplier={self.multiplier}, letter={self.letter}, word_multiplier={self.word_multiplier})"


class Player:
    def __init__(self):
        self.score = 0
        self.tiles = []
        self.name = ''

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
    
    def set_name(self, name):
        self.name = name
    
    def get_score(self):
        return self.score
    
    def get_name(self):
        return self.name

    def show_tiles(self):
        return self.tiles
    
    
class Dictionary:
    def __init__(self, file_path):
        self.words = self.load_words(file_path)

    def load_words(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(word.strip() for word in file)

    def has_word(self, word):
        return word in self.words

class Word:
    def __init__(self, word, location, player, direction, board):
        self.word = word.upper()
        self.location = location
        self.player = player
        self.direction = direction.lower()
        self.board = board

    def set_word(self, word):
        self.word = word.upper()

    def set_location(self, location):
        self.location = location

    def set_direction(self, direction):
        self.direction = direction

    def get_word(self):
        return self.word

if __name__ == "__main__":
    board = Board(15, 15)
    player = Player()
    bag = Tilebag()