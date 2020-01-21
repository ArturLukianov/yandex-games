import pygame

height = 400
width = 400

G = 9.8
DT = 0.000001

screen = pygame.display.set_mode((width,height))

def coll(o1,o2):
    if o1.pos[0]+o1.size[0]>=o2.pos[0] and o2.pos[0]+o2.size[0]>=o1.pos[0] and o1.pos[1]+o1.size[1]>=o2.pos[1] and o2.pos[1]+o2.size[1]>=o1.pos[1]:
        return True
    return False

class block():
    def __init__(self,pos,size):
        self.pos = pos
        self.size = size
        self.v = [0,0]
    def fall(self):
        self.v[1]+=G*DT
    def move(self):
        self.pos[0]+=self.v[0]
        if coll(self,block):
            self.pos[0]-=self.v[0]
            self.v[0]*=-0.5
        self.pos[1]+=self.v[1]
        if coll(self,block):
            self.pos[1]-=self.v[1]
            self.v[1]*=-0.5
    def draw(self):
        pygame.draw.rect(screen,(255,255,255),(self.pos[0],self.pos[1],self.size[0],self.size[1]))

done = False

box = block([20,50],[20,20])
box1 = block([20,20],[20,20])
block = block([0,300],[400,20])

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True

    screen.fill((0,0,0))
    
    box.fall()
    box.move()
    box.draw()
    box1.fall()
    box1.move()
    box1.draw()
    block.draw()

    pygame.display.update()

pygame.quit()
