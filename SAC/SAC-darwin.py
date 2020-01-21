import pygame as pg
import random


cell = [0 for i in range(256)]
ncell = []
ncell[:] = cell
cellh = [None for i in range(256)]
cellc = [256, 1, 1]


class CodeHandler():
    def __init__(self, memp):
        self.memp = memp

    def code(self, code):
        self.code = code

    def prepare(self):
        self.dataseg = {}
        self.codeseg = []
        self.infoseg = {'name':'noname', 'rcol':-1, 'gcol':-1, 'bcol':-1}
        self.constseg = {'memp':self.memp, 'codep':0, 'bfl':0, 'ctyp':cell[self.memp]}
        mode = 'nomode'
        for line in self.code:
            if line[0] == '~':
                mode = line[1:]
                continue
            if mode == 'data':
                self.dataseg[line[1:]] = 0
            elif mode == 'code':
                self.codeseg.append(line)
            elif mode == 'info':
                self.infoseg[line[1:].split()[0]] = line[1:].split()[1]
        self.ptrs = {}
        lnn = 0
        for line in self.codeseg:
            if line[0] == ':':
                self.ptrs[line[1:]] = lnn
            lnn += 1

    def value_parse(self, lne):
        val = 0
        if lne[0] == '@':
            if not lne[1:] in self.dataseg.keys():
                return None
            val = self.dataseg[lne[1:]]
        elif lne[0] == '%':
            if not lne[1:] in self.constseg.keys():
                return None
            val = self.constseg[lne[1:]]
        else:
            try:
                val = int(lne)
            except:
                return None
        return val

    def pointer_parse(self, lne):
        val = 0
        if lne[0] == '*':
            if not lne[1:] in self.ptrs.keys():
                return None
            val = self.ptrs[lne[1:]]
        else:
            try:
                val = int(lne)
            except:
                return None
        return val

    def run(self):
        if(self.constseg['codep'] < 0):
            self.prepare()
            self.constseg['codep'] = 0
        while self.constseg['codep'] != len(self.codeseg):
            tln = self.codeseg[self.constseg['codep']].split()
            #Commands
            #mov dst src
            if tln[0] == 'mov':
                to_name = ''
                if tln[1][0] == '@':
                    to_name = tln[1][1:]
                else:
                    print(self.constseg['codep'], "\t:value error")
                    self.constseg['codep'] = -2
                    return
                val = self.value_parse(tln[2])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                self.dataseg[to_name] = val
            #add dst n
            if tln[0] == 'add':
                to_name = ''
                if tln[1][0] == '@':
                    to_name = tln[1][1:]
                else:
                    print(self.constseg['codep'], "\t:value error")
                    self.constseg['codep'] = -2
                    return
                val = self.value_parse(tln[2])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                self.dataseg[to_name] += val
            #mul dst n
            if tln[0] == 'mul':
                to_name = ''
                if tln[1][0] == '@':
                    to_name = tln[1][1:]
                else:
                    print(self.constseg['codep'], "\t:value error")
                    self.constseg['codep'] = -2
                    return
                val = self.value_parse(tln[2])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                self.dataseg[to_name] *= val
            #div dst n
            if tln[0] == 'div':
                to_name = ''
                if tln[1][0] == '@':
                    to_name = tln[1][1:]
                else:
                    print(self.constseg['codep'], "\t:value error")
                    self.constseg['codep'] = -2
                    return
                val = self.value_parse(tln[2])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                self.dataseg[to_name] //= val
            #mod dst n
            if tln[0] == 'mod':
                to_name = ''
                if tln[1][0] == '@':
                    to_name = tln[1][1:]
                else:
                    print(self.constseg['codep'], "\t:value error")
                    self.constseg['codep'] = -2
                    return
                val = self.value_parse(tln[2])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                self.dataseg[to_name] %= val
            #dec dst n
            if tln[0] == 'dec':
                to_name = ''
                if tln[1][0] == '@':
                    to_name = tln[1][1:]
                else:
                    print(self.constseg['codep'], "\t:value error")
                    self.constseg['codep'] = -2
                    return
                val = self.value_parse(tln[2])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                self.dataseg[to_name] -= val
            #show src
            if tln[0] == 'show':
                val = self.value_parse(tln[1])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                print("[", val, "]")
            #rand dst
            if tln[0] == 'rand':
                to_name = ''
                if tln[1][0] == '@':
                    to_name = tln[1][1:]
                else:
                    print(self.constseg['codep'], "\t:value error")
                    self.constseg['codep'] = -2
                    return
                val = random.randint(0, 255)
                self.dataseg[to_name] = val
                self.constseg['codep'] += 1
                return
            #eql v1 v2
            if tln[0] == 'eql':
                val1 = self.value_parse(tln[1])
                if val1 == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                val2 = self.value_parse(tln[2])
                if val2 == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                if val1 == val2:
                    self.constseg['bfl'] = 1
                else:
                    self.constseg['bfl'] = 0
            #halt memp
            if tln[0] == 'halt':
                val = self.value_parse(tln[1])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                if val >= 256 or val < 0:
                    return
                if cell[val] != 0:
                    cellc[cell[val]] -= 1
                ncell[val] = 0
                cellh[val] = None
                self.constseg['codep'] += 1
                return
            #load memp
            if tln[0] == 'load':
                val = self.value_parse(tln[1])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                if val >= 256 or val < 0:
                    return
                if cell[val] != 0:
                    return
                cellc[cell[self.constseg['memp']]] += 1
                ncell[val] = cell[self.constseg['memp']]
                cellh[val] = CodeHandler(val)
                cellh[val].code(self.code)
                cellh[val].prepare()
                self.constseg['codep'] += 1
                return
            #prob dst src
            if tln[0] == 'prob':
                to_name = ''
                if tln[1][0] == '@':
                    to_name = tln[1][1:]
                else:
                    print(self.constseg['codep'], "\t:value error")
                    self.constseg['codep'] = -2
                    return
                val = self.value_parse(tln[2])
                if val == None:
                    print(self.constseg['codep'], '\t:value error')
                    self.constseg['codep'] = -2
                    return
                self.constseg['codep'] += 1
                if val >= 256 or val < 0:
                    return
                self.dataseg[to_name] = cell[val]
                return
            self.constseg['codep'] += 1
            #Go commands
            if tln[0] == 'go':
                val = self.pointer_parse(tln[1])
                if val == None:
                    print(self.constseg['codep'], '\t:pointer error')
                    self.constseg['codep'] = -2
                    return
                self.constseg['codep'] = val
            if tln[0] == 'goio':
                val = self.pointer_parse(tln[1])
                if val == None:
                    print(self.constseg['codep'], '\t:pointer error')
                    self.constseg['codep'] = -2
                    return
                if self.constseg['bfl'] == 1:
                    self.constseg['codep'] = val
            if tln[0] == 'gono':
                val = self.pointer_parse(tln[1])
                if val == None:
                    print(self.constseg['codep'], '\t:pointer error')
                    self.constseg['codep'] = -2
                    return
                if self.constseg['bfl'] == 0:
                    self.constseg['codep'] = val
        self.constseg['codep'] = -1

names = ["empty", "", ""]
col = [(50, 50, 50), (50, 200, 50), (200, 50, 200), (200, 50, 50)]
        
def init(prog1, prog2):
    global cell, ncell, cellh, names, cellc, col
    cellc = [256, 1, 1]
    cell = [0 for i in range(256)]
    ncell = []
    ncell[:] = cell
    cellh = [None for i in range(256)]
    
    p1 = random.randint(0, 255)
    p2 = random.randint(0, 255)
    while p1 == p2:
        p2 = random.randint(0, 255)
    cell[p1] = 1
    cellh[p1] = CodeHandler(p1)
    with open(prog1) as codefile:
        cellh[p1].code([i.strip().rstrip() for i in codefile.readlines()])
    cellh[p1].prepare()
    names[1] = cellh[p1].infoseg['name']
    if int(cellh[p1].infoseg['rcol']) != -1 and int(cellh[p1].infoseg['gcol']) != -1 and int(cellh[p1].infoseg['bcol']) != -1:
        col[1] = (int(cellh[p1].infoseg['rcol']),int(cellh[p1].infoseg['gcol']),int(cellh[p1].infoseg['bcol']))
    cell[p2] = 2
    cellh[p2] = CodeHandler(p2)
    with open(prog2) as codefile:
        cellh[p2].code([i.strip().rstrip() for i in codefile.readlines()])
    cellh[p2].prepare()
    names[2] = cellh[p2].infoseg['name']
    if int(cellh[p2].infoseg['rcol'] != -1) and int(cellh[p2].infoseg['gcol']) != -1 and int(cellh[p2].infoseg['bcol']) != -1:
        col[2] = (int(cellh[p2].infoseg['rcol']),int(cellh[p2].infoseg['gcol']),int(cellh[p2].infoseg['bcol']))

reinit = lambda:init('chaos.sac', 'meat.sac')
reinit()
pg.init()
screen = pg.display.set_mode((600, 600))
loop = 1
turn = 0
mturns = 1000

f1 = pg.font.Font(None, 16)
n1 = f1.render(names[1], 1, col[1])
n2 = f1.render(names[2], 1, col[2])
screen.blit(n1, (176, 0))
screen.blit(n2, (176, 16))
lres = []

points = [[256], [0], [0]]

while loop:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = 0
    screen.fill((0, 0, 0))
    screen.blit(n1, (176, 0))
    screen.blit(n2, (176, 16))
    c1 = f1.render(str(cellc[1]), 1, col[1])
    screen.blit(c1, (256, 0))
    c2 = f1.render(str(cellc[2]), 1, col[2])
    screen.blit(c2, (256, 16))
    for i in range(len(lres)):
        pg.draw.rect(screen, col[lres[i]], pg.Rect((i % 16) * 10, i // 16 * 10 + 176, 10, 10))
    lpoint = points[1][0]
    for i in range(1, len(points[1])):
        pg.draw.line(screen, col[1],((i - 1) * 16, 320 + 256 - points[1][i - 1]), ((i) * 16,  320 + 256 - points[1][i]), 4)
    lpoint = points[2][0]
    for i in range(1, len(points[2])):
        pg.draw.line(screen, col[2],((i - 1) * 16, 320 + 256 - points[2][i - 1]), ((i) * 16,  320 + 256 - points[2][i]), 4)
    for i in range(256):
        pg.draw.rect(screen, col[cell[i]], pg.Rect((i % 16) * 10, i // 16 * 10, 10, 10))
    ncell = cell
    for i in range(256):
        if cell[i]:
            cellh[i].run()
    turn += 1
    cell = ncell
    if(turn >= mturns or cellc[1] == 0 or cellc[2] == 0):
        if cellc[1] > cellc[2]:
            lres.append(1)
        elif cellc[2] > cell[1]:
            lres.append(2)
        else:
            lres.append(0)
        reinit()
        turn = 0
    points[1].append(cellc[1])
    if len(points[1]) > 32:
        points[1].pop(0)
    points[2].append(cellc[2])
    if len(points[2]) > 32:
        points[2].pop(0)
    pg.display.update()
pg.quit()
