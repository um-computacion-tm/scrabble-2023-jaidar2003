import random

class Tile:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

class BagTiles:
    def __init__(self):
        letter_scores_es = [
            ('A', 1),
            ('B', 3), 
            ('C', 3),
            ('CH', 5),
            ('D', 2), 
            ('E', 1), 
            ('F', 4), 
            ('G', 2),
            ('H', 4), 
            ('I', 1), 
            ('J', 8), 
            ('L', 1),
            ('LL', 8),
            ('M', 3), 
            ('N', 1),
            ('Ñ', 8),
            ('O', 1),
            ('P', 3), 
            ('Q', 5), 
            ('R', 1),
            ('RR', 8), 
            ('S', 1),
            ('T', 1),
            ('U', 1),
            ('V', 4),
            ('X', 8), 
            ('Y', 4),
            ('Z', 10),
            (' ', 0),
            (' ', 0),
        ]
        
        self.tiles = [Tile(letter, score) for letter, score in letter_scores_es]
        random.shuffle(self.tiles)

        self.valid_letters = [letter for letter, _ in letter_scores_es]
    
    def take(self, count):
        if count > len(self.tiles):
            count = len(self.tiles)
        tiles = []
        for _ in range(count):
            tiles.append(self.tiles.pop())
        return tiles

    def put(self, tiles):
        self.tiles.extend(tiles)
        random.shuffle(self.tiles)


if __name__ == '__main__':
    bag = BagTiles()