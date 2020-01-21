import pygame
from math import sin, cos, radians, sqrt, asin, degrees
from random import randint

screen = pygame.display.set_mode((400,400))
done = False

class enemy():
    def __init__(self,pos,v):
        self.pos = pos
        self.deg = 0
        self.v = v
        self.weaponP = [0,0]
        self.r = 20
        self.deg2p = 0
        self.cooldown = 0
        self.hp = 4
        self.Vmove = 0
    def move(self):
        if dist(self,player)>=100:
            self.Vmove = 0.1
        elif dist(self,player)<=150:
            self.Vmove = -0.1
        else:
            self.Vmove = 0
        self.pos[0]+=self.v*cos(radians(self.deg))*self.Vmove
        self.pos[1]+=self.v*sin(radians(self.deg))*self.Vmove
        if self.pos[0]>400-self.r:
            self.pos[0]-=self.v*cos(radians(self.deg))*self.Vmove
        if self.pos[1]>400-self.r:
            self.pos[1]-=self.v*sin(radians(self.deg))*self.Vmove
        if self.pos[0]<self.r:
            self.pos[0]-=self.v*cos(radians(self.deg))*self.Vmove
        if self.pos[1]<self.r:
            self.pos[1]-=self.v*sin(radians(self.deg))*self.Vmove
    def rotate(self):
        self.deg2p = degrees(asin((self.pos[1]-player.pos[1])/dist(self,player)))
        if self.pos[0]>player.pos[0]:
            self.deg2p+=180
        else:
            self.deg2p*=-1
        if self.deg > self.deg2p:
            self.deg-=0.2
        if self.deg < self.deg2p:
            self.deg+=0.2
        self.weaponP = [self.pos[0]+cos(radians(self.deg))*(self.r+10),
                        self.pos[1]+sin(radians(self.deg))*(self.r+10)]
    def shoot(self):
        if self.deg-self.deg2p>-0.001 and self.deg-self.deg2p<0.001 and self.cooldown <= 0:
            bullets.put(bullet(self.weaponP,self.deg,0.1))
            self.cooldown = 2000
    def draw(self):
        pygame.draw.line(screen,(0,0,0),[int(self.pos[0]),int(self.pos[1])],[int(self.weaponP[0]),int(self.weaponP[1])],3)
        pygame.draw.circle(screen,(200,0,0),[int(self.pos[0]),int(self.pos[1])],self.r)

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

cooldown = 0

class bullet():
    def __init__(self,pos,deg,v):
        self.pos = pos
        self.deg = deg
        self.v = v
        self.dirx = 1
        self.diry = 1
        self.r = 3
        self.hp = 1
    def move(self):
        self.pos[0]+=self.v*cos(radians(self.deg))*self.dirx
        self.pos[1]+=self.v*sin(radians(self.deg))*self.diry
        if self.pos[0]>=397:
            self.dirx*=-1
        if self.pos[0]<=3:
            self.dirx*=-1
        if self.pos[1]>=397:
            self.diry*=-1
        if self.pos[1]<=3:
            self.diry*=-1
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
player = player([100,100],1)
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
                player.Vmove = -0.08
            if e.scancode == 17:
                player.Vmove = 0.08
            if e.scancode == 30:
                player.Vrot = -0.1
            if e.scancode == 32:
                player.Vrot = 0.1
            if e.scancode == 57:
                #isShooting = 1
                player.shoot()
        if e.type == pygame.KEYUP:
            if e.scancode == 31 and player.Vmove < 0:
                player.Vmove = 0
            if e.scancode == 17 and player.Vmove > 0:
                player.Vmove = 0
            if e.scancode == 30 and player.Vrot < 0:
                player.Vrot = 0
            if e.scancode == 32 and player.Vrot > 0:
                player.Vrot = 0
            #if e.scancode == 57:
                #isShooting = 0
        #print(e)
        
    screen.fill((255,255,255))
    player.move()
    player.rotate()
    player.draw()
    for i in range(len(bullets.elements)):
        if i>=len(bullets.elements):
            break
        if bullets.elements[i].hp == 0:
            bullets.take(i)
        elif coll(bullets.elements[i],player):
            bullets.take(i)
            player.hp-=1
        for j in range(len(enemies.elements)):
            if i>=len(bullets.elements):
                break
            if coll(bullets.elements[i],enemies.elements[j]):
                bullets.take(i)
                enemies.elements[j].hp-=1
    for i in range(len(bullets.elements)):
        bullets.elements[i].draw()
        bullets.elements[i].move()
    for i in enemies.elements:
        i.draw()
        i.rotate()
        i.shoot()
        i.cooldown-=1
        i.move()
    pygame.draw.rect(screen,(255,0,0),(10,10,player.hp*10,20))
    pygame.display.update()
    if player.hp <= 0:
        done = True
    for i in range(len(enemies.elements)):
        #print(enemies.elements)
        if i>=len(enemies.elements):
            break
        if enemies.elements[i].hp<=0:
            enemies.take(i)
    if cooldown<=0:
        enemies.put(enemy([randint(20,380),randint(20,380)],1))
        cooldown = 3000
    cooldown -= 1
    if player.hp<10:
        player.hp+=0.0003
    #if isShooting:
    #    player.shoot()
pygame.quit()
