import pygame
from random import randint

pygame.init()

Tsize = 10
Fsize = 2
number = 12

f = int(input("Type mines frequency \"%\":"))
if f>100:
    print("too big")
    f = 100

screen = pygame.display.set_mode((Tsize*number+Fsize*(number+1),Tsize*number+Fsize*(number+1)))

done = False

one = pygame.image.load("1S.png")
two = pygame.image.load("2S.png")
three = pygame.image.load("3S.png")
four = pygame.image.load("4S.png")
flag = pygame.image.load("flagS.png")
mine = pygame.image.load("mineS.png")
fear = [one,two,three,four]



field = []
real = []
hints = []

for i in range(number):
    field.append([])
    real.append([])
    hints.append([])
    for j in range(number):
        field[i].append(0)
        real[i].append(0)
        hints[i].append(0)

mines = 0
Hmines = 0

for i in range(number):
    for j in range(number):
        if randint(0,100//f)==0:
            real[i][j] = 1
            mines += 1
            hints[i][j] = 9
print(mines)

for i in range(number):
    for j in range(number):
        if real[i][j]!=1:
            hint = 0
            if i>0 and j>0:
                if real[i-1][j-1]==1:
                    hint+=1
            if i<number-1 and j<number-1:
                if real[i+1][j+1]==1:
                    hint+=1
            if i>0:
                if real[i-1][j]==1:
                    hint+=1
            if j>0:
                if real[i][j-1]==1:
                    hint+=1
            if i<number-1:
                if real[i+1][j]==1:
                    hint+=1
            if j<number-1:
                if real[i][j+1]==1:
                    hint+=1
            if i>0 and j<number-1:
                if real[i-1][j+1]==1:
                    hint+=1
            if i<number-1 and j>0:
                if real[i+1][j-1]==1:
                    hint+=1
            hints[i][j] = hint




mx = 0
my = 0
refresh = 5
last = 0

def fill(i,j,old,new):
    if hints[i][j]==9 or field[i][j]!=0:
        return
    field[i][j]=1
    if hints[i][j]==old:
        if i>0:
            fill(i-1,j,old,new)
        if i<number-1:
            fill(i+1,j,old,new)
        if j>0:
            fill(i,j-1,old,new)
        if j<number-1:
            fill(i,j+1,old,new)
        if i>0 and j>0:
            fill(i-1,j-1,old,new)
        if i<number-1 and j<number-1:
            fill(i+1,j+1,old,new)
        if i<number-1 and j>0:
            fill(i+1,j-1,old,new)
        if i>0 and j<number-1:
            fill(i-1,j+1,old,new)

def boxColl(pos1,pos2,size):
    if pos1[0] <= pos2[0]+size[0] and pos1[0] >= pos2[0] and pos1[1] <= pos2[1]+size[1] and pos1[1] >= pos2[1]:
        return True
    return False

while not done:
    #print(pygame.time.get_ticks())
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.MOUSEMOTION:
            mx,my = e.pos
        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            for i in range(number):
                for j in range(number):
                    if boxColl((mx,my),(i*Tsize+i*Fsize+Fsize,j*Tsize+j*Fsize+Fsize),(Tsize,Tsize)):
                        fill(i,j,0,-1)
                        field[i][j]=1
                        if real[i][j] == 1:
                            print("YOU LOSE")
                            for i in range(number):
                                for j in range(number):
                                    if real[i][j]==1:
                                        field[i][j]=1
                            done = True
                        break
        if e.type == pygame.MOUSEBUTTONUP and e.button == 3:
            for i in range(number):
                for j in range(number):
                    if boxColl((mx,my),(i*Tsize+i*Fsize+Fsize,j*Tsize+j*Fsize+Fsize),(Tsize,Tsize)):
                        if last + refresh <= pygame.time.get_ticks():
                            if field[i][j]==0:
                                Hmines +=1
                                field[i][j]=2
                            elif field[i][j]==2:
                                Hmines -=1
                                field[i][j]=0
                            last = pygame.time.get_ticks()

    screen.fill((0,0,0))

    for i in range(number):
        for j in range(number):
            if field[i][j]==0:
                pygame.draw.rect(screen,(255,255,255),(i*Tsize+i*Fsize+Fsize,j*Tsize+j*Fsize+Fsize,Tsize,Tsize))
            elif hints[i][j]<5 and hints[i][j]!=0 and field[i][j]==1:
                screen.blit(fear[hints[i][j]-1],(i*Tsize+i*Fsize+Fsize,j*Tsize+j*Fsize+Fsize,Tsize,Tsize))
            elif field[i][j]==2:
                screen.blit(flag,(i*Tsize+i*Fsize+Fsize,j*Tsize+j*Fsize+Fsize,Tsize,Tsize))
            if real[i][j] == 1 and field[i][j] == 1:
                screen.blit(mine,(i*Tsize+i*Fsize+Fsize,j*Tsize+j*Fsize+Fsize,Tsize,Tsize))
    Mwon = True
    for i in range(number):
        for j in range(number):
            if real[i][j]==1:
                if field[i][j]!=2:
                    Mwon = False
            if field[i][j]==0:
                Mwon = False
    if Mwon and Hmines == mines:
        done = True
        print("YOU WIN!")
    pygame.display.update()
pygame.quit()
