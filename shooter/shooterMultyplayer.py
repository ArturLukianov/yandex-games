import pygame
from math import sin, cos, radians, sqrt

screen = pygame.display.set_mode((400,400))
done = False

class player():
    def __init__(self,pos,v):
        self.pos = pos
        self.deg = 0
        self.v = v
        self.Vmove = 0
        self.Vrot = 0
        self.weaponP = [0,0]
        self.r = 20
        self.hp = 10
    def rotate(self):
        self.deg+=self.Vrot
        self.weaponP = [self.pos[0]+cos(radians(self.deg))*(self.r+10),
                        self.pos[1]+sin(radians(self.deg))*(self.r+10)]
    def move(self):
        self.pos[0]+=self.v*cos(radians(self.deg))*self.Vmove
        if self.pos[0]>400-self.r:
            self.pos[0]-=self.v*cos(radians(self.deg))*self.Vmove
        if self.pos[0]<self.r:
            self.pos[0]-=self.v*cos(radians(self.deg))*self.Vmove
        self.pos[1]+=self.v*sin(radians(self.deg))*self.Vmove
        if self.pos[1]>400-self.r:
            self.pos[1]-=self.v*sin(radians(self.deg))*self.Vmove
        if self.pos[1]<self.r:
            self.pos[1]-=self.v*sin(radians(self.deg))*self.Vmove
        for i in enemies.elements:
            if coll(self,i):
                self.pos[1]-=self.v*sin(radians(self.deg))*self.Vmove
                self.pos[0]-=self.v*cos(radians(self.deg))*self.Vmove
    def shoot(self):
        bullets.put(bullet(self.weaponP,self.deg,0.1))
    def draw(self):
        pygame.draw.line(screen,(255,0,0),[int(self.pos[0]),int(self.pos[1])],[int(self.weaponP[0]),int(self.weaponP[1])],3)
        pygame.draw.circle(screen,(0,0,0),[int(self.pos[0]),int(self.pos[1])],self.r)

class bullet():
    def __init__(self,pos,deg,v):
        self.pos = pos
        self.deg = deg
        self.v = v
        self.dirx = 1
        self.diry = 1
        self.hp = 4
        self.r = 3
    def move(self):
        self.pos[0]+=self.v*cos(radians(self.deg))*self.dirx
        self.pos[1]+=self.v*sin(radians(self.deg))*self.diry
        if self.pos[0]>=397:
            self.dirx*=-1
            self.hp-=1
        if self.pos[0]<=3:
            self.dirx*=-1
            self.hp-=1
        if self.pos[1]>=397:
            self.diry*=-1
            self.hp-=1
        if self.pos[1]<=3:
            self.diry*=-1
            self.hp-=1
    def draw(self):
        pygame.draw.circle(screen,(255,200,0),[int(self.pos[0]),int(self.pos[1])],self.r)

class idk():
    def __init__(self,elements):
        self.elements = elements
    def put(self,element):
        self.elements.append(element)
    def take(self,index):
        b = []
        a = self.elements[index]
        for i in range(len(self.elements)):
            if i!=index:
                b.append(self.elements[i])
        self.elements = b
        return a

bullets = idk([])
player1 = player([100,100],1)
player2 = player([300,300],1)
enemies = idk([])

def dist(o1,o2):
    x = o1.pos[0]-o2.pos[0]
    y = o1.pos[1]-o2.pos[1]
    return sqrt(x*x+y*y)

def coll(o1,o2):
    if dist(o1,o2)<=o1.r+o2.r:
        return True
    return False

#isShooting = 0

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN:
            if e.scancode == 31:
                player1.Vmove = -0.08
            if e.scancode == 17:
                player1.Vmove = 0.08
            if e.scancode == 30:
                player1.Vrot = -0.08
            if e.scancode == 32:
                player1.Vrot = 0.08
            if e.scancode == 57:
                #isShooting = 1
                player1.shoot()
            if e.scancode == 80:
                player2.Vmove = -0.08
            if e.scancode == 72:
                player2.Vmove = 0.08
            if e.scancode == 75:
                player2.Vrot = -0.08
            if e.scancode == 77:
                player2.Vrot = 0.08
            if e.scancode == 82:
                #isShooting = 1
                player2.shoot()
        if e.type == pygame.KEYUP:
            if e.scancode == 31 and player1.Vmove < 0:
                player1.Vmove = 0
            if e.scancode == 17 and player1.Vmove > 0:
                player1.Vmove = 0
            if e.scancode == 30 and player1.Vrot < 0:
                player1.Vrot = 0
            if e.scancode == 32 and player1.Vrot > 0:
                player1.Vrot = 0
            if e.scancode == 80 and player2.Vmove < 0:
                player2.Vmove = 0
            if e.scancode == 72 and player2.Vmove > 0:
                player2.Vmove = 0
            if e.scancode == 75 and player2.Vrot < 0:
                player2.Vrot = 0
            if e.scancode == 77 and player2.Vrot > 0:
                player2.Vrot = 0
            #if e.scancode == 57:
                #isShooting = 0
        print(e)
        
    screen.fill((255,255,255))
    player1.move()
    player1.rotate()
    player1.draw()
    player2.move()
    player2.rotate()
    player2.draw()
    for i in range(len(bullets.elements)):
        if i>=len(bullets.elements):
            break
        if bullets.elements[i].hp == 0:
            bullets.take(i)
        elif coll(bullets.elements[i],player1):
            bullets.take(i)
            player1.hp-=1
        elif coll(bullets.elements[i],player2):
            bullets.take(i)
            player2.hp-=1
    for i in range(len(bullets.elements)):
        bullets.elements[i].draw()
        bullets.elements[i].move()
    pygame.draw.rect(screen,(255,0,0),(10,10,player1.hp*10,20))
    pygame.draw.rect(screen,(255,0,0),(290,10,player2.hp*10,20))
    pygame.display.update()
    if player1.hp <= 0:
        done = True
    if player1.hp<10:
        player1.hp+=0.0001
    if player2.hp <= 0:
        done = True
    if player2.hp<10:
        player2.hp+=0.0001
    #if isShooting:
    #    player.shoot()
pygame.quit()
