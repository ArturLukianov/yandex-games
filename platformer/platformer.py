import pygame
#from random import randint
from math import sin,cos,radians

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)

pygame.init()

r = 100

WIDTH = 400
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH,HEIGHT))

G = 9.8
DT = 0.0001
bg = (0,0,0)
noise = -2

class player():
    def __init__(self,param,color,speed):
        self.param = param
        self.color = color
        self.v = [0,0]
        self.speed = speed
        self.onground = 0
        self.ice = 1.001
    def draw(self):
        pygame.draw.rect(screen,self.color,self.param)
    def fall(self):
        self.v[1]+=G*DT
    def move(self):
        self.param[0]+=self.v[0]
        for i in blocks:
            self.param[1]+=self.v[1]
            if coll(self,i):
                self.param[1]-=self.v[1]

class block():
    def __init__(self,param,color):
        self.param = param
        self.color = color
    def draw(self):
        pygame.draw.rect(screen,self.color,self.param)

class colects():
    def __init__(self):
        self.items = []
    def put(self,element):
        self.items.append(element)
    def take(self,index):
        b = []
        for i in range(len(self.items)):
            if i!=index:
                b.append(self.items[i])
        self.items = b
    def draw(self):
        for i in self.items:
            i.draw()

class coin():
    def __init__(self,param):
        self.param = param
        self.color = [255,200,0]
    def draw(self):
        pygame.draw.rect(screen,self.color,self.param)

class trap():
    def __init__(self,param):
        self.param = param
        self.color = [255,0,0]
    def draw(self):
        pygame.draw.rect(screen,self.color,self.param)
class ice():
    def __init__(self,param):
        self.param = param
        self.color = [0,100,200]
    def draw(self):
        pygame.draw.rect(screen,self.color,self.param)

Trap = trap([100,100,25,25])
Ice = ice([150,250,100,10])

C = [200,200]

shift = 0

def coll(obj1,obj2):
    x = obj1.param[0]+obj1.param[2]>=obj2.param[0] and obj2.param[0]+obj2.param[2]>=obj1.param[0]
    y = obj1.param[1]+obj1.param[3]>=obj2.param[1] and obj2.param[1]+obj2.param[3]>=obj1.param[1]
    #print(x,y)
    return x and y

blocks = [block([50,300,300,50],[255,255,255]),block([100,250,200,20],[255,255,255])]

col = colects()

def start():
    global points, deg, textsurface
    textsurface = myfont.render(str(0), False, [255,255,255])
    points = 0
    col.items = []
    deg = 0
    col.put(coin([110,220,20,20]))
    col.put(coin([150,220,20,20]))
    col.put(coin([230,220,20,20]))
    col.put(coin([270,220,20,20]))
    global pl
    pl = player([190,190,20,20],[255,255,255],0.4)

done = False

refresh = 2
last = 0

r = 0

left = 0
right = 0

points = 0

space = 0

deg = 0

start()

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        #print(e)
        if e.type == pygame.KEYDOWN:
            if e.scancode == 30:
                left = 1
                pl.v[0]=-pl.speed
            if e.scancode == 32:
                right = 1
            if e.scancode == 57:
                space = 1
            if e.scancode == 42:
                shift = 1
        if e.type == pygame.KEYUP:
            if e.scancode == 30:
                left = 0
            if e.scancode == 32:
                right = 0
            if e.scancode == 57:
                space = 0
            if e.scancode == 42:
                shift = 0

    screen.fill(bg)

    for i in blocks:
        if coll(pl,i) and pl.param[1]+pl.param[3]+noise<=i.param[1]:
            pl.onground = 1
            break
        else:
            pl.onground = 0
        if coll(pl,i) and pl.param[0]+pl.param[2]+noise<=i.param[0] and pl.v[0]>0:
            pl.v[0]=0
        if coll(pl,i) and i.param[0]+i.param[2]+noise<=pl.param[0] and pl.v[0]<0:
            pl.v[0]=0
        if coll(pl,i) and i.param[1]+i.param[3]+noise<=pl.param[1] and pl.v[1]<0:
            pl.v[1]=0

    if pl.param[0]<=0 and pl.v[0]<0:
        pl.v[0]=0
    if pl.param[0]+pl.param[2]>=400 and pl.v[0]>0:
        pl.v[0]=0

    pl.draw()

    Trap.param[0]=cos(radians(deg))*100+C[0]
    Trap.param[1]=sin(radians(deg))*100+C[1]

    if pl.param[1]>400:
        pl.param[1]=0-pl.param[3]-1

    #for i in blocks:
    #    if coll(pl,i) and pl.param[0]+pl.param[2]+noise>=i.param[0] and pl.v[0]<0 and pl.param[1]+pl.param[2]+noise<=i.param[0]:
    #        pl.v[0] = 0
    #    if coll(pl,i) and i.param[0]+i.param[2]+noise>=pl.param[0] and pl.v[0]>0:
    #        pl.v[0] = 0
    
    if last+refresh<=pygame.time.get_ticks():
        pl.move()
        if not pl.onground:
            pl.fall()
        else:
            pl.v[1]=0
        last = pygame.time.get_ticks()
    for i in blocks:
        i.draw()

    col.draw()

    for i in range(len(col.items)):
        if coll(pl,col.items[i]):
            points+=1
            col.take(i)
            textsurface = myfont.render(str(points), False, [255,255,255])
            break

    if space and pl.onground:
        pl.v[1]=-0.3
    if right:
        if shift:
            pl.v[0]=pl.speed*1.5
        else:
            pl.v[0]=pl.speed
    if left:
        if shift:
            pl.v[0]=-pl.speed*1.5
        else:
            pl.v[0]=-pl.speed

    if coll(pl,Trap):
        start()
    if coll(pl,Ice):
        pl.ice = 1.0005
    else:
        pl.ice = 1.001

    pl.color = [r%255,(150-r)%255,(50-r)%255]
    r+=0.1

    Ice.draw()

    Trap.draw()
    deg+=0.05

    screen.blit(textsurface,[100,10])

    pygame.display.update()

    if not (right or left):
        pl.v[0]/=pl.ice

pygame.quit()
