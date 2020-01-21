import pygame
from base import *
import random
import copy
import xml.etree.cElementTree as ET
import os

numtags = ['hp','atk','def','chance','level','roll','str']

TEXTURE = {}
reservedt = ["wall","empty","defaultitem","player","none"]
for r in reservedt:
    TEXTURE[r] = pygame.image.load("Textures/" + r + ".png")

preentities = [[] for i in range(100)]
preitems = [[] for i in range(100)]

maxlvl = 0

ERES = os.path.join('resourses.xml')
tree = ET.ElementTree(file=ERES)
root = tree.getroot()
for cen in root[0]:
    pare = {}
    lvl = 0
    for att in cen:
        if att.tag == "drop":
            rd = []
            for qw in att:
                rt = {}
                for ae in qw:
                    if ae.tag in numtags:
                        rt[ae.tag] = int(ae.text)
                    else:
                        rt[ae.tag] = ae.text
                if rt.get('texture'):
                    TEXTURE[rt['texture']] = pygame.image.load("Textures/" + rt['texture'] + ".png")
                rd.append(Item(rt))
                ilvl = 99
                if rt.get('level'):
                    ilvl = rt['level']
                preitems[ilvl].append(Item(rt))
            pare['drop'] = rd
        elif att.tag in numtags:
            pare[att.tag] = int(att.text)
        else:
            pare[att.tag] = att.text
    lvl = pare['level']
    TEXTURE[pare['texture']] = pygame.image.load("Textures/" + pare['texture'] + ".png")
    maxlvl = max(maxlvl, lvl)
    preentities[lvl].append(Entity(pare))

for cen in root[1]:
    rt = {}
    for ae in cen:
        if ae.tag in numtags:
            rt[ae.tag] = int(ae.text)
        else:
            rt[ae.tag] = ae.text
    if rt.get('texture'):
        TEXTURE[rt['texture']] = pygame.image.load("Textures/" + rt['texture'] + ".png")
    ilvl = 99
    if rt.get('level'):
        ilvl = rt['level']
    preitems[ilvl].append(Item(rt))

sentities = EntityBank([
            Entity({
                 'atk':1,
                 'def':0,
                 'hp':10,
                 'max_hp':10,
                 'x':15,
                 'y':15,
                 'texture':'player',
                 'player':1,
                 'inventory':[]
                 })
            ])

sitems = ItemBank([])

entities = copy.deepcopy(sentities)
items = copy.deepcopy(sitems)

spawnp = [(1,1),(1,28),(28,1),(28,28)]

def spawn():
    for pos in spawnp:
        if random.randint(0,100) < 90:
            if entities.entity_on_coords(pos[0],pos[1]) != -1:
                continue
            o = preentities[random.randint(1, wavelvl)]
            while len(o) == 0:
                o = preentities[random.randint(1, wavelvl)]
            rmob = copy.deepcopy(random.choice(preentities[random.randint(1, wavelvl)]))
            rmob.params['x'] = pos[0]
            rmob.params['y'] = pos[1]
            entities.entities.append(rmob)
        else:
            o = preitems[random.randint(1, wavelvl)]
            while len(o) == 0:
                o = preitems[random.randint(1, wavelvl)]
            rmob = copy.deepcopy(random.choice(preitems[random.randint(1, wavelvl)]))
            rmob.params['x'] = pos[0]
            rmob.params['y'] = pos[1]
            if rmob.params.get('roll'):
                if rmob.params.get('atk'):
                    rmob.params['atk'] -= random.randint(-1, rmob.params['roll'] + 1)
                if rmob.params.get('def'):
                    rmob.params['def'] -= random.randint(-1, rmob.params['roll'] + 1)
                if rmob.params.get('eff'):
                    rmob.params['eff'] -= random.randint(-1, rmob.params['roll'] + 1)
            rmob.params['hidden'] = 1
            if random.randint(0,100) < 30:
                rmob.params['cursed'] = 1
            if rmob.params['type'] in NOUSABLE:
                rmob.params['hidden'] = 0
                rmob.params['cursed'] = 0
            items.items.append(rmob)

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("DiRo (2019)")
pygame.display.set_icon(pygame.image.load("icon.png"))
field = Field()
gui = Graphics(screen, TEXTURE)
controller = Controller()
state = 10
wave = 0
timer = 0
wavelvl = 1

specs = Specs()
effects = EffectBank()

while state > 0:
    if state == 1:
        timer += 1
        if timer >= wave:
            timer = 0
            wave += 100
            wavelvl += 1
            if wavelvl > maxlvl:
                wavelvl = maxlvl
            spawn()
    gui.draw_frame(field, entities,items, state, specs)
    for e in entities.entities:
        qstate = controller.control(state, field, entities,items,e,specs,effects)
        if e.params.get('player'):
            state = qstate
##        gui.draw_frame(field, entities,items, state, specs)
##        for effect in effects.effects:
##            gui.draw_effect(effect)
##            pygame.time.delay(100)
##            gui.draw_frame(field, entities,items, state, specs)
##        effects.effects = []
    if state > 100:
        state -= 100
    if state == 11:
        entities = copy.deepcopy(sentities)
        items = copy.deepcopy(sitems)
        wave = 0
        timer = 0
        wavelvl = 0
        field = Field()
        state = 1
    if entities.get_player() == None:
        entities = copy.deepcopy(sentities)
        items = copy.deepcopy(sitems)
        wave = 0
        timer = 0
        wavelvl = 0
        field = Field()
        state = 1
        state = 6
    

pygame.quit()
