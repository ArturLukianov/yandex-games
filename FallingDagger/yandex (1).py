import pygame
from math import sin, cos, radians

screen = pygame.display.set_mode((501, 501))

done = False

polytext = input()
polytext = polytext.replace(")", "")
polytext = polytext.replace("(", "")
polytext = polytext.replace(",", ".")
polytext = polytext.split(". ")
for i in range(len(polytext)):
    polytext[i] = list(map(float, polytext[i].split(";")))

z = 1

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:
                z *= 2
            if e.button == 5:
                z /= 2
    screen.fill((0, 0, 0))

    polygon = []
    for i in polytext:
        polygon.append([i[0] * z + 250, i[1] * z + 250])

    pygame.draw.polygon(screen, (255, 0, 0), polygon, 1)

    pygame.display.update()
pygame.quit()
