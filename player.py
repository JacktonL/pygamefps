from room import Room
from math import sqrt
from OpenGL.GL import *
from OpenGL.GLU import *


class Player(Room):

    def __init__(self, display=(1, 1), fov=90):
        self.buffer = 2
        self.starty = 200
        self.pos = [0, self.starty, 0]
        self.jumpvel = 20
        self.relvel = self.jumpvel
        gluPerspective(fov, (display[0] / display[1]), 0.1, 5000)
        glTranslatef(0, -self.starty, 0)
        Room.__init__(self)

    def gravity(self, mul):
        glTranslatef(0, self.jumpvel*mul, 0)
        self.pos[1] -= self.jumpvel*mul

    def checkwall(self):

        k = [False, False]
        if -self.mulx < self.pos[0] < self.mulx:
            k[0] = True
        if -self.mulz < self.pos[2] < self.mulz:
            k[1] = True

        return k