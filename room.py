import numpy as np


class Room:

    grid = [
        [1, 0, 1],
        [1, 0, -1],
        [-1, 0, -1],
        [-1, 0, 1],
        [1, 1, 1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, 1, 1]

    ]

    colors = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1)
    ]

    edges = (
        (1, 2),
        (2, 6),
        (2, 3),
        (0, 1),
        (0, 3),
        (0, 4),
        (1, 5),
        (3, 7),
        (6, 5),
        (4, 5),
        (7, 4),
        (6, 7)
    )

    def __init__(self):
        self.mul = 800
        self.colors = Room.colors
        self.edges = Room.edges
        self.grid = list(np.multiply(np.array(Room.grid), self.mul))
        self.cont = self.grid