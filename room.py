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

    mesh = [list(zip([1 for a in range(10)], [0 for b in range(10)], np.linspace(-1, 1, 10))),
            list(zip(np.linspace(-1, 1, 10), [0 for c in range(10)], [-1 for d in range(10)])),
            list(zip([-1 for e in range(10)], [0 for f in range(10)], np.linspace(-1, 1, 10))),
            list(zip(np.linspace(-1, 1, 10), [0 for g in range(10)], [1 for h in range(10)])),
            list(zip([1 for i in range(10)], [1 for j in range(10)], np.linspace(-1, 1, 10))),
            list(zip(np.linspace(-1, 1, 10), [1 for k in range(10)], [-1 for l in range(10)])),
            list(zip([-1 for m in range(10)], [1 for n in range(10)], np.linspace(-1, 1, 10))),
            list(zip(np.linspace(-1, 1, 10), [1 for o in range(10)], [1 for p in range(10)])),
            list(zip([1 for q in range(10)], np.linspace(0, 1, 10), [1 for r in range(10)])),
            list(zip([1 for s in range(10)], np.linspace(0, 1, 10), [-1 for t in range(10)])),
            list(zip([-1 for u in range(10)], np.linspace(0, 1, 10), [-1 for v in range(10)])),
            list(zip([-1 for w in range(10)], np.linspace(0, 1, 10), [1 for x in range(10)]))]

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
        self.mesh = list(np.multiply(np.array(Room.mesh), self.mul))
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

    def drawroom(self):
        glLineWidth(5)
        glBegin(GL_LINES)
        Room.surface(self, 0, 2, (0, 0, 1))
        Room.surface(self, 1, 3, (0, 0, 1))
        Room.surface(self, 0, 4, (0, 1, 0))
        Room.surface(self, 1, 5, (0, 1, 0))
        Room.surface(self, 2, 6, (0, 1, 0))
        Room.surface(self, 3, 7, (0, 1, 0))
        Room.surface(self, 4, 6, (1, 0, 0))
        Room.surface(self, 5, 7, (1, 0, 0))
        Room.surface(self, 8, 9, (0, 1, 0))
        Room.surface(self, 9, 10, (0, 1, 0))
        Room.surface(self, 10, 11, (0, 1, 0))
        Room.surface(self, 11, 8, (0, 1, 0))



        glEnd()

    def surface(self, e1, e2, color):
        glColor3fv(color)
        for i in range(10):
            for j in (e1, e2):
                glVertex3fv(self.mesh[j][i])

    def rotateworld(self, anglex, angley):
        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * np.mat(buffer[:3, :3]) * np.mat(buffer[3, :3]).T).reshape(3, 1)
        glTranslate(c[0], c[1], c[2])
        m = buffer.flatten()
        glRotate(anglex, m[1], m[5], m[9])  # [1]
        glRotate(angley, m[0], m[4], m[8])  # [1]
        glRotate(atan2(-m[4], m[5]) * 57.29577, m[2], m[6], m[10])
        glTranslate(-c[0], -c[1], -c[2])