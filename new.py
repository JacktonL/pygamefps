import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from math import radians as rad
from math import sin, cos, sqrt


class Game:
    grid = [
        [0.5, 0, 0.5],
        [0.5, 0, -0.5],
        [-0.5, 0, -0.5],
        [-0.5, 0, 0.5],
        [0.5, 1, 0.5],
        [0.5, 1, -0.5],
        [-0.5, 1, -0.5],
        [-0.5, 1, 0.5]

    ]

    colors = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 1)
    ]

    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (1, 5),
        (1, 2),
        (2, 6),
        (2, 3),
        (3, 7),
        (6, 5),
        (4, 5),
        (7, 4),
        (6, 7)
    )

    def __init__(self, mul=1):
        self.mul = mul
        self.x = 0
        self.colors = Game.colors
        self.edges = Game.edges
        self.grid = list(numpy.multiply(numpy.array(Game.grid), mul))
        self.cont = self.grid

    def draw(self):
        glLineWidth(5)
        glBegin(GL_LINES)
        for edge in self.edges:
            glColor3f(self.colors[self.x][0], self.colors[self.x][1], self.colors[self.x][2])
            for vertex in edge:
                glVertex3fv(self.grid[vertex])
            self.x += 1
            if self.x == 4:
                self.x = 0
        glEnd()

    def move(self, x, y, z):
        self.grid = list(map(lambda vert: (vert[0] + x, vert[1] + y, vert[2] + z), self.grid))

    def translate(self, x, y, z, const):
        return list(map(lambda vert: (vert[0] + x, vert[1] + y, vert[2] + z), const))

    def rotateworldy(self, angle):
        self.grid = list(map(lambda vert: (vert[0] * cos(rad(angle)) - vert[2] * sin(rad(angle)),
                                           vert[1],
                                           vert[2] * cos(rad(angle)) + vert[0] * sin(rad(angle))), self.grid))

    def rotateworldx(self, angle):
        self.grid = list(map(lambda vert: (vert[0],
                                           vert[1]*cos(rad(angle)) - vert[2]*sin(rad(angle)),
                                           vert[2] * cos(rad(angle)) + vert[1] * sin(rad(angle))), self.grid))

    def rotateworldz(self, angle):
        self.grid = list(map(lambda vert: (vert[0]*cos(rad(angle)) - vert[1]*sin(rad(angle)),
                                           vert[1] * cos(rad(angle)) + vert[0] * sin(rad(angle)),
                                           vert[2]), self.grid))


def main():
    pygame.init()
    size = 500
    display = (size, size)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.event.set_grab(True)
    pygame.mouse.set_pos(size/2, size/2)

    gluPerspective(70, (display[0]/display[1]), 0.1, 50)
    glTranslatef(0, 0, 0)
    p = Game(30)

    vel = 0.1
    clock = pygame.time.Clock()
    c = 0
    exit = True
    wall = True
    first = False
    theta = 0
    while exit:
        clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        mouserel = pygame.mouse.get_rel()
        mousepos = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            exit = False
        if wall:
            if mouserel[0] != 0:
                p.rotateworldy(-mouserel[0]*0.45)
                theta += mouserel[0]*0.45
            if mousepos[1] != 0:
                p.rotateworldx(-mouserel[1]*0.45*sin(rad(theta)))
                p.rotateworldz(-mouserel[1]*0.45*cos(rad(theta)))
        wall = True
        if mousepos[0] <= 1:
            pygame.mouse.set_pos(size, mousepos[1])
            wall = False
        if mousepos[0] >= size-1:
            pygame.mouse.set_pos(0, mousepos[1])
            wall = False
        if mousepos[1] <= 1:
            pygame.mouse.set_pos(mousepos[0], size)
            wall = False
        if mousepos[1] >= size-1:
            pygame.mouse.set_pos(mousepos[0], 0)
            wall = False
        print(theta)
        # if keys[pygame.K_LEFT]:
        #     p.move(-vel, 0, 0)
        # if keys[pygame.K_RIGHT]:
        #     p.move(vel, 0, 0)
        # if keys[pygame.K_UP]:
        #     p.move(0, vel, 0)
        # if keys[pygame.K_DOWN]:
        #     p.move(0, -vel, 0)
        # if keys[pygame.K_t]:
        #     p.move(0, 0, vel)
        # if keys[pygame.K_g]:
        #       p.move(0, 0, -vel)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        p.draw()
        pygame.display.flip()


main()
pygame.quit()
quit()
