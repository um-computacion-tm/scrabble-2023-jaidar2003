from game.scrabble import ScrabbleGame
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