from room import Room
from OpenGL.GL import *
from math import cos, sin, atan2
from math import radians as rad


class Bullet(Room):

    x = 150
    y = 40
    z = 20

    grid = [
        [x, 0, z],
        [x, 0, -z],
        [-x, 0, -z],
        [-x, 0, z],
        [x, y, z],
        [x, y, -z],
        [-x, y, -z],
        [-x, y, z]

    ]

    bedges = (
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

        self.bvertices = Bullet.grid
        self.bedges = Bullet.edges
        self.thetax = 0
        self.thetay = 0
        self.bvel = 80
        self.pos = [0, 0, 0]

        Room.__init__(self)

    def drawbullet(self):
        glLineWidth(3)
        glBegin(GL_LINES)
        for edge in self.bedges:
            glColor3f(1, 0, 0)

            for vertex in edge:
                glVertex3fv(self.bvertices[vertex])

        glEnd()

    def bmove(self, x, y, z):

        self.bvertices = list(map(lambda vert: (vert[0] + x,
                                                vert[1] + y,
                                                vert[2] + z), self.bvertices))
        self.pos[0] += x
        self.pos[1] += y
        self.pos[2] += z

    def brotate(self, thetax, thetay):
        self.thetax = thetax
        self.thetay = thetay
        self.bvertices = list(map(lambda vert: (vert[2]*cos(rad(thetax)) - vert[0]*sin(rad(thetax)),
                                                vert[0]*sin(rad(thetay)) + vert[1]*cos(rad(thetay)),
                                                vert[0]*cos(rad(thetax)) + vert[2]*sin(rad(thetax))), self.bvertices))

    def checkpyramid(self, plist):

        pass
