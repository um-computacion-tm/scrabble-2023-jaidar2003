import unittest

from game.tiles import (Tile, BagTiles  )

class TestTile(unittest.TestCase):
    def test_tile_creation(self):
        tile = Tile('A', 1)
        self.assertEqual(tile.letter, 'A')
        self.assertEqual(tile.value, 1)

class TestBagTiles(unittest.TestCase):
    def setUp(self):
        self.bag = BagTiles()

    def test_tile_bag_creation(self):
        self.assertIsInstance(self.bag, BagTiles)

    def test_take_tiles(self):
        tiles_taken = self.bag.take(7)
        self.assertEqual(len(tiles_taken), 7)
        self.assertTrue(all(isinstance(tile, Tile) for tile in tiles_taken))
    
    def test_put_tiles(self):
        initial_tile_count = len(self.bag.tiles)
        tiles_to_put = [Tile('A', 1), Tile('B', 3)]
        self.bag.put(tiles_to_put)
        new_tile_count = len(self.bag.tiles)
        self.assertEqual(new_tile_count, initial_tile_count + len(tiles_to_put))

if __name__ == '__main__':
    unittest.main()