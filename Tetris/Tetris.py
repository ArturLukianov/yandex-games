import pygame
from random import randint

pygame.init()

pygame.font.init()

font = pygame.font.SysFont('Arial', 16)

Next = font.render('Next:', False, (255,255,255))

screen = pygame.display.set_mode((400,400))

pygame.display.set_caption("Tetris")

done = False

field = []

last = 0
refresh = 100

w = 20
h = 40

lastF = 0

boost = 0

v = 0

points = 0

def rotate(a,s):
    new = []
    if s==1:
        for i in a:
            v = i
            vr = v
            r = [[0,-1],[1,0]]
            vt = [r[0][0]*vr[0]+r[0][1]*vr[1],r[1][0]*vr[0]+r[1][1]*vr[1]]
            new.append(vt)
    elif s==-1:
        for i in a:
            v = i
            vr = v
            r = [[0,1],[-1,0]]
            vt = [r[0][0]*vr[0]+r[0][1]*vr[1],r[1][0]*vr[0]+r[1][1]*vr[1]]
            new.append(vt)
    return new

Tsize = 400/h

for i in range(h):
    field.append([])
    for j in range(w):
        field[i].append([0,0])

colors = [[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255]]

shapes = [[[[0,0],[1,0],[1,1],[0,1]],0],
                [[[0,0],[1,0],[1,1],[1,2]],1],
                [[[1,0],[0,0],[0,1],[0,2]],2],
                [[[0,0],[0,1],[1,1],[1,2]],3],
                [[[1,0],[1,1],[0,1],[0,2]],4],
                [[[0,0],[0,1],[1,1],[0,2]],5]]

shape = shapes[randint(0,len(shapes)-1)][::1]
pos = [9,0]

new = shapes[randint(0,len(shapes)-1)][::1]

pressed_W = 0

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN:
            if e.scancode == 30:
                v = -1
            if e.scancode == 32:
                v = 1
            if e.scancode == 17:
                shape[0] = rotate(shape[0],1)
                for i in shape[0]:
                    if i[0]+pos[0]<0 or i[0]+pos[0]==w or i[1]+pos[1]<0 or i[1]+pos[1]==h:
                        shape[0] = rotate(shape[0],-1)
                        break
                    elif field[i[1]+pos[1]][i[0]+pos[0]][0]==1:
                        shape[0] = rotate(shape[0],-1)
                        break
            if e.scancode == 31:
                pressed_W = 1
        if e.type == pygame.KEYUP:
            if e.scancode == 30 and v<0:
                v = 0
            if e.scancode == 32 and v>0:
                v = 0
            if e.scancode == 31:
                pressed_W = 0
                boost = 0

    screen.fill((0,0,0))

    pygame.draw.line(screen,(255,255,255),[201,0],[201,400])

    for i in range(h):
        for j in range(w):
            if field[i][j][0]==1:
                pygame.draw.rect(screen,colors[field[i][j][1]],[j*Tsize+1,i*Tsize+1,Tsize-2,Tsize-2])

    for i in shape[0]:
        pygame.draw.rect(screen,colors[shape[1]],[(i[0]+pos[0])*Tsize+1,(i[1]+pos[1])*Tsize+1,Tsize-2,Tsize-2])
    pygame.draw.rect(screen,(255,255,255),[280,80,40,50])
    pygame.draw.rect(screen,(0,0,0),[281,81,38,48])
    for i in new[0]:
        pygame.draw.rect(screen,colors[new[1]],[290+i[0]*Tsize+1,90+i[1]*Tsize+1,Tsize-2,Tsize-2])

    Score = font.render('Score: '+str(points), False, (255,255,255))

    screen.blit(Next,[280,60])

    screen.blit(Score,[280,130])

    if pygame.time.get_ticks() >= last+refresh:
        pos[0]+=v
        for i in shape[0]:
            if i[0]+pos[0]==w or i[0]+pos[0]<0:
                pos[0]-=v
            elif field[i[1]+pos[1]][i[0]+pos[0]][0]==1:
                pos[0]-=v
        last = pygame.time.get_ticks()
    
    if pygame.time.get_ticks() >= lastF+refresh-boost:
        pos[1]+=1
        lastF = pygame.time.get_ticks()

    for i in shape[0]:
        if i[1]+pos[1] == h-1 or field[i[1]+pos[1]+1][i[0]+pos[0]][0]==1:
            for j in shape[0]:
                field[j[1]+pos[1]][j[0]+pos[0]]=[1,shape[1]]
            pos = [9,0]
            shape = new[::1]
            new = shapes[randint(0,len(shapes)-1)][::1]
            refresh*=0.99
            break

    for i in range(w):
        if field[0][i][0]==1:
            done = True
    for i in range(h):
        s = 0
        for j in field[i]:
            s+=j[0]
        if s == w:
            for j in range(w):
                field[i][j]=[0,0]
            points +=1

    if pressed_W:
        boost = refresh/1.75

    pygame.display.update()

pygame.quit()
