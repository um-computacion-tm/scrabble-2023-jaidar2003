from game.tilebag import Tilebag

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