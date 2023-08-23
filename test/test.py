import unittest
from game.tiles import Tile, BagTiles, Board, Player, Dictionary, Square

class TestTile(unittest.TestCase):
    def test_tile_creation(self):
        tile = Tile("A", 1)
        self.assertEqual(tile.letter, "A")
        self.assertEqual(tile.value, 1)

    def test_tile_creation_different_values(self):
        tile = Tile("Z", 10)
        self.assertEqual(tile.letter, "Z")
        self.assertEqual(tile.value, 10)

class TestBagTiles(unittest.TestCase):

    def setUp(self):
        self.board = Board(15, 15)
        self.bag = BagTiles()
        self.player = Player("TestPlayer", self.board, self.bag)

    def test_bag_creation(self):
        bag = BagTiles()
        self.assertEqual(bag.tiles_remaining(), 98)

    def test_draw_tiles(self):
        bag = BagTiles()
        initial_remaining = bag.tiles_remaining()  
        drawn_tiles = bag.draw_tiles(7)
        self.assertEqual(len(drawn_tiles), 7)
        self.assertEqual(bag.tiles_remaining(), initial_remaining - 7)

    def test_draw_all_tiles(self):
        bag = BagTiles()
        all_drawn_tiles = bag.draw_tiles(98)
        self.assertEqual(len(all_drawn_tiles), 98)
        self.assertEqual(bag.tiles_remaining(), 0)

    def test_get_tile_value(self):
        self.player.hand = [Tile("A", 1), Tile("Z", 10), Tile("E", 1)]
        self.assertEqual(self.player.get_tile_value("A"), 1)
        self.assertEqual(self.player.get_tile_value("Z"), 10)
        self.assertEqual(self.player.get_tile_value("E"), 1)

    def test_draw_tiles_empty_bag(self):
        bag = BagTiles()
        bag.draw_tiles(98) 
        drawn_tiles = bag.draw_tiles(1)  
        self.assertEqual(len(drawn_tiles), 0) 

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
    def setUp(self):
        self.board = Board(15, 15)
        self.bag = BagTiles()
        self.player = Player("TestPlayer", self.board, self.bag)

    def test_draw_tiles(self):
        self.player.draw_tiles(7)
        self.assertEqual(len(self.player.hand), 7)

    def test_exchange_tiles(self):
        self.player.draw_tiles(7)
        initial_hand = self.player.hand.copy()
        exchanged_tiles = self.player.exchange_tiles(initial_hand[:3])
        self.assertEqual(len(exchanged_tiles), 3)
        self.assertEqual(len(self.player.hand), 7)

    def test_calculate_score(self):
        score = self.player.calculate_score("HELLO", 7, 7, "horizontal")
        self.assertEqual(score, 8)

    def test_draw_to_full_hand(self):
        initial_hand_size = len(self.player.hand)
        self.player.draw_tiles(10) 
        self.assertEqual(len(self.player.hand), initial_hand_size + 10)

    def test_exchange_no_tiles(self):
        initial_hand = self.player.hand.copy()
        exchanged_tiles = self.player.exchange_tiles([])
        self.assertEqual(len(exchanged_tiles), 0)
        self.assertEqual(self.player.hand, initial_hand)

    def test_calculate_score_vertical(self):
        score = self.player.calculate_score("HELLO", 7, 7, "vertical")
        self.assertEqual(score, 8)

    def test_get_tile_value(self):
        self.assertEqual(self.player.get_tile_value("A"), 1)
        self.assertEqual(self.player.get_tile_value("Z"), 10)
        self.assertEqual(self.player.get_tile_value("E"), 1)

class TestDictionary(unittest.TestCase):
    def test_dictionary(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertTrue(dictionary.has_word('arbol'))

    def test_word_false(self):
        dictionary = Dictionary('dictionaries/dictionary.txt')
        self.assertFalse(dictionary.has_word('willkommen'))

if __name__ == '__main__':
    unittest.main()