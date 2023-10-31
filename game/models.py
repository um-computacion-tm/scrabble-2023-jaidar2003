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

PLAYERS = 2

class ScrabbleCli:
    def __init__(self):
        self.game = ScrabbleGame(PLAYERS)
        self.game_state = None
        self.VALID_ACTIONS = {
            'rules': self.game_rules,
            'elements': self.game_elements,
            'pass': self.pass_turn,
            'play': self.play_turn,
            'draw': self.takeout_tiles,
            'quit': self.end_game,
            'scores': self.show_scores,
            'show board': self.show_board,
            'tiles': self.show_tiles,
        }

    def game_rules(self):
            scrabbles_rules = """
            Scrabble rules:
                        
                        1. Aim of the game: The aim of Scrabble is to form words on a game board using letters with assigned values to obtain the highest possible score.
                        
                        2. The board: The Scrabble board is a square of 15x15 squares. Some squares have special values and bonuses.
                        
                        3. Tiles: The game is played with tiles representing letters. Each tile has a numerical value that determines its score. 
                        The number of tiles and their value vary according to the language you are playing in.
                        
                        4. Start of the game: Each player takes 7 tiles at random from the set of tiles, which are replenished after each play.
                        
                        5. Words: Players must form words on the board using their counters. Words must be formed from left to right or top to bottom, 
                        and must be connected to at least one letter already on the board.
                        
                        6. Scoring: Each letter has a numerical value assigned to it. The score of a word is the sum of the letter values in that word. In addition, the board has bonus squares, 
                        the board has bonus squares that can double or triple the score of a word or a letter.
                        
                        7. Shifting tiles: A player may choose to shift some or all of his tiles on his turn, but this costs him a full turn.
                        
                        8. End of the game: The game ends when all the tiles have been used up and a player has used all his tiles or when no more valid moves can be made.
                        
                        9. Winner: The player with the highest score at the end of the game wins.
                        
                        10. Valid words: Words must be valid words in the language you are using, and can be consulted in an official dictionary if a dispute arises.
                        """
            print(scrabbles_rules)

    def game_elements(self):
        print("1 board, 100 tiles, 4 stands, 1 bag of tiles, 1 regulation.")

    def start_game(self):
        self.game_state_start()
        self.get_player_names()
        self.start_player_tiles()
        self.game.board.premium_squares()
        while not self.game_state == 'over':
            self.player_turn()

    def show_board(self):
        self.game.board.print_board()

    def player_turn(self):
        action = input("What would you like to do? (rules, elemets, show board, play, pass, draw, scores, quit, tiles) ").lower()
        chosen_action = self.VALID_ACTIONS.get(action)
        if chosen_action:
            chosen_action()
        else:
            options = ', '.join(self.VALID_ACTIONS.keys())
            print(f"Action not valid, please choose an opcion from the followings...: {options}")

    def play_turn(self):
        word = input("Give a word to enter: ").upper()
        row = int(input("Give an Y position: "))
        column = int(input("Give an X position: "))
        direction = input("Give direction (horizontal or vertical): ")

        player_tiles = self.game.players[self.game.current_player_index].get_letters()
        for letter in word:

            if letter not in player_tiles:
                print(f"Letter '{letter}' not found in player's tiles")
                return  

        print(self.game.players[self.game.current_player_index].give_requested_tiles(word))
    
        word = self.game.players[self.game.current_player_index].give_requested_tiles(word)
        self.game.place_word(word, row, column, direction)
        self.game.players[self.game.current_player_index].loss_tiles(word)
        self.game.players[self.game.current_player_index].increase_score(self.game.word_score(self.game.last_word))
        self.game.change_player_index()

        self.game.board.print_board()


    def first_turn(self):
        print("Since there is no word in the center, please place your word there to start the game")
        word = input("Give a word to enter: ").upper()
        row = int(input("State starting X: "))
        column = int(input("State starting : "))
        direction = input("State direction (horizontal or vertical: ")
        word = self.game.players[self.game.current_player_index].give_requested_tiles(word)
        if not self.valid_first_word(word, row, column, direction):
            self.game.place_word(word, row, column, direction)
            self.game.players[self.game.current_player_index].loss_tiles(word)
            self.game.players[self.game.current_player_index].increase_score(self.game.word_score(self.game.last_word))
            self.game.change_player_index()

    def pass_turn(self):
        self.game.change_player_index()

    def takeout_tiles(self):
        amount = int(input("How many tiles do you want to draw? "))
        self.game.players[self.game.current_player_index].takeout_tiles(self.game.tilebag, amount)
        self.game.change_player_index()

    def check_tiles(self):
        if len(self.game.tilebag.tiles) <= 0:
            self.end_game()

    def show_scores(self):
        scores = self.game.get_scores()
        for element in scores:
            print("Score for", element, ":", scores[element])

    def game_state_start(self):
        self.game_state = 'ongoing'

    def end_game(self):
        self.game_state = 'over'

    def start_player_tiles(self):
        for player in self.game.players:
            player.takeout_tiles(self.game.tilebag, 7)

    def get_player_names(self):
        for i in range(len(self.game.players)):
            self.game.players[i].set_name(input(f"Player {i + 1}, write your nickname: "))

    def show_tiles(self):
        tiles = self.game.players[self.game.current_player_index].show_tiles()
        print(tiles)

    def check_game_over(self):
        return len(self.game.tilebag.tiles) == 0 and all(player.passed_turn for player in self.game.players)

    @staticmethod
    def valid_first_word(word, starting_row, starting_column, direction):
        mock_game = ScrabbleGame(1)
        mock_game.place_word(word, starting_row, starting_column, direction)
        return mock_game.board.board_empty()

class Tile:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.letter == other.letter and self.value == other.value
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def individual_score(self):
        return self.value

    def get_value(self):
        return self.value

    def get_letter(self):
        return self.letter

    def __repr__(self):
        return f"{self.letter}:{self.value}"

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

class Square:
    def __init__(self, multiplier: int = 1, letter: Tile = None, word_multiplier: int = 1, letter_multiplier: int = 1):

        self.multiplier = multiplier
        self.letter = letter  
        self.word_multiplier = word_multiplier
        self.letter_multiplier = letter_multiplier
        self.multiplier_type = None
        
    
    def has_letter(self):
        return self.letter is not None
    
    def has_tile(self):  
        return self.has_letter()

    def has_multiplier(self):
        return self.multiplier > 1
    
    def get_multiplier_type(self):
        return self.multiplier_type
    
    def get_multiplier(self):
        return self.multiplier

    def insert_letter(self, letter):
        if not self.has_letter():
            self.letter = letter

    def set_multiplier_type(self, word):
        self.multiplier_type = word

    def multiplier_is_up(self):
        if self.word_multiplier > 1:
            self.word_multiplier -= 1

    def put_tile(self, letter):
        if not self.has_tile():
            self.letter = letter
        self.multiplier_is_up()

    def set_multiplier(self, amount):
        self.multiplier = amount

    def get_tile(self):
        return self.letter
 
    def individual_score(self):
        return self.letter.get_value() * self.multiplier

    def set_word_multiplier(self, amount):
        self.multiplier = amount

    def set_letter_multiplier(self, amount):
        self.multiplier = amount

    def __repr__(self):
        if self.letter:
            return repr(self.letter)
        if self.multiplier > 1:
            return f'{"W" if self.multiplier_type == "word" else "L"}x{self.multiplier}'
        else:
            return '   '
        
class Player:
    def __init__(self):
        self.score = 0
        self.tiles = []
        self.name = ''

    def increase_score(self, points):
        self.score += points

    def takeout_tiles(self, bag: Tilebag, num_tiles):
        self.tiles.extend(bag.take(num_tiles))

    def exchange_tile(self, tile, bag: Tilebag):
        for i, current_tile in enumerate(self.tiles):
            if current_tile == tile:
                exchanged_tile = self.tiles.pop(i)
                bag.put([exchanged_tile])
                break

        self.tiles.extend(bag.take(1))

    def give_requested_tiles(self, word):
        tiles = []
        for letter in word:
            letter = letter.lower()  
            tile = self.find_letter_in_tiles(letter)
            print(tile)
            if tile is not None:
                tiles.append(tile)
            else:
                print(f"Letter '{letter}' not found in player's tiles")
                return None
        print(tiles)
        return tiles


    def find_letter_in_tiles(self, letter):
        for tile in self.tiles:
            if tile.get_letter() == letter.upper():
                return tile
        return None

    def loss_tiles(self, word):
        for tile in word:
            self.loss_a_tile(tile)

    def loss_a_tile(self, tile):
        for i in range(len(self.tiles)):
            if self.tiles[i].get_letter() == tile.get_letter():
                self.tiles.pop(i)
                break

    def set_name(self, name):
        self.name = name
    
    def get_score(self):
        return self.score
    
    def get_name(self):
        return self.name

    def show_tiles(self):
       return self.tiles
    
    def get_letters(self):
        return [tile.letter for tile in self.tiles]
    

class Dictionary:
    def __init__(self, file_path):
        self.words = self.load_words(file_path)

    def load_words(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(word.strip() for word in file)

    def has_word(self, word):
        return word in self.words
