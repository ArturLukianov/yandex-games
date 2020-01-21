import pygame as pg
import random

pg.init()

h = int(input())
w = int(input())
fh = h
fw = w

screen = pg.display.set_mode((h * 20, w * 20))

field = []

for i in range(h):
    b = []
    for j in range(w):
        b.append(2)
    field.append(b)

loop = 1
clicked = 0
ed = 2
tsi = 20

def draw_tile(i, j):
    if field[i][j] == 1:
        if i > 0 and field[i - 1][j] == 1:
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i, tsi * j + 4), (6, 2)), 0)
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i, tsi * j + 14), (6, 2)), 0)
        else:
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 4, tsi * j + 6), (2, 8)), 0)
        if j > 0 and field[i][j - 1] == 1:
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 4, tsi * j), (2, 6)), 0)
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 14, tsi * j), (2, 6)), 0)
        else:
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 6, tsi * j + 4), (8, 2)), 0)
        if i < fh - 1 and field[i + 1][j] == 1:
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 14, tsi * j + 4), (6, 2)), 0)
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 14, tsi * j + 14), (6, 2)), 0)
        else:
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 14, tsi * j + 6), (2, 8)), 0)
        if j < fw - 1 and field[i][j + 1] == 1:
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 4, tsi * j + 14), (2, 6)), 0)
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 14, tsi * j + 14), (2, 6)), 0)
        else:
            pg.draw.rect(screen, (0, 0, 255),
                            ((tsi * i + 6, tsi * j + 14), (8, 2)), 0)
    if field[i][j] == 2:
        pg.draw.rect(screen, (255, 255, 255),
                        ((tsi * i + 8, tsi * j + 8), (4, 4)), 0)
        


while loop:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            loop = 0
        if ev.type == pg.MOUSEBUTTONDOWN:
            clicked = 1
        if ev.type == pg.MOUSEBUTTONUP:
            clicked = 0
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_s:
                print(field)
            if ev.key == pg.K_q:
                ed = 1
            if ev.key == pg.K_w:
                ed = 2
    if clicked:
        field[pg.mouse.get_pos()[0] // 20][pg.mouse.get_pos()[1] // 20] = ed
    screen.fill((0,0,0))
    for i in range(h):
        for j in range(w):
            draw_tile(i,j)
    pg.display.update()

pg.quit()
