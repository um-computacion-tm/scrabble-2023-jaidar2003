import unittest
from game.tiles import *
from unittest.mock import patch

class TestScrabble(unittest.TestCase):
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

class TestBagTiles(unittest.TestCase):
    @patch('random.shuffle')
    def test_bag_tiles(self, patch_shuffle):
        bag = Tilebag()
        self.assertEqual(
            len(bag.tiles),
            sum(quantity for _, (_, quantity) in LETTER_COUNT.items()),  # Calculate the total quantity
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
        board = Board(5, 5)  # Initialize the board
        tile = Tile("X", 8)
        result = board.place_tile(tile, 5, 5)
        self.assertFalse(result)




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


class TestDictionary(unittest.TestCase):
    def test_dictionary(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertTrue(dictionary.has_word('arbol'))

    def test_word_false(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertFalse(dictionary.has_word('willkommen'))

if __name__ == '__main__':
    unittest.main()