import pygame
import sys
from random import randint

#dfn - defence
#dmg - damage

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 32)
log = pygame.font.SysFont("Arial",12)

screen = pygame.display.set_mode((400,400))

items = [[255,0,0],[0,255,0],[0,0,255]]

path = "textures/"

names = ["sword","sword","clothes"]
textures = []

for i in names:
    textures.append(pygame.image.load(path+i+".png"))

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

done = False

class item():
    def __init__(self,idi,count,Type,dmg,dfn):
        self.id = idi
        self.count = count
        self.color = items[self.id]
        self.use = False
        self.type = Type
        self.dmg = dmg
        self.dfn = dfn
        self.uses = 0
    def draw(self,pos):
        if self.id < len(textures):
            screen.blit(textures[self.id],pos)
        else:
            pygame.draw.rect(screen,self.color,[pos[0],pos[1],32,32])
        count = log.render(str(self.count),True,[0,255,255])
        rect = count.get_rect()
        screen.blit(count,[pos[0]+33-rect[2],pos[1]+34-rect[3]])
    def Refresh(self):
        mins = -2+self.uses
        if mins>0:
             mins = 0
        maxs = 2-self.uses
        if maxs<0:
            maxs = 0
        if self.type == "weapon":
            self.showEffect = self.dmg+randint(mins,maxs)
        elif self.type == "armor":
            self.showEffect = self.dfn+randint(mins,maxs)
        if self.showEffect < 0:
            self.showEffect = 0

class itemOnField():
    def __init__(self,idi,count,pos,Type,dmg,dfn):
        self.id = idi
        self.count = count
        self.color = items[self.id]
        self.pos = pos
        self.size = [10,10]
        self.type = Type
        self.dmg = dmg
        self.dfn = dfn
    def draw(self):
        pygame.draw.rect(screen,self.color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])

Items = idk([itemOnField(0,1,[150,100],"weapon",7,0),itemOnField(2,1,[200,100],"armor",0,40)])

def PIR(pos,o):
    if pos[0]>=o.pos[0] and pos[0]<=o.pos[0]+o.size[0]:
        if pos[1]>=o.pos[1] and pos[1]<=o.pos[1]+o.size[1]:
            return True
    return False

def PIR2(pos1,pos2,size):
    if pos1[0]>=pos2[0] and pos1[0]<=pos2[0]+size[0]:
        if pos1[1]>=pos2[1] and pos1[1]<=pos2[1]+size[1]:
            return True
    return False

def coll(o1,o2):
    if o1.pos[0]<=o2.pos[0]+o2.size[0] and o2.pos[0]<=o1.pos[0]+o1.size[0]:
        if o1.pos[1]<=o2.pos[1]+o2.size[1] and o2.pos[1]<=o1.pos[1]+o1.size[1]:
            return True
    return False

class button():
    def __init__(self,pos,size,command,text,color):
        self.pos = pos
        self.size = size
        self.command = command
        self.text = font.render(text, False, (0, 0, 0))
        self.color = color
        self.active = 0
    def push(self,mouse):
        if PIR(mouse,self):
            self.command()
    def draw(self):
        if not self.active:
            pygame.draw.rect(screen,self.color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])
        else:
            pygame.draw.rect(screen,[200,200,200],[self.pos[0],self.pos[1],self.size[0],self.size[1]])
        rect = self.text.get_rect()
        p1 = (self.size[0]-rect[2])/2
        p2 = (self.size[1]-rect[3])/2
        screen.blit(self.text,[self.pos[0]+p1,self.pos[1]+p2])

class hand():
    def __init__(self):
        self.dmg = 1
        self.dfn = 1
        self.uses = 0
        self.showEffect = 1
    def Refresh(self):
        pass

class player():
    def __init__(self,pos,size,color,speed):
        self.pos = pos
        self.size = size
        self.color = color
        self.v = [0,0]
        self.inv = [0,0,0,0,0,0,0,0,0,0]
        self.speed = speed
        self.equipment = {"weapon":hand(),"armor":hand()}
        self.dmg = 1
        self.dfn = 0
        self.cooldown = 5000
        self.lasthit = -self.cooldown
        self.hp = 100
        self.dmgBoost = 0
        self.dfnBoost = 0
    def move(self):
        self.pos[0]+=self.v[0]
        if self.pos[0]<=0 or self.pos[0]+self.size[0]>401:
            self.pos[0]-=self.v[0]
        for test in enemies.elements:
            if coll(self,test):
                self.pos[0]-=self.v[0]
                if pygame.time.get_ticks() >= self.lasthit + self.cooldown:
                    test.hp-=player.dmg*(100-test.dfn)/100
                    self.lasthit = pygame.time.get_ticks()
                    self.equipment["weapon"].uses+=1
                    player.equipment["weapon"].Refresh()
                break
        self.pos[1]+=self.v[1]
        if self.pos[1]<=0 or self.pos[1]+self.size[1]>401:
            self.pos[1]-=self.v[1]
        for test in enemies.elements:
            if coll(self,test):
                self.pos[1]-=self.v[1]
                if pygame.time.get_ticks() >= self.lasthit + self.cooldown:
                    test.hp-=player.dmg*(100-test.dfn)/100
                    self.lasthit = pygame.time.get_ticks()
                    self.equipment["weapon"].uses+=1
                    player.equipment["weapon"].Refresh()
                break
    def draw(self):
        pygame.draw.rect(screen,self.color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])
    def drawInv(self):
        for i in range(len(self.inv)):
            pygame.draw.rect(screen,(255,255,255),[i*34,0,34,34])
            pygame.draw.rect(screen,(0,0,0),[i*34+1,1,32,32])
            if self.inv[i] != 0:
                self.inv[i].draw([34*i+1,1])

mode = 0

player = player([100,100],[20,20],[255,255,255],1)

def Quit():
    pygame.quit()
    sys.exit()

def start():
    global mode
    mode = 2

def options():
    global mode
    mode = 1

def Credits():
    global mode
    mode = 3

def menu():
    global mode
    mode = 0

cred1 = "Programming: KlinSchneFlei"
cred2 = "Textures: KlinSchneFlei"
cred3 = "Music: KlinSchneFlei"
cred4 = "Parallel with B@gcat"
cred1 = font.render(cred1,True,(255,255,255))
cred2 = font.render(cred2,True,(255,255,255))
cred3 = font.render(cred3,True,(255,255,255))
cred4 = font.render(cred4,True,(255,255,255))

take = "Press \"p\" to pick up"
take = font.render(take,True,(255,255,255))

quitButton = button([150,300],[100,40],Quit,"Quit",[255,255,255])
startButton = button([150,100],[100,40],start,"Start",[255,255,255])
creditsButton = button([150,200],[100,40],Credits,"Credits",[255,255,255])
creditsBackButton = button([10,10],[100,40],menu,"Back",[255,255,255])


menuButtons = [startButton,creditsButton,quitButton]

mPos = [0,0]

class optButton():
    def __init__(self,command,text):
        self.command = command
        self.text = text
        self.text = log.render(self.text,True,(255,255,255))
        self.size = [self.text.get_rect()[0],self.text.get_rect()[1]]
        self.pos = [self.text.get_rect()[2],self.text.get_rect()[3]]
        self.active = False
    def push(self,args):
        self.command(args)
    def draw(self,size,pos):
        self.pos = pos
        self.size = size
        pygame.draw.rect(screen,(255,255,255),[pos[0],pos[1],size[0],size[1]])
        if not self.active:
            pygame.draw.rect(screen,(0,0,0),[pos[0]+1,pos[1]+1,size[0]-2,size[1]-2])
        else:
            pygame.draw.rect(screen,(100,100,100),[pos[0]+1,pos[1]+1,size[0]-2,size[1]-2])
        screen.blit(self.text,[pos[0]+2,pos[1]+2])

class options():
    def __init__(self,buttons):
        self.buttons = buttons
        self.size = [0,0]
        for i in buttons:
            if self.size[0]<i.text.get_rect()[2]:
                self.size[0] = i.text.get_rect()[2]
            if self.size[1]<i.text.get_rect()[3]:
                self.size[1] = i.text.get_rect()[3]
        self.size[0]+=5
        self.size[1]+=5
    def draw(self,pos):
        for i in range(len(self.buttons)):
            self.buttons[i].draw(self.size,[pos[0],pos[1]+self.size[1]*i])

class enemy():
    def __init__(self,pos,dmg,dfn,hp,size,name,v,cooldown,drops,Type):
        self.dmg = dmg
        self.pos = pos
        self.dfn = dfn
        self.hp = hp
        self.size = size
        self.name = name
        self.v = v
        self.cooldown = cooldown
        self.lasthit = -cooldown
        self.drops = drops
        self.type = Type
    def move(self,target):
        mePos = [self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2]
        targetPos = [target.pos[0]+target.size[0]/2,target.pos[1]+target.size[1]/2]
        if mePos[0]>targetPos[0]:
            self.pos[0]-=self.v
        if coll(self,target):
            self.pos[0]+=self.v
            if pygame.time.get_ticks()>=self.lasthit+self.cooldown:
                target.hp-=self.dmg*(100-target.dfn)/100
                self.lasthit = pygame.time.get_ticks()
        if mePos[0]<targetPos[0]:
            self.pos[0]+=self.v
        if coll(self,target):
            self.pos[0]-=self.v
            if pygame.time.get_ticks()>=self.lasthit+self.cooldown:
                target.hp-=self.dmg*(100-target.dfn)/100
                self.lasthit = pygame.time.get_ticks()
        if mePos[1]>targetPos[1]:
            self.pos[1]-=self.v
        if coll(self,target):
            self.pos[1]+=self.v
            if pygame.time.get_ticks()>=self.lasthit+self.cooldown:
                target.hp-=self.dmg*(100-target.dfn)/100
                self.lasthit = pygame.time.get_ticks()
        if mePos[1]<targetPos[1]:
            self.pos[1]+=self.v
        if coll(self,target):
            self.pos[1]-=self.v
            if pygame.time.get_ticks()>=self.lasthit+self.cooldown:
                target.hp-=self.dmg*(100-target.dfn)/100
                self.lasthit = pygame.time.get_ticks()
    def drop(self):
        a = randint(0,len(self.drops)-1)
        if self.drops[a]["type"]=="weapon":
            Items.put(itemOnField(self.drops[a]["id"],randint(self.drops[a]["count"][0],self.drops[a]["count"][1]),self.pos,self.drops[a]["type"],randint(self.drops[a]["dmg"][0],self.drops[a]["dmg"][0]),randint(self.drops[a]["dfn"][0],self.drops[a]["dfn"][0])))

    def draw(self):
        pygame.draw.rect(screen,(0,0,255),[self.pos[0],self.pos[1],self.size[0],self.size[1]])

pressed = 0

drops = [{"id":0,"count":[1,1],"type":"weapon","dmg":[1,8],"dfn":[0,0]},{"id":0,"count":[1,1],"type":"weapon","dmg":[3,5],"dfn":[0,0]}]

enemies = idk([enemy([300,300],10,50,50,[20,20],"test",0.5,1000,drops,"1"),enemy([300,300],20,50,100,[20,20],"test",0.1,2000,drops,"1")])

last = 0
refresh = 5

pressedRight = False
pressedLeft = False

Use = False

def use(i):
    if not player.inv[i].use:
        player.equipment[player.inv[i].type] = player.inv[i]
        player.inv[i].use = True
    else:
        player.equipment[player.inv[i].type] = hand()
        player.inv[i].use = False
    player.dmg = player.equipment[player.inv[i].type].dmg + player.dmgBoost
    player.dfn = player.equipment[player.inv[i].type].dfn + player.dfnBoost

def drop(i):
    player.equipment[player.inv[i].type] = hand()
    if player.inv[i].type == "weapon":
        player.dmg = hand().dmg + player.dmgBoost
    elif player.inv[i].type == "armor":
        player.dfn = hand().dfn
    Items.put(itemOnField(player.inv[i].id,player.inv[i].count,[player.pos[0],player.pos[1]],player.inv[i].type,player.inv[i].dmg,player.inv[i].dfn))
    player.inv[i] = 0
    global Use
    Use = False

lastPos = [0,0]

useOpt = options([optButton(use,"use"),optButton(drop,"drop")])

current = 0

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.MOUSEMOTION:
            mPos = e.pos
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                pressed = 1
                pressedLeft = True
            if e.button == 3:
                pressedRight = True
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                pressed = 0
        if e.type == pygame.KEYDOWN:
            if mode == 2:
                if e.scancode == 30:
                    player.v[0]=-player.speed
                if e.scancode == 32:
                    player.v[0]=player.speed
                if e.scancode == 17:
                    player.v[1]=-player.speed
                if e.scancode == 31:
                    player.v[1]=player.speed
        if e.type == pygame.KEYUP:
            if mode == 2:
                if e.scancode == 30 and player.v[0]<0:
                    player.v[0]=0
                if e.scancode == 32 and player.v[0]>0:
                    player.v[0]=0
                if e.scancode == 17 and player.v[1]<0:
                    player.v[1]=0
                if e.scancode == 31 and player.v[1]>0:
                    player.v[1]=0
                if e.scancode == 1 and mode == 2:
                    mode = 0
                if e.scancode == 18:
                    mode = 4
            elif e.scancode == 18:
                if mode == 4:
                    mode = 2
            if e.scancode == 25:
                if mode == 2:
                    for i in range(len(Items.elements)):
                        if coll(Items.elements[i],player):
                            if 0 in player.inv:
                                a = Items.take(i)
                            for i in range(len(player.inv)):
                                if player.inv[i]==0:
                                    player.inv[i] = item(a.id,a.count,a.type,a.dmg,a.dfn)
                                    player.inv[i].Refresh()
                                    break
                                elif player.inv[i].id==a.id and player.inv[i].dmg == a.dmg and player.inv[i].dfn == a.dfn:
                                    player.inv[i].count += a.count
                                    break
                            break
    screen.fill((0,0,0))
    if mode == 0:
        for i in menuButtons:
            if PIR(mPos,i):
                i.active = 1
            else:
                i.active = 0
            if pressed:
                i.push(mPos)
            i.draw()
    elif mode == 3:
        creditsBackButton.draw()
        if PIR(mPos,creditsBackButton):
            creditsBackButton.active = 1
        else:
            creditsBackButton.active = 0
        if pressed:
            creditsBackButton.push(mPos)
        screen.blit(cred1,[10,50])
        screen.blit(cred2,[10,90])
        screen.blit(cred3,[10,130])
        screen.blit(cred4,[10,170])
    elif mode == 2:
        for i in Items.elements:
            if coll(i,player):
                screen.blit(take,[10,10])
            i.draw()
        if pygame.time.get_ticks()>=last+refresh:
            player.move()
            for test in enemies.elements:
                test.move(player)
            last = pygame.time.get_ticks()
        player.draw()
        for test in enemies.elements:
            test.draw()
        hp = log.render(str(player.hp),True,[255,255,255])
        screen.blit(hp,[380,10])
        dmg = log.render(str(player.dmg),True,[255,255,255])
        dfn = log.render(str(player.dfn),True,[255,255,255])
        screen.blit(dmg,[10,10])
        screen.blit(dfn,[10,50])
    elif mode == 4:
        player.drawInv()
        for i in range(len(player.inv)):
            if PIR2(mPos,[i*34,0],[34,34]):
                if player.inv[i]!=0:
                    a = ")"
                    if player.inv[i].use == True:
                        a = ") (equiped)"
                    effect = ""
                    color = [255,0,0]
                    if player.inv[i].type == "weapon":
                        if player.inv[i].dmg - player.equipment[player.inv[i].type].dmg >0:
                            effect = "+"
                            color = [0,255,0]
                        elif player.inv[i].dmg - player.equipment[player.inv[i].type].dmg == 0:
                            color = [255,255,255]
                    elif player.inv[i].type == "armor":
                        if player.inv[i].dfn - player.equipment[player.inv[i].type].dfn >0:
                            effect = "+"
                            color = [0,255,0]
                        elif player.inv[i].dfn - player.equipment[player.inv[i].type].dfn == 0:
                            color = [255,255,255]
                    
                    name = log.render(names[player.inv[i].id]+" "+effect+str(player.inv[i].showEffect - player.equipment[player.inv[i].type].showEffect)+" ("+str(player.inv[i].showEffect)+a,True,color)
                    nameRect = name.get_rect()
                    pygame.draw.rect(screen,(255,255,255),[mPos[0],mPos[1]-nameRect[3]-4,nameRect[2]+4,nameRect[3]+4])
                    pygame.draw.rect(screen,(0,0,0),[mPos[0]+1,mPos[1]-nameRect[3]-3,nameRect[2]+2,nameRect[3]+2])
                    screen.blit(name,[mPos[0]+2,mPos[1]-nameRect[3]-2])
                    if pressedRight:
                        Use = True
                        lastPos = mPos
                        current = i
        if Use:
            s = False
            for i in useOpt.buttons:
                if PIR(mPos,i):
                    s = True
                    i.active = True
                    if pressedLeft:
                        i.push(current)
                else:
                    i.active = False
            if s or PIR2(mPos,[current*34,0],[34,34]):
                useOpt.draw(lastPos)
            else:
                Use = 0
    
    player.cooldown-=1
        
    pygame.display.update()

    for i in range(len(enemies.elements)):
        if i>=len(enemies.elements):
            break
        if enemies.elements[i].hp<=0:
            enemies.elements[i].drop()
            enemies.take(i)

    if player.hp <= 0:
        done = True


    pressedRight = False
    pressedLeft = False

pygame.quit()
