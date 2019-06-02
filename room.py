import numpy as np
from OpenGL.GL import *
from math import atan2


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

    def draw(self):
        x = 0
        glLineWidth(5)
        glBegin(GL_LINES)
        for edge in self.edges:
            if x < 3:
                glColor3f(self.colors[x][0], self.colors[x][1], self.colors[x][2])
            else:
                glColor3f(1, 1, 1)
            for vertex in edge:
                glVertex3fv(self.grid[vertex])
            x += 1

        glEnd()

    def rotateworld(self, anglex, angley):
        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * np.mat(buffer[:3, :3]) * np.mat(buffer[3, :3]).T).reshape(3, 1)
        glTranslate(c[0], c[1], c[2])
        m = buffer.flatten()
        glRotate(anglex, m[1], m[5], m[9])  # [1]
        glRotate(angley, m[0], m[4], m[8])  # [1]
        glRotate(atan2(-m[4], m[5]) * 57.29577, m[2], m[6], m[10])
        glTranslate(-c[0], -c[1], -c[2])