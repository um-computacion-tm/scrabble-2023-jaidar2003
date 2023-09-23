import unittest
from game.models import *
from unittest.mock import patch

class TestScrabble(unittest.TestCase):
    def setUp(self):
        self.game = ScrabbleGame(1)
        self.tilebag = Tilebag()
        self.board = self.game.board

    def test_scrabble(self):
        game = ScrabbleGame(1)
        self.assertIsNotNone(game.board)
        self.assertIsNotNone(game.tilebag)
        self.assertEqual(len(game.players), 1)

    def test_word_validation(self):
        game = ScrabbleGame(1)
        word = [Tile('A', 1),
                Tile('R', 1),
                Tile('B', 1),
                Tile('O', 1),
                Tile('L', 1)]
    
    def board_test_score_2(self):
        board = Board()
        board.grid[7][7].set_multiplier(2)
        board.place_tile(7, 7, Tile('A', 1))
        self.assertEqual(board.get_tile(7, 7), Tile('A', 1))
        self.assertEqual(board.grid[7][7].get_multiplier(), 2)

    @patch('random.shuffle')
    def test_board_place_tile(self, patch_shuffle):
        board = Board(15, 15)
        tile = Tile('X', 1)
        self.assertTrue(board.place_tile(tile, 7, 7))
        self.assertEqual(board.grid[7][7], 'X')
        self.assertFalse(patch_shuffle.called)

    def test_square_insert_letter(self):
        square = Square()
        tile = Tile('A', 1)
        square.insert_letter(tile)
        self.assertEqual(square.letter, tile)

    def test_word_score(self):
        game = ScrabbleGame(1)
        player = game.players[0]
        bag = game.tilebag
        board = game.board
        dictionary = game.dictionary

        word = ['A', 'R', 'B', 'O', 'L']
        row, col = 7, 7 
        for letter in word:
            tile = Tile(letter, 1)
            square = Square(letter=tile)
            board.grid[row][col] = square
            col += 1

        expected_score = 0
        for letter in word:
            expected_score += 1

        calculated_score = game.word_score([board.grid[row][col] for col in range(7, 7 + len(word))])

        self.assertEqual(calculated_score, expected_score)
    
    def test_word_score_no_multipliers(self):
        game = ScrabbleGame(1)
        player = game.players[0]
        bag = game.tilebag
        board = game.board
        dictionary = game.dictionary

        word = ['A', 'R', 'B', 'O', 'L']
        row, col = 7, 7 
        for letter in word:
            tile = Tile(letter, 1)
            square = Square(letter=tile)
            board.grid[row][col] = square
            col += 1

        expected_score = len(word) * 1  
        calculated_score = game.word_score([board.grid[row][col] for col in range(7, 7 + len(word))])

        self.assertEqual(calculated_score, expected_score)

    def test_change_player_index(self):
        game = ScrabbleGame(2)
        self.assertEqual(game.current_player_index, 0)
        game.change_player_index()
        self.assertEqual(game.current_player_index, 1)
        game.change_player_index()
        self.assertEqual(game.current_player_index, 0)

    def test_square_occupied(self):
        game = ScrabbleGame(1)
        tiles = [Tile('A', 1),
                Tile('R', 1),
                Tile('B', 1),
                Tile('O', 1),
                Tile('L', 1)]
        
        game.board.grid[7][8].insert_letter(Tile('R', 1))
        game.place_word(tiles, 7, 7, 'horizontal')
        self.assertEqual(game.board.grid[7][7].letter.get_letter(), 'A')
        self.assertEqual(game.board.grid[7][8].letter.get_letter(), 'R')
        self.assertEqual(game.board.grid[7][9].letter.get_letter(), 'B')
        self.assertEqual(game.board.grid[7][10].letter.get_letter(), 'O')
        self.assertEqual(game.board.grid[7][11].letter.get_letter(), 'L')

    def test_place_horizontal_valid_word(self):
        game = ScrabbleGame(1)
        game.dictionary = Dictionary('dictionaries/dictionary.txt')
        palabra = [Tile('C', 3), Tile('A', 1), Tile('S', 1), Tile('A', 1)]
        fila_inicio, columna_inicio = 7, 7
        game.place_horizontal(palabra, fila_inicio, columna_inicio)

        for col, tile in enumerate(palabra):
            square = game.board.grid[fila_inicio][columna_inicio + col]
            self.assertEqual(square.letter, tile)


    def test_place_horizontal_word_does_not_fit(self):
        palabra = [Tile('A', 1), Tile('B', 3), Tile('C', 1)]  
        fila_inicio, columna_inicio = 7, 13 
        with self.assertRaises(WordNotValid):
            self.game.place_horizontal(palabra, fila_inicio, columna_inicio)

    def test_place_horizontal_word_interferes_with_another(self):
        game = ScrabbleGame(1)
        game.dictionary = Dictionary('dictionaries/dictionary.txt')

        gato = [Tile('G', 2), Tile('A', 1), Tile('T', 1), Tile('O', 1)]
        fila_inicio, columna_inicio = 7, 7
        game.place_horizontal(gato, fila_inicio, columna_inicio)

        palabra = [Tile('P', 3), Tile('E', 1), Tile('R', 1), Tile('R', 1), Tile('O', 1)]
        try:
            game.place_horizontal(palabra, fila_inicio, columna_inicio + 2)
            self.fail("The word should interfere with 'GATO'.")
        except WordNotValid:
            pass

    def test_place_vertical_valid_word(self):
        palabra = [Tile('P', 3), Tile('E', 1), Tile('R', 1), Tile('R', 1), Tile('O', 1)]
        fila_inicio, columna_inicio = 7, 7
        self.assertTrue(self.game.place_vertical(palabra, fila_inicio, columna_inicio))
        for fila, tile in enumerate(palabra):
            self.assertEqual(self.board.grid[fila_inicio + fila][columna_inicio].letter, tile)

    def test_place_vertical_word_does_not_fit(self):
        palabra = [Tile('A', 1), Tile('B', 3), Tile('C', 1)]  
        fila_inicio, columna_inicio = 13, 7  
        with self.assertRaises(WordNotValid):
            self.game.place_vertical(palabra, fila_inicio, columna_inicio)

    def test_place_vertical_word_interferes_with_another(self):
        gato = [Tile('G', 2), Tile('A', 1), Tile('T', 1), Tile('O', 1)]
        fila_inicio, columna_inicio = 7, 7
        self.assertTrue(self.game.place_vertical(gato, fila_inicio, columna_inicio))

        palabra = [Tile('P', 3), Tile('E', 1), Tile('R', 1), Tile('R', 1), Tile('O', 1)]  
        with self.assertRaises(WordNotValid):
            self.game.place_vertical(palabra, fila_inicio + 2, columna_inicio)

    def test_get_scores(self):
        game = ScrabbleGame(1)
        game.players[0].set_name("Juanma")
        self.assertEqual(game.get_scores(), {'Juanma': 0})
    

class TestTiles(unittest.TestCase):
    def test_tile(self):
        tile = Tile('A', 1)
        self.assertEqual(tile.letter, 'A')
        self.assertEqual(tile.value, 1)

    def test_tile_repr(self):
        tile = Tile('A', 1)
        expected_repr = "Tile(letter='A', value=1)"
        self.assertEqual(repr(tile), expected_repr)

    def test_eq_same_objects(self):
        tile = Tile('A', 1)
        self.assertTrue(tile == tile)

    def test_eq_different_objects(self):
        tile1 = Tile('A', 1)
        tile2 = Tile('A', 1)

        self.assertTrue(tile1 == tile2)
        self.assertTrue(tile2 == tile1)

    def test_neq_different_objects(self):
        tile1 = Tile('A', 1)
        tile2 = Tile('B', 2)

        self.assertTrue(tile1 != tile2)
        self.assertTrue(tile2 != tile1)

    def test_eq_invalid_comparison(self):
        tile = Tile('A', 1)
        other_object = 'Not a Tile object'

        self.assertFalse(tile == other_object)
        self.assertFalse(other_object == tile)

    def test_get_tile(self):
        tile = Tile('A', 1)
        self.assertEqual(tile.letter, tile.get_letter())
    
    def test_tile_value(self):
        tile = Tile('Z', 10)  
        self.assertEqual(tile.letter, 'Z')
        self.assertEqual(tile.value, 10)

class TestBagTiles(unittest.TestCase):
    @patch('random.shuffle')
    def test_bag_tiles(self, patch_shuffle):
        bag = Tilebag()
        self.assertEqual(
            len(bag.tiles),
            sum(quantity for _, (_, quantity) in LETTER_COUNT.items()),  
        )
        self.assertEqual(
            patch_shuffle.call_count,
            1,
        )
        self.assertEqual(
            patch_shuffle.call_args[0][0],
            bag.tiles,
        )

    def test_take(self):
        bag = Tilebag()
        initial_tile_count = len(bag.tiles)
        tiles = bag.take(2)
        self.assertEqual(
            len(bag.tiles),
            initial_tile_count - 2,
        )
        self.assertEqual(
            len(tiles),
            2,
        )

    def test_put(self):
        bag = Tilebag()
        initial_tile_count = len(bag.tiles)
        put_tiles = [Tile('Z', 1), Tile('Y', 1)]
        bag.put(put_tiles)
        self.assertEqual(
            len(bag.tiles),
            initial_tile_count + len(put_tiles),
        )

    def test_take_too_many(self):
        bag = Tilebag()
        with self.assertRaises(DrawingMoreThanAvailable):
            bag.take(1000000000)
        
    def test_bag_tiles_shuffled(self):
        bag = Tilebag()
        tile_counts_before = [tile.get_value() for tile in bag.tiles]
        bag_tiles_shuffled = Tilebag()  
        tile_counts_after = [tile.get_value() for tile in bag_tiles_shuffled.tiles]
        self.assertNotEqual(tile_counts_before, tile_counts_after)

    def test_take_too_many(self):
        bag = Tilebag()
        initial_tile_count = len(bag.tiles)
        with self.assertRaises(DrawingMoreThanAvailable):
            bag.take(initial_tile_count + 1)

class TestRack(unittest.TestCase):
    def test_rack_initialization(self):
        bag = Tilebag()
        rack = Rack(bag)
        self.assertEqual(len(rack.rack), 7)

    def test_rack_add_to_rack(self):
        bag = Tilebag()
        rack = Rack(bag)
        initial_rack_length = len(rack.rack)
        rack.add_to_rack()
        self.assertEqual(len(rack.rack), initial_rack_length + 1) 
    
    def test_rack_remove_from_rack(self):
        bag = Tilebag()
        rack = Rack(bag)
        initial_rack_length = len(rack.rack)
        tile = rack.rack[0]
        rack.remove_from_rack(tile)
        self.assertEqual(len(rack.rack), initial_rack_length - 1) 

    def test_rack_replenish_rack(self):
        pass
 
class TestBoardMethods(unittest.TestCase):
    def test_board_creation(self):
        board = Board(10, 10)
        self.assertEqual(len(board.grid), 10)
        self.assertEqual(len(board.grid[0]), 10)

    def test_place_tile(self):
        board = Board(5, 5)
        tile = Tile("X", 8)
        board.place_tile(tile, 2, 2)
        self.assertEqual(board.grid[2][2], "X") 

    def test_place_tile_invalid_position(self):
        board = Board(5, 5)
        tile = Tile("X", 8)
        result = board.place_tile(tile, 4, 4) 
        self.assertTrue(result)  
        self.assertEqual(board.grid[4][4], "X")
    
    def test_place_tile_invalid_position(self):
        board = Board(5, 5)
        tile = Tile("X", 8)
        result = board.place_tile(tile, 5, 5)  
        self.assertFalse(result)               

    def test_place_tile_invalid_position2(self):
        board = Board(5, 5)  
        tile = Tile("X", 8)
        result = board.place_tile(tile, 5, 5)
        self.assertFalse(result)
    
    def test_board_place_tile_invalid_position(self):
        board = Board(15, 15)
        tile = Tile("X", 1)
        result = board.place_tile(tile, 15, 15)
        self.assertFalse(result)
        self.assertNotEqual(board.grid[7][7], "X")

    def test_get_square_valid_position(self):
        board = Board(15, 15)
        tile = Tile('X', 1)
        row, col = 7, 7
        board.place_tile(tile, row, col)

        square = board.get_square(row, col)
        if isinstance(square, Square):
            self.assertEqual(square.letter, tile)
        else:
            self.assertIsNone(square)  

    def test_get_square_invalid_position(self):
        board = Board(15, 15)
        tile = Tile('X', 1)
        row, col = 16, 16  
        board.place_tile(tile, row, col)

        square = board.get_square(row, col)
        self.assertIsNone(square)


class TestSquare(unittest.TestCase):
    def test_empty_square(self):
        square = Square()
        self.assertEqual(square.multiplier, 1)
        self.assertEqual(square.letter, None)

    def test_square_letter(self):
        tile = Tile('A', 1)
        square = Square(letter=tile)
        self.assertEqual(square.letter, tile)

    def test_square_multiplier(self):
        square = Square(multiplier=2)
        self.assertEqual(square.multiplier, 2)

    def test_no_multiplier(self):
        square = Square()
        self.assertFalse(square.has_multiplier())

    def test_has_multiplier(self):
        square = Square(multiplier=2)
        self.assertTrue(square.has_multiplier())

    def test_no_letter(self):
        square = Square()
        self.assertFalse(square.has_multiplier())

    def test_has_letter(self):
        square = Square(letter=Tile('A', 1))
        self.assertTrue(square.has_letter())

    def test_insert_letter_full(self):
        square = Square(letter=Tile('A', 1))
        square.insert_letter(Tile('B', 1))
        self.assertEqual(square, square)

    def test_insert_letter_empty(self):
        square = Square()
        square.insert_letter((Tile('A', 1)))
        self.assertEqual(square.letter.letter, 'A')
    
    def test_square_insert_letter_empty(self):
        square = Square()
        tile = Tile('A', 1)
        square.insert_letter(tile)
        self.assertEqual(square.letter, tile)  

    def test_square_insert_letter_occupied(self):
        square = Square(letter=Tile('A', 1))
        tile = Tile('B', 1)
        square.insert_letter(tile)
        self.assertEqual(square.letter, Tile('A', 1)) 
    
class TestPlayer(unittest.TestCase):
    def test_player(self):
        player = Player()
        self.assertEqual(player.score, 0)
        self.assertEqual(len(player.tiles), 0)

    def test_player_score(self):
        player = Player()
        player.increase_score(2)
        self.assertEqual(player.score, 2)

    def test_player_score_many(self):
        player = Player()
        player.increase_score(2)
        player.increase_score(2)
        self.assertEqual(player.score, 4)

    def test_player_draw(self):
        player = Player()
        bag = Tilebag()
        player.draw_tiles(bag, 2)
        self.assertEqual(len(player.tiles), 2)

    def test_player_exchange(self):
        player = Player()
        bag = Tilebag()
        player.draw_tiles(bag, 2)
        tile = player.tiles[0]
        player.exchange_tile(player.tiles[0], bag)
        self.assertFalse(tile == player.tiles[0])
    
    def test_set_name(self):
        player = Player()
        player.set_name('Juanma')
        self.assertEqual(player.get_name(), 'Juanma')

    def test_get_score(self):
        player = Player()
        player.increase_score(2)
        self.assertEqual(player.get_score(), 2)

    def test_check_word_validity_valid_word(self):
        game = ScrabbleGame(1)
        game.dictionary = Dictionary('dictionaries/dictionary.txt')
        valid_word = [Tile('C', 1), Tile('A', 1), Tile('S', 1), Tile('A', 1)]
        self.assertTrue(game.check_word_validity(valid_word))

    def test_check_word_validity_invalid_word(self):
        game = ScrabbleGame(1)
        game.dictionary = Dictionary('dictionaries/dictionary.txt')
        invalid_word = [Tile('W', 1), Tile('O', 1), Tile('R', 1), Tile('D', 1)]
        self.assertFalse(game.check_word_validity(invalid_word))

    def test_has_tile_empty_square(self):
        square = Square()
        self.assertFalse(square.has_tile())

    def test_has_tile_occupied_square(self):
        tile = Tile('A', 1)
        square = Square(letter=tile)
        self.assertTrue(square.has_tile())

    def test_put_tile_empty_square(self):
        square = Square()
        tile = Tile('B', 2)
        square.put_tile(tile)
        self.assertEqual(square.letter, tile)

    def test_put_tile_occupied_square(self):
        tile1 = Tile('A', 1)
        tile2 = Tile('B', 2)
        square = Square(letter=tile1)
        square.put_tile(tile2)
        self.assertEqual(square.letter, tile1) 

class TestDictionary(unittest.TestCase):
    def test_dictionary(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertTrue(dictionary.has_word('arbol'))
    
    def test_dictionary(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertTrue(dictionary.has_word('arbol'))
        
    def test_dictionary(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertTrue(dictionary.has_word('casa'))

    def test_word_false(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertFalse(dictionary.has_word('willkommen'))
    
    def test_word_false(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertFalse(dictionary.has_word('volkswagen'))

class TestWord(unittest.TestCase):
    def setUp(self):
        self.board = Board(15, 15)
        self.player = Player()
        self.tilebag = Tilebag()

    def test_creation_of_word(self):
        word = Word("HOLA", (7, 7), self.player, "horizontal", self.board)
        self.assertEqual(word.word, "HOLA")
        self.assertEqual(word.location, (7, 7))
        self.assertEqual(word.player, self.player)
        self.assertEqual(word.direction, "horizontal")
        self.assertEqual(word.board, self.board)

    def test_set_word(self):
        word = Word("HOLA", (7, 7), self.player, "horizontal", self.board)
        word.word = "CASA"
        self.assertEqual(word.word, "CASA")

    def test_set_location(self):
        word = Word("HOLA", (7, 7), self.player, "horizontal", self.board)
        word.location = (5, 5)
        self.assertEqual(word.location, (5, 5))

    def test_set_direction(self):
        word = Word("HOLA", (7, 7), self.player, "horizontal", self.board)
        word.direction = "vertical"
        self.assertEqual(word.direction, "vertical")



if __name__ == '__main__':
    unittest.main()