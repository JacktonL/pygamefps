from room import Room


class Bullet(Room):

    def __init__(self):

        self.vertices = [[]]

        Room.__init__(self)

    def drawbullet(self, x, y, z):
        pass
