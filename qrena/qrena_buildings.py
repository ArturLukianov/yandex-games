from qrena_constants import *
from qrena_base import *

class Tile:
    def __init__(self, texture, mpos):
        self.t = texture
        self.mposes = mpos

    def draw(self, screen, queue, x, y):
        def _():
            screen.blit(self.t, (x, y))
        if queue is not None:
            queue.append((_, (x, y)))
        else:
            _()

    def collides(self, mpos, pos):
        for npos in self.mposes:
##            if (mpos[0] + npos[0] <= pos[0] - 5 <= mpos[0] + npos[0] + npos[2] or mpos[0] + npos[0] <= pos[0] + 5 <= mpos[0] + npos[0] + npos[2]):
##                if(mpos[1] + npos[1] <= pos[1] - 5 <= mpos[1] + npos[1] + npos[3] or mpos[1] + npos[1] <= pos[1] + 5 <= mpos[1] + npos[1] + npos[3]):
##                    return True
            x = mpos[0] + npos[0]
            y = mpos[1] + npos[1]
            w = npos[2]
            h = npos[3]
            x2 = pos[0] - 5
            y2 = pos[1] - 5
            w2 = 10
            h2 = 10
            if x + w > x2 and x2 + w2 > x:
                if y + h > y2 and y2 + h2 > y:
                    return True

class Building:
    def __init__(self, x, y, background_map, wall_map, background, wall, door):
        self.x = x
        self.y = y
        self.b_map = background_map
        self.w_map = wall_map
        self.b = background
        self.w = wall
        self.d = door

    def draw_background(self, screen, queue, relative_to=(0,0)):
        for y in range(len(self.b)):
            for x in range(len(self.b[y])):
                if self.b[y][x] >= 0:
                    rx, ry = get_relative_position((self.x + x * 28 + 14, self.y + y * 28), relative_to)
                    self.b_map[self.b[y][x]].draw(screen, queue, rx, ry)

    def draw_wall(self, screen, queue, relative_to=(0,0)):
        for y in range(len(self.w)):
            for x in range(len(self.w[y])):
                if self.w[y][x] >= 0:
                    rx, ry = get_relative_position((self.x + x * 28 + 14, self.y + y * 28), relative_to)
                    self.w_map[self.w[y][x]].draw(screen, queue, rx, ry)
                        

    def draw(self, screen, queue, queue2, relative_to=(0,0)):
        self.draw_background(screen, queue2, relative_to)
        self.draw_wall(screen, queue, relative_to)

    def collides(self, pos):
        for y in range(len(self.w)):
            for x in range(len(self.w[y])):
                if self.w[y][x] >= 0:
                    tx = self.x + x * 28
                    ty = self.y + y * 28
                    if self.w_map[self.w[y][x]].collides((tx, ty), pos):
                        return True
