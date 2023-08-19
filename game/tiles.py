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

        self.tiles = []
        for letter, value in letter_scores_es:
            count = 0
            if letter == 'A':
                count = 12
            elif letter == 'E':
                count = 12
            elif letter == 'O':
                count = 9
            elif letter == 'I':
                count = 6
            elif letter == 'S':
                count = 6
            elif letter == 'N':
                count = 5
            elif letter == 'L':
                count = 4
            elif letter == 'R':
                count = 5
            elif letter == 'U':
                count = 5
            elif letter == 'T':
                count = 4
            elif letter == 'D':
                count = 5
            elif letter == 'G':
                count = 2
            elif letter == 'C':
                count = 4
            elif letter == 'B':
                count = 2
            elif letter == 'M':
                count = 2
            elif letter == 'P':
                count = 2
            elif letter == 'H':
                count = 2
            elif letter == 'F':
                count = 1
            elif letter == 'V':
                count = 1
            elif letter == 'Y':
                count = 1
            elif letter == 'CH':
                count = 1
            elif letter == 'Q':
                count = 1
            elif letter == 'J':
                count = 1
            elif letter == 'LL':
                count = 1
            elif letter == 'Ñ':
                count = 1
            elif letter == 'RR':
                count = 1
            elif letter == 'X':
                count = 1
            elif letter == 'Z':
                count = 1

            for _ in range(count):
                self.tiles.append(Tile(letter, value))

        random.shuffle(self.tiles)

        self.valid_letters = [letter for letter, _ in letter_scores_es]
    
    def get_letter_count(self, letter):
        count = 0
        for tile in self.tiles:
            if tile.letter == letter:
                count += 1
        return count
    
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