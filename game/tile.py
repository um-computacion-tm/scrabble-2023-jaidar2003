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