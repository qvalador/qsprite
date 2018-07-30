class PokeCard:
    """represents a generic pokémon card."""

    def __init__(self, name, hp, ptype):
        self.name = name
        self.hp = hp
        self.ptype = ptype
        self.moves = {}
        self.power = None
    
    def attack(self, move, foe):
        """uses move on foe.  easy!"""
        if move in self.moves:
            self.moves[move](foe)
            return True
        else:
            print("Move not found.")
            return False