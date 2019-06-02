import pygame
from pygame.locals import *
from OpenGL.GL import *
from room import Room
from player import Player


class Game:
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

    def __init__(self, starty, mul=1):
        self.jumpvel = 3
        self.relvel = self. jumpvel
        self.starty = starty
        self.pos = [0, starty, 0]
        self.mul = mul
        self.colors = Game.colors
        self.edges = Game.edges
        self.grid = list(numpy.multiply(numpy.array(Game.grid), mul))
        self.cont = self.grid

    def draw(self):
        x = 0
        glLineWidth(5)
        glBegin(GL_LINES)
        for edge in self.edges:
            glColor3f(self.colors[x][0], self.colors[x][1], self.colors[x][2])
            for vertex in edge:
                glVertex3fv(self.grid[vertex])
            x += 1
        glEnd()

    def move(self, x, y, z):
        self.grid = list(map(lambda vert: (vert[0] + x, vert[1] + y, vert[2] + z), self.grid))

    def translate(self, x, y, z, const):
        return list(map(lambda vert: (vert[0] + x, vert[1] + y, vert[2] + z), const))

    def rotateworld(self, anglex, angley):
        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * numpy.mat(buffer[:3, :3]) * numpy.mat(buffer[3, :3]).T).reshape(3, 1)
        glTranslate(c[0], c[1], c[2])
        m = buffer.flatten()
        glRotate(anglex, m[1], m[5], m[9])  # [1]
        glRotate(angley, m[0], m[4], m[8])  # [1]
        glRotate(atan2(-m[4], m[5]) * 57.29577, m[2], m[6], m[10])
        glTranslate(-c[0], -c[1], -c[2])

    def checkwall(self):

        k = [False, False]
        if -self.mul < self.pos[0] < self.mul:
            k[0] = True
        if -self.mul < self.pos[2] < self.mul:
            k[1] = True
        return k


def main():
    pygame.init()
    size = 500
    display = (size, size)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.event.set_grab(True)
    pygame.mouse.set_pos(size / 2, size / 2)
    room = Room()
    player = Player()

    clock = pygame.time.Clock()
    exit = True
    wall = True
    sens = 0.25
    vel = 3.5

    while exit:
        clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        mousepos = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        fwd = -vel * (keys[K_w]-keys[K_s])
        strafe = vel * (keys[K_a]-keys[K_d])
        if abs(fwd) or abs(strafe):
            m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
            if player.checkwall()[0] and player.checkwall()[1]:
                glTranslatef(fwd*m[2], 0, fwd*m[10])
                glTranslatef(strafe*m[0], 0, strafe*m[8])
                player.pos[0] += fwd*m[2] + strafe*m[0]
                player.pos[2] += fwd*m[10] + strafe*m[8]
            else:
                if not player.checkwall()[0]:
                    glTranslatef(-player.pos[0]*0.001, 0, fwd * m[10])
                    glTranslatef(-player.pos[0]*0.001, 0, strafe * m[8])
                    player.pos[0] += 2*(-player.pos[0]*0.001)
                    player.pos[2] += fwd * m[10] + strafe * m[8]

                elif not player.checkwall()[1]:
                    glTranslatef(fwd * m[2], 0, -player.pos[2]*0.001)
                    glTranslatef(strafe * m[0], 0, -player.pos[2]*0.001)
                    player.pos[0] += fwd * m[2] + strafe * m[0]
                    player.pos[2] += 2*(-player.pos[2]*0.001)

        if keys[pygame.K_ESCAPE]:
            exit = False
        if player.pos[1] == player.starty:
            if keys[pygame.K_SPACE]:
                glTranslatef(0, -0.1, 0)
                player.pos[1] += 0.1

        if player.pos[1] > player.starty:
            player.gravity()

        if wall:
            room.rotateworld(mouse_dx*sens, mouse_dy*sens)
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
        print(player.pos)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        room.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
    quit()
