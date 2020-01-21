import pygame
from math import sqrt

def dist(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return sqrt(x * x + y * y)

def get_abc(p1, p2):
    a = 1
    if p1[1] - p2[1] != 0:
        b = -(p1[0] - p2[0]) / (p1[1] - p2[1])
    else:
        a = 0
        b = 1
    c = -(p1[0] + b * p1[1])
    return a, b, c

def true_coll(p1, p2, o, r):
    a = dist(p1, p2)
    b = dist(p1, o)
    c = dist(p2, o)
    p = (a + b + c) / 2
    s = sqrt(p * (p - a) * (p - b) * (p - c))
    h = s / a * 2
    if h <= r:
        a, b, c = get_abc(p1, p2)
        d = o[0]
        e = o[1]
        aa = b ** 2 + 1
        bb = 2 * (b * d + b * c - e)
        cc = (c + d) ** 2 + e ** 2 - r ** 2
        dd = bb ** 2 - 4 * aa * cc
        print(c, d, e)
        dd = sqrt(dd)
        y1 = (-bb + dd) / (2 * aa)
        y2 = (-bb - dd) / (2 * aa)
        yy1 = y1 >= min(p1[1], p2[1]) and y1 <= max(p1[1], p2[1])
        yy2 = y2 >= min(p1[1], p2[1]) and y2 <= max(p1[1], p2[1])
        return yy1 or yy2
    return False

def coll(p1, p2, o, r):
    a = dist(p1, p2)
    b = dist(p1, o)
    c = dist(p2, o)
    p = (a + b + c) / 2
    s = sqrt(p * (p - a) * (p - b) * (p - c))
    h = s / a * 2
    if h <= r:
        if not p2[0]-p1[0] == 0:
            a = (p2[1]-p1[1])/(p2[0]-p1[0])
        else:
            a=9999999999999999
        b = p1[1]-a*p1[0]
        aa = a ** 2 + 1
        bb = 2 * (o[0] - (b - o[1]) * a)
        cc = (b - o[1]) ** 2 - r ** 2 + o[0] ** 2
        d = bb ** 2 - 4 * aa * cc
        d = sqrt(d)
        x1 = (bb + d) / (2 * aa)
        x2 = (bb - d) / (2 * aa)
        xx1 = x1 > min(p1[0], p2[0]) and x1 < max(p1[0], p2[0])
        xx2 = x2 > min(p1[0], p2[0]) and x2 < max(p1[0], p2[0])
        y1 = a * x1 + b
        y2 = a * x2 + b
        return xx1 or xx2
    return False

ppos = [100, 100]

pv = [0, 0]

r = 10

line = [[200, 200], [300, 200]]

screen = pygame.display.set_mode((400, 400))

done = False

points = False

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN:
            if e.scancode == 17:
                pv[1] = -0.1
            if e.scancode == 30:
                pv[0] = -0.1
            if e.scancode == 31:
                pv[1] = 0.1
            if e.scancode == 32:
                pv[0] = 0.1
        if e.type == pygame.KEYUP:
            if e.scancode == 17 and pv[1] < 0:
                pv[1] = 0
            if e.scancode == 30 and pv[0] < 0:
                pv[0] = 0
            if e.scancode == 31 and pv[1] > 0:
                pv[1] = 0
            if e.scancode == 32 and pv[0] > 0:
                pv[0] = 0
    screen.fill((0, 0, 0))
    ppos[0] += pv[0]
    points = true_coll(line[0], line[1], ppos, r)
    if points:
        ppos[0] -= pv[0]
    ppos[1] += pv[1]
    points = true_coll(line[0], line[1], ppos, r)
    if points:
        ppos[1] -= pv[1]

    pygame.draw.circle(screen, (255, 255, 255), [int(ppos[0]), int(ppos[1])], r)

    pygame.draw.line(screen, (255, 255, 255), line[0], line[1])

    #pygame.draw.circle(screen, (255, 255, 255), (200, 250), 3)
    #if points:
    #    if points[0]:
    #        pygame.draw.circle(screen, (0, 255, 0), [int(points[2][0]), int(points[2][1])], 3)
    #    if points[1]:
    #        pygame.draw.circle(screen, (0, 255, 0), [int(points[3][0]), int(points[3][1])], 3)

    pygame.display.update()
pygame.quit()
