from game.tile import Tile

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