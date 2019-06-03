from room import Room
import numpy as np
import random
from OpenGL.GL import *


class Pyramid(Room):

    def __init__(self):
        Room.__init__(self)

        self.pvertices = [
            [Room.x, 0, Room.z],
            [Room.x, 0, -Room.z],
            [-Room.x, 0, -Room.z],
            [-Room.x, 0, Room.z],
            [0, Room.y, 0]
        ]

        self.pedges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4)

        )

        self.psurfaces = (
            (1, 0, 4),
            (2, 1, 4),
            (3, 2, 4),
            (3, 0, 4)
        )

        self.pvertices = np.array(np.multiply(np.array(self.pvertices), self.mul))
        Pyramid.randtransform(self)

    def randtransform(self):
        fac = 1 / (Room.num-1)

        self.pvertices = np.multiply(self.pvertices, (fac, fac*4, fac))

        randposx = random.choice(Room.mesh[1][1:Room.num-1])[0]*self.mul + self.mulx*fac
        randposz = random.choice(Room.mesh[0][1:Room.num-1])[2]*self.mul + self.mulz*fac
        print(randposx, randposz)

        self.pvertices = list(map(lambda vert: (vert[0] + randposx, vert[1],
                                                vert[2] + randposz), self.pvertices))

    def drawpyramid(self):
        glBegin(GL_QUADS)
        glColor3fv((1, 1, 1))
        for surface in self.psurfaces:
            for vertex in surface:
                glVertex3fv(self.pvertices[vertex])
        glEnd()

        glLineWidth(3)
        glBegin(GL_LINES)
        for edge in self.pedges:
            for vertex in edge:
                glVertex3fv(self.pvertices[vertex])

        glEnd()



