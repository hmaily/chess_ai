
class Move:
    def __init__(self, initial, final):
        # Instantiate initial and final squares 
        self.initial = initial
        self.final = final

    # Special method
    # Tell python when a move is equal to another move 
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final