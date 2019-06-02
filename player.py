class Player:

    def __init__(self):
        self.starty = 10
        self.pos = [0, self.starty, 0]
        self.jumpvel = 3
        self.relvel = self.jumpvel