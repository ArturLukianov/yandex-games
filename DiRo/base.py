import pygame
import random
import copy

NOUSABLE = ["collectible","book"]

class Item:
    def __init__(self, params):
        self.params = params

class Entity:
    def __init__(self, params):
        self.params = params
        if not self.params.get('max_hp'):
            self.params['max_hp'] = self.params['hp']
    def get_sum_atk(self):
        atk = self.params['atk']
        if self.params.get('inventory'):
            for it in self.params['inventory']:
                if it.params['type'] == 'weapon' and (it.params.get('use') and it.params['use'] == 1):
                    atk += it.params['atk']
        return atk
    def get_sum_def(self):
        res = self.params['def']
        if self.params.get('inventory'):
            for it in self.params['inventory']:
                if it.params['type'] == 'armor' and (it.params.get('use') and it.params['use'] == 1):
                    res += it.params['def']
        return res
    def unusesame(self, typ):
        for it in self.params['inventory']:
            if it.params['type'] == typ and (it.params.get('use') and it.params['use'] == 1):
                it.params['use'] = 0
    def checkcurse(self,typ):
        for it in self.params['inventory']:
            if it.params['type'] == typ and (it.params.get('use') and it.params.get('cursed')):
                return 0
        return 1
    def hit(self, atk):
        ratk = atk
        if ratk > 0:
            ratk -= self.get_sum_def()
            if ratk < 0:
                ratk = 0
        if ratk > 0:
            self.params['sadness'] = 1
        else:
            self.params['sadness'] = 0
        self.params['hp'] -= ratk
        if self.params['hp'] > self.params['max_hp']:
            self.params['hp'] = self.params['max_hp']
    def move(self, nx, ny, field, entities, items, effects):
        if self.params['x'] == nx and self.params['y'] == ny:
            return
        if(self.params.get('ghost') or
           field.field[nx][ny] == 0) and entities.entity_on_coords(nx, ny) == -1:
            self.params['x'] = nx
            self.params['y'] = ny
        elif entities.entity_on_coords(nx, ny) != -1:
            effects.effects.append(Effect({'type':'attack','x':nx,'y':ny}))
            entities.hit(self.get_sum_atk(),
                         entities.entity_on_coords(nx, ny),
                         items)
    
class EntityBank:
    def __init__(self, entities):
        self.entities = entities
    def entity_on_coords(self,x,y):
        res = -1
        for en in range(len(self.entities)):
            if self.entities[en].params['x'] == x and self.entities[en].params['y'] == y:
                res = en
        return res
    def hit(self, atk, ind, items):
        self.entities[ind].hit(atk)
        if self.entities[ind].params['hp'] <= 0:
            mon = random.randint(0, 100)
            ch = 100
            if self.entities[ind].params.get('chance'):
                ch = self.entities[ind].params['chance']
            if mon <= ch  and self.entities[ind].params.get('drop') and len(self.entities[ind].params['drop']):
                nitem = copy.deepcopy(random.choice(self.entities[ind].params['drop']))
                nitem.params['x'] = self.entities[ind].params['x']
                nitem.params['y'] = self.entities[ind].params['y']
                if nitem.params.get('roll'):
                    if nitem.params.get('atk'):
                        nitem.params['atk'] -= random.randint(-1, nitem.params['roll'] + 1)
                    if nitem.params.get('def'):
                        nitem.params['def'] -= random.randint(-1, nitem.params['roll'] + 1)
                    if nitem.params.get('eff'):
                        nitem.params['eff'] -= random.randint(-1, nitem.params['roll'] + 1)
                nitem.params['hidden'] = 1
                if random.randint(0,100) < 30:
                    nitem.params['cursed'] = 1
                if nitem.params['type'] in NOUSABLE:
                    nitem.params['cursed'] = 0
                    nitem.params['hidden'] = 0
                items.items .append(nitem)
            del self.entities[ind]
    def get_player(self):
        player = None
        for en in self.entities:
            if en.params.get('player'):
                player = en
        return player

class ItemBank:
    def __init__(self, items):
        self.items = items
    def get_item(self, x, y):
        res = None
        for it in self.items:
            if it.params['x'] == x and it.params['y'] == y:
                res = it
        return res
    def get_item_ind(self, x, y):
        res = -1
        co = 0
        for it in self.items:
            if it.params['x'] == x and it.params['y'] == y:
                res = co
            co += 1
        return res

class Specs:
    def __init__(self):
        self.specs = {}

class Effect():
    def __init__(self,params):
        self.params = params

class EffectBank():
    def __init__(self):
        self.effects = []
        

class Controller:
    def __init__(self):
        pass
    def control(self, state, field, entities,items, entity,specs,effects):
        nstate = state
        if entity.params.get('player'):
            _ = 0
            turn = 0
            while not _:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        nstate = 0
                        _ = 1
                    if e.type == pygame.KEYDOWN:
                        if state == 1:
                            nposd = (0,0)
                            if e.key == pygame.K_UP and not _:
                                nposd = (0, -1)
                                turn = 1
                            if e.key == pygame.K_DOWN and not _:
                                nposd = (0, 1)
                                turn = 1
                            if e.key == pygame.K_LEFT and not _:
                                nposd = (-1, 0)
                                turn = 1
                            if e.key == pygame.K_RIGHT and not _:
                                nposd = (1, 0)
                                turn = 1
                            if e.key == pygame.K_i and not _:
                                nstate = 2
                                specs.specs['cursor'] = 0
                                specs.specs['info'] = 0
                            if e.key == pygame.K_s and not _:
                                nstate = 3
                            if e.key == pygame.K_q and not _:
                                nstate = 10
                            if e.key == pygame.K_p and not _:
                                if items.get_item(entity.params['x'],
                                                  entity.params['y']) != None:
                                    if not entity.params.get('inventory'):
                                        entity.params['inventory'] = []
                                    if len(entity.params['inventory']) < 10:
                                        entity.params['inventory'].append(copy.deepcopy(
                                            items.get_item(entity.params['x'],
                                                  entity.params['y'])))
                                        ditem = items.get_item_ind(entity.params['x'],
                                                  entity.params['y'])
                                        del items.items[ditem]
                            entity.move(entity.params['x'] + nposd[0],
                                        entity.params['y'] + nposd[1],
                                        field,
                                        entities,
                                        items,
                                        effects)
                            _ = 1
                        if state == 2:
                            if e.key == pygame.K_q:
                                nstate = 101
                            if e.key == pygame.K_DOWN:
                                specs.specs['cursor'] = specs.specs['cursor'] + 1
                                if specs.specs['cursor'] >= 10:
                                    specs.specs['cursor'] = 0
                                specs.specs['info'] = 0
                            if e.key == pygame.K_UP:
                                specs.specs['cursor'] = specs.specs['cursor'] - 1
                                if specs.specs['cursor'] < 0:
                                    specs.specs['cursor'] = 9
                                specs.specs['info'] = 0
                            if e.key == pygame.K_RIGHT:
                                specs.specs['info'] = 1
                            if e.key == pygame.K_LEFT:
                                specs.specs['info'] = 0
                            if e.key == pygame.K_u:
                                if specs.specs['cursor'] < len(entity.params['inventory']) and not entity.params['inventory'][specs.specs['cursor']].params.get('none'):
                                    if entity.params['inventory'][specs.specs['cursor']].params['type'] not in NOUSABLE:
                                        if not entity.params['inventory'][specs.specs['cursor']].params.get('use'):
                                            entity.params['inventory'][specs.specs['cursor']].params['use'] = 0
                                        if entity.params['inventory'][specs.specs['cursor']].params['use'] == 0:
                                            if entity.params['inventory'][specs.specs['cursor']].params['type'] == 'potion':
                                                if entity.params['inventory'][specs.specs['cursor']].params['eff'] == 'heal':
                                                    entity.hit(-entity.params['inventory'][specs.specs['cursor']].params['str'])
                                                    for i in range(specs.specs['cursor'], len(entity.params['inventory']) - 1):
                                                        entity.params['inventory'][i] = copy.deepcopy(entity.params['inventory'][i + 1])
                                                    del entity.params['inventory'][len(entity.params['inventory']) - 1]
                                            else:
                                                if entity.checkcurse(entity.params['inventory'][specs.specs['cursor']].params['type']):
                                                    entity.params['inventory'][specs.specs['cursor']].params['hidden'] = 0
                                                    entity.unusesame(entity.params['inventory'][specs.specs['cursor']].params['type'])
                                                    entity.params['inventory'][specs.specs['cursor']].params['use'] = 1
                                        else:
                                            entity.params['inventory'][specs.specs['cursor']].params['use'] = 0
                            if e.key == pygame.K_d:
                                if specs.specs['cursor'] < len(entity.params['inventory']) and not entity.params['inventory'][specs.specs['cursor']].params.get('cursed'):
                                    nitem = copy.deepcopy(entity.params['inventory'][specs.specs['cursor']])
                                    nitem.params['x'] = entity.params['x']
                                    nitem.params['y'] = entity.params['y']
                                    nitem.params['use'] = 0
                                    items.items.append(nitem)
                                    for i in range(specs.specs['cursor'], len(entity.params['inventory']) - 1):
                                        entity.params['inventory'][i] = copy.deepcopy(entity.params['inventory'][i + 1])
                                    del entity.params['inventory'][len(entity.params['inventory']) - 1]
                            _ = 1
                        if state == 3:
                            if e.key == pygame.K_q:
                                nstate = 101 
                            _ = 1
                        if state == 10:
                            if e.key == pygame.K_q:
                                nstate = 0
                            if e.key == pygame.K_p:
                                nstate = 11
                            _ = 1
                        if state == 6:
                            if e.key == pygame.K_q:
                                nstate = 10 
                            _ = 1
        elif not entity.params.get('int') or entity.params['int'] == 'aggro':
            if state == 1:
                npos = (0,0)
                player = entities.get_player()
                if player != None:
                    if entity.params['x'] < player.params['x']:
                        npos = (1,0)
                    if entity.params['x'] > player.params['x']:
                        npos = (-1,0)
                    if entity.params['y'] < player.params['y']:
                        npos = (0,1)
                    if entity.params['y'] > player.params['y']:
                        npos = (0,-1)
                entity.move(entity.params['x'] + npos[0],
                            entity.params['y'] + npos[1],
                            field,
                            entities,
                            items,
                            effects)
        elif entity.params['int'] == 'random':
            if state == 1:
                npos = (0,0)
                r = random.randint(0,3)
                if r == 0:
                    npos = (1,0)
                if r == 1:
                    npos = (-1,0)
                if r == 2:
                    npos = (0,1)
                if r == 3:
                    npos = (0,-1)
                entity.move(entity.params['x'] + npos[0],
                                entity.params['y'] + npos[1],
                                field,
                                entities,
                                items,
                            effects)
        elif entity.params['int'] == 'static':
            if state == 1:
                if entity.params.get('sadness'):
                    npos = (0,0)
                    player = entities.get_player()
                    if player != None:
                        if entity.params['x'] < player.params['x']:
                            npos = (1,0)
                        if entity.params['x'] > player.params['x']:
                            npos = (-1,0)
                        if entity.params['y'] < player.params['y']:
                            npos = (0,1)
                        if entity.params['y'] > player.params['y']:
                            npos = (0,-1)
                    entity.move(entity.params['x'] + npos[0],
                                entity.params['y'] + npos[1],
                                field,
                                entities,
                                items,
                                effects)
        elif entity.params['int'] == 'item_hunter':
            pass
        return nstate
class Field:
    def __init__(self):
        self.field = []
        for i in range(30):
            b = []
            for j in range(30):
                if i == 0 or j == 0 or i == 29 or j == 29:
                    b.append(1)
                else:
                    b.append(0)
            self.field.append(b)

class Graphics:
    def __init__(self, screen, TEXTURE):
        self.screen = screen
        self.font = pygame.font.Font('font.ttf', 10)
        self.bigfont = pygame.font.Font('font.ttf', 100)
        self.midfont = pygame.font.Font('font.ttf', 50)
        self.TEXTURE = TEXTURE
    def draw_field(self, field):
        for i in range(len(field.field)):
            for j in range(len(field.field[i])):
                if field.field[i][j] == 1:
                    self.screen.blit(self.TEXTURE["wall"], (j * 20, i * 20))
                else:
                    self.screen.blit(self.TEXTURE["empty"], (j * 20, i * 20))
    def draw_entity(self, entity):
        self.screen.blit(self.TEXTURE[entity.params['texture']],
                         (entity.params['x'] * 20, entity.params['y'] * 20))
    def draw_item_info(self, ind, item):
        pygame.draw.rect(self.screen,(0,0,0),(110, 30 + ind * 20, 70, 50))
        pygame.draw.rect(self.screen,(150,150,150),(110, 30 + ind * 20, 70, 50),1)
        pygame.draw.rect(self.screen,(0,0,0),(190, 30 + ind * 20, 40, 40))
        pygame.draw.rect(self.screen,(150,150,150),(190, 30 + ind * 20, 40, 40),1)
        itext = self.TEXTURE['none']
        if item.params.get('none'):
            testso = self.font.render('None',False, (200,100,100),(0,0,0))
            self.screen.blit(testso,(112,31 + ind * 20))
        else:
            itext = self.TEXTURE['defaultitem']
            if item.params.get('texture'):
                itext = self.TEXTURE[item.params['texture']]
            if item.params.get('cursed') and not item.params.get('hidden'):
                    testso = self.font.render('cursed',False, (200,100,100),(0,0,0))
                    self.screen.blit(testso,(112,61 + ind * 20))
            if item.params.get('use') and item.params['use'] == 1:
                testso = self.font.render('using',False, (100,200,100),(0,0,0))
                self.screen.blit(testso,(112,51 + ind * 20))
            #print(item.params)
            if(item.params.get('hidden') and item.params['hidden'] == 1):
                testso = self.font.render("???",False, (200,100,100),(0,0,0))
                self.screen.blit(testso,(112,31 + ind * 20))
            else:
                
                if item.params['type'] == 'weapon':
                    testso = self.font.render('atk ' + str(item.params['atk']),False, (100,100,200),(0,0,0))
                    self.screen.blit(testso,(112,41 + ind * 20))
                elif item.params['type'] == 'armor':
                    testso = self.font.render('def ' + str(item.params['def']),False, (100,100,200),(0,0,0))
                    self.screen.blit(testso,(112,41 + ind * 20))
                elif item.params['type'] == 'book':
                    pygame.draw.rect(self.screen,(0,0,0),(190, 80 + ind * 20, 200, 200))
                    pygame.draw.rect(self.screen,(150,150,150),(190, 80 + ind * 20, 200, 200),1)
                    testso = self.font.render(str(item.params['desc']),False, (100,100,200),(0,0,0))
                    self.screen.blit(testso,(191,82 + ind * 20))
                    testso = self.font.render(item.params['type'],False, (200,100,100),(0,0,0))
                    self.screen.blit(testso,(112,31 + ind * 20))
                if item.params.get('cursed'):
                    testso = self.font.render(item.params['type'],False, (250,200,000),(0,0,0))
                    self.screen.blit(testso,(112,31 + ind * 20))
                else:
                    testso = self.font.render(item.params['type'],False, (200,100,100),(0,0,0))
                    self.screen.blit(testso,(112,31 + ind * 20))
        self.screen.blit(itext, (200, 40 + ind * 20))
    def draw_inventory(self, inventory, cpos):
        pygame.draw.rect(self.screen,(0,0,0),(10, 10, 100, 20))
        pygame.draw.rect(self.screen,(150,150,150),(10, 10, 100, 20),1)
        testso = self.font.render('Inventory:',False, (200,200,200),(0,0,0))
        self.screen.blit(testso,(12,11))
        for i in range(10):
            color = (50,50,50)
            pygame.draw.rect(self.screen,(0,0,0),(10, i * 20 + 30, 100, 20))
            if i < len(inventory):
                color = (150,150,150)
                if inventory[i].params.get('use') and inventory[i].params['use'] == 1:
                    color = (100, 200, 100)
                testso = self.font.render(inventory[i].params['name'],False, color,(0,0,0))
                self.screen.blit(testso,(12, i * 20 + 30))
            if cpos == i:
                color =  (150,0,150)
            pygame.draw.rect(self.screen,color,(10, i * 20 + 30, 100, 20),1)
    def draw_stats(self, player):
        pygame.draw.rect(self.screen,(0,0,0),(10, 10, 100, 100))
        pygame.draw.rect(self.screen,(150,150,150),(10, 10, 100, 100),1)
        
        testso = self.font.render('DEF: ' + str(player.get_sum_def()),False, (100,200,100),(0,0,0))
        self.screen.blit(testso,(12,56))
        testso = self.font.render('ATK: ' + str(player.get_sum_atk()),False, (100,100,200),(0,0,0))
        self.screen.blit(testso,(12,41))
        testso = self.font.render('HP: ' + str(player.params['hp']) + "/" + str(player.params['max_hp']),False, (200,100,100),(0,0,0))
        self.screen.blit(testso,(12,26))
        testso = self.font.render('Stats:',False, (200,200,200),(0,0,0))
        self.screen.blit(testso,(12,11))
    def draw_item(self, item):
        tnum = "defaultitem"
        if item.params.get('texture'):
            tnum = item.params['texture']
        self.screen.blit(self.TEXTURE[tnum],
                         (item.params['x'] * 20, item.params['y'] * 20))
    def draw_menu(self,menu):
        if menu == 'main':
            pygame.draw.rect(self.screen,(0,0,0),(10, 10, 400, 400))
            pygame.draw.rect(self.screen,(150,150,150),(10, 10, 400, 400),10)
            testso = self.bigfont.render('DiRo',False, (200,200,200),(0,0,0))
            self.screen.blit(testso,(20,20))
            testso = self.font.render('v0.3.1a',False, (200,200,200),(0,0,0))
            self.screen.blit(testso,(250,130))
            testso = self.midfont.render('[Q]uit',False, (000,200,200),(0,0,0))
            self.screen.blit(testso,(20,200))
            testso = self.midfont.render('[P]lay',False, (200,200,000),(0,0,0))
            self.screen.blit(testso,(20,140))
            tlist = [self.TEXTURE[i] for i in self.TEXTURE]
            self.screen.blit(random.choice(tlist),(500,500))
            self.screen.blit(random.choice(tlist),(520,500))
            self.screen.blit(random.choice(tlist),(480,500))
    def game_over(self):
        self.screen.fill((0,0,0))
        testso = self.midfont.render('Game over...',False, (200,100,100),(0,0,0))
        self.screen.blit(testso,(10,10))
        testso = self.font.render('[Q]uit',False, (200,100,100),(0,0,0))
        self.screen.blit(testso,(250,100))
    def draw_frame(self,field,entities,items,state,specs):
        self.screen.fill((0,0,0))
        self.draw_field(field)
        for it in items.items:
            self.draw_item(it)
        for en in entities.entities:
            self.draw_entity(en)
        if state == 2:
            self.draw_inventory(
                entities.get_player().params['inventory'],
                specs.specs['cursor']
                )
            if specs.specs.get('info') and specs.specs['info'] == 1:
                ilem = Item({'none':1})
                if specs.specs['cursor'] < len(entities.get_player().params['inventory']):
                    ilem = entities.get_player().params['inventory'][specs.specs['cursor']]
                self.draw_item_info(specs.specs['cursor'],ilem)
        if state == 3:
            self.draw_stats(entities.get_player())
        if state == 10:
            self.screen.fill((0,0,0))
            self.draw_menu('main')
        if state == 6:
            self.game_over()
        pygame.display.update()
    def draw_effect(self, effect):
        if effect.params['type'] == 'attack':
            pygame.draw.rect(self.screen,(250,50,50),(effect.params['x'] * 20, effect.params['y'] * 20, 20, 20))
        pygame.display.update()
    
