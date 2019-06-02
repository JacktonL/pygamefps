import pygame
from pygame.locals import *
from OpenGL.GL import *
from room import Room
from player import Player
import numpy as np


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
    c = 0

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
                    if player.pos[0] > player.mul:
                        d = player.pos[0] - player.mul
                        glTranslatef(-d - player.buffer, 0, fwd * m[10])
                        glTranslatef(0, 0, strafe * m[8])
                        player.pos[0] = player.mul - player.buffer
                        player.pos[2] += fwd * m[10] + strafe * m[8]
                    elif player.pos[0] < -player.mul:
                        d = player.pos[0] + player.mul
                        glTranslatef(-d + player.buffer, 0, fwd * m[10])
                        glTranslatef(0, 0, strafe * m[8])
                        player.pos[0] = -player.mul + player.buffer
                        player.pos[2] += fwd * m[10] + strafe * m[8]

                elif not player.checkwall()[1]:
                    if player.pos[2] > player.mul:
                        d = player.pos[2] - player.mul
                        glTranslatef(fwd * m[2], 0, -d-player.buffer)
                        glTranslatef(strafe * m[0], 0, 0)
                        player.pos[0] += fwd * m[2] + strafe * m[0]
                        player.pos[2] = player.mul - player.buffer
                    elif player.pos[2] < -player.mul:
                        d = player.pos[2] + player.mul
                        glTranslatef(fwd * m[2], 0, -d+player.buffer)
                        glTranslatef(strafe * m[0], 0, 0)
                        player.pos[0] += fwd * m[2] + strafe * m[0]
                        player.pos[2] = -player.mul+player.buffer


        if keys[pygame.K_ESCAPE]:
            exit = False
        if player.pos[1] == player.starty:
            if keys[pygame.K_SPACE]:
                glTranslatef(0, 0.1, 0)
                player.pos[1] += 0.1

        if player.pos[1] > player.starty:
            array = np.linspace(-1, 1)
            player.gravity(array[c])
            c += 1
            if c == len(array):
                d = abs(player.pos[1] - player.starty)
                glTranslatef(0, -d, 0)
                player.pos[1] = player.starty
                c = 0
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
