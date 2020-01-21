import pygame
from math import sqrt, sin, cos, radians

def dist(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return sqrt(x * x + y * y)

def create_ray(x, ppos, p_dir):
    angle = Camera_view / W * (W - x) + Camera_view / 2 - p_dir
    angle = radians(angle)
    p0 = [ppos[0], ppos[1]]
    p1 = [sin(angle) * 9999 + ppos[0], cos(angle) * 9999 + ppos[1]]
    return p0, p1

def get_abc(p1, p2):
    a = 1
    b = -(p1[0] - p2[0]) / (p1[1] - p2[1])
    c = -(p1[0] + b * p1[1])
    return a, b, c

W = 200
H = 100

def coll_circle_line(p1, p2, o, r):
    if p1[0] == p2[0]:
        p1[0], p1[1] = p1[1], p1[0]
        p2[0], p2[1] = p2[1], p2[0]
        o[0], o[1] = o[1], o[0]
    a = dist(p1, p2)
    b = dist(p1, o)
    c = dist(p2, o)
    p = (a + b + c) / 2
    s = sqrt(p * (p - a) * (p - b) * (p - c))
    h = s / a * 2
    if h <= r:
        if not p2[0]-p1[0] == 0:
            a = (p2[1]-p1[1])/(p2[0]-p1[0])
        else:
            a=9999999999999999
        b = p1[1]-a*p1[0]
        aa = a ** 2 + 1
        bb = 2 * (o[0] - (b - o[1]) * a)
        cc = (b - o[1]) ** 2 - r ** 2 + o[0] ** 2
        d = bb ** 2 - 4 * aa * cc
        d = sqrt(d)
        x1 = (bb + d) / (2 * aa)
        x2 = (bb - d) / (2 * aa)
        xx1 = x1 > min(p1[0], p2[0]) and x1 < max(p1[0], p2[0])
        xx2 = x2 > min(p1[0], p2[0]) and x2 < max(p1[0], p2[0])
        y1 = a * x1 + b
        y2 = a * x2 + b
        return xx1 or xx2
    return False

def find_a_b_c(p1, p2):
    a = 1
    b = (p2[0] - p1[0]) / (p1[1] - p2[1])
    c = -p1[0] - b * p1[1]
    return a, b, c

screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)

done = False

def coll_line_line(p11,p12,p21,p22):
    if not p12[0]-p11[0] == 0:
            a1 = (p12[1]-p11[1])/(p12[0]-p11[0])
    else:
        a1=9999999999999999
    b1 = p11[1]-a1*p11[0]
    if not p22[0]-p21[0] == 0:
        a2 = (p22[1]-p21[1])/(p22[0]-p21[0])
    else:
        a2=9999999999999999
    b2 = p21[1]-a2*p21[0]
    y11 = a1*p21[0]+b1
    y12 = a1*p22[0]+b1
    y21 = a2*p11[0]+b2
    y22 = a2*p12[0]+b2
    i = (y11>p21[1] and y12<p22[1]) or (y11<p21[1] and y12>p22[1])
    j = (y21>p11[1] and y22<p12[1]) or (y21<p11[1] and y22>p12[1])
    return i and j

def coll_line_line_point(p11, p12, p21, p22):
    if not p12[0]-p11[0] == 0:
            a1 = (p12[1]-p11[1])/(p12[0]-p11[0])
    else:
        a1=9999999999999999
    b1 = p11[1]-a1*p11[0]
    if not p22[0]-p21[0] == 0:
        a2 = (p22[1]-p21[1])/(p22[0]-p21[0])
    else:
        a2=9999999999999999
    b2 = p21[1]-a2*p21[0]
    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1
    return (x, y)

def find_pixel(x, ppos, objects, p_dir, characters, items):
    ray = create_ray(x, ppos, p_dir)
    d = []
    for i in objects + characters + items:
        if coll_line_line(ray[0], ray[1], i.get_p1(), i.get_p2()):
            point = coll_line_line_point(ray[0], ray[1], i.get_p1(), i.get_p2())
            tex = i.get_tex()
            tex_size = i.get_tex_size()
            dist_to_point = dist(ppos, point)
            dist_to_p1 = dist(point, i.get_p1())
            t = i.get_type()
            width = i.width
            name = ""
            if t == 2:
                name = characters.index(i)
            d.append((dist_to_point, tex, dist_to_p1, t, tex_size, width, name))
        else:
            d.append((99999, 0))
    try:
        d = sorted(d)
    except:
        pass
    queue = []
    for i in d:
        if i[0] > 1:
            queue.append(i)
        if len(i) < 3:
            break
        if not i[3]:
            break
    queue2 = []
    if len(queue) > 1 and queue[-1][1] == 0:
        queue.pop()
    if queue[0][1]:
        for i in queue:
            tex = i[1]
            pixel = i[2] * i[4][0] / i[5]
            pixel = int(pixel)
            pixel %= i[4][0]
            if i[0] < 20 and i[0] != 0:
                l = H / i[0]# / Tex_w * i[4][1]
                h = H / i[0] / Tex_w * i[4][1]
                h = int(h)
                l = int(l)
                tex = pygame.transform.scale(tex, (int(i[4][0]), int(h * 2)))
                queue2.append([1, tex, H // 2 + l - h * 2, pixel, l * 2, i[4][1]])
                if abs(W // 2 - x) < 10 and t == 2 and i[0] < 2:
                    global hint
                    hint = "Press [E] to talk to " + characters[i[6]].name
                    global talkative
                    talkative = i[6]
        if len(queue2) == 0:
            return (0, )
        return queue2
    else:
        return (0, )

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.deg = 0
        self.v = 0
        self.inv = []
        self.rotate_v = 0

#objects = [[[-3, -3], [-3, 3], "wall", 0],
#           [[-3, 3], [3.001, 3], "wall", 0],
#           [[3.001, 3], [3.001, -3], "wall", 0],
#           [[3.001, -3], [-3, -3], "wall", 0]]

#characters = [[[10, 10], [13, 10], "test", 2]]

#characters = 

Tex_w = 32

player = Player([10, 0])

textures = {"wall":[pygame.image.load("wall.png"), [32, 32]],
            "wooden_wall":[pygame.image.load("wooden_wall.png"), [32, 32]],
            "test":[pygame.image.load("tester.png"), [32, 32]],
            "sword":[pygame.image.load("sword_on_floor.png"), [16, 16]]}

Camera_view = 45

p_dir = 0

p_rotate_v = 0

p_v = 0
pr = 1.1

text = ""

class Character():
    def __init__(self, pos, deg, tex, name):
        self.pos = pos
        self.deg = deg
        self.tex = textures[tex]
        self.type = 2
        self.width = self.tex[1][0] / Tex_w
        self.calc_points()
        self.name = name

    def talk(self):
        global mode
        mode = 2
        global text
        text = "Hi"

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]
        self.calc_points()

    def calc_points(self):
        self.p1 = []
        self.p2 = []
        self.p1.append(self.width / 2 * cos(radians(self.deg + 90)) + self.pos[0])
        self.p1.append(self.width / 2 * sin(radians(self.deg + 90)) + self.pos[1])
        self.p2.append(self.width / 2 * cos(radians(self.deg - 90)) + self.pos[0])
        self.p2.append(self.width / 2 * sin(radians(self.deg - 90)) + self.pos[1])

    def get_tex(self):
        return self.tex[0]

    def get_tex_size(self):
        return self.tex[1]

    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2

    def get_type(self):
        return self.type

class Wall():
    def __init__(self, pos, deg, tex, t, inv):
        self.pos = pos
        self.deg = deg
        self.tex = textures[tex]
        self.type = t
        self.calc_points()
        self.inv = inv
        self.width = self.tex[1][0] / Tex_w

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]
        self.calc_points()

    def calc_points(self):
        self.p1 = []
        self.p2 = []
        self.p1.append(self.tex[1][0] / Tex_w / 2 * cos(radians(self.deg + 90)) + self.pos[0])
        self.p1.append(self.tex[1][0] / Tex_w / 2 * sin(radians(self.deg + 90)) + self.pos[1])
        self.p2.append(self.tex[1][0] / Tex_w / 2 * cos(radians(self.deg - 90)) + self.pos[0])
        self.p2.append(self.tex[1][0] / Tex_w / 2 * sin(radians(self.deg - 90)) + self.pos[1])

    def get_tex(self):
        return self.tex[0]

    def get_tex_size(self):
        return self.tex[1]

    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2

    def get_type(self):
        return self.type

class Item():
    def __init__(self, pos, deg, tex, stats, t):
        self.name = tex
        self.pos = pos
        self.deg = deg
        self.tex = textures[tex]
        self.type = 1
        self.calc_points()
        self.stats = stats
        self.t = t
        self.width = self.tex[1][0] / Tex_w

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]
        self.calc_points()

    def calc_points(self):
        self.p1 = []
        self.p2 = []
        self.p1.append(self.tex[1][0] / Tex_w / 2 * cos(radians(self.deg + 90)) + self.pos[0])
        self.p1.append(self.tex[1][0] / Tex_w / 2 * sin(radians(self.deg + 90)) + self.pos[1])
        self.p2.append(self.tex[1][0] / Tex_w / 2 * cos(radians(self.deg - 90)) + self.pos[0])
        self.p2.append(self.tex[1][0] / Tex_w / 2 * sin(radians(self.deg - 90)) + self.pos[1])

    def get_tex(self):
        return self.tex[0]

    def get_tex_size(self):
        return self.tex[1]

    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2

    def get_type(self):
        return self.type

class ItemInv:
    def __init__(self, name, stats, t):
        self.name = name
        self.stats = stats
        self.t = t


f = open("walls.txt")
objects = []
r = f.read()
f.close()
r = r.split("\n")
for i in r:
    f = i.split()
    objects.append(Wall([float(f[0]), float(f[1])], float(f[2]), f[3], 0, 1))

#objects = [Wall([1, 1], 90, "wall", 0, 1),]
characters = [Character([2, 2], 0, "test", "test")]
items = [Item([3, 3], 0, "sword", {"atk":10, "w":2, "price":10}, "sword"),
         Item([4, 4], 0, "sword", {}, "sword")]

hint = "Press [F] to pay respect"

pygame.font.init()

font = pygame.font.SysFont("Arial", 14)

hint_pos = [W // 2, H // 4 * 3]

mode = 0

talkative = -1

def show_hint(hint):
    hint = hint.split("\n")
    for i in range(len(hint)):
        text = font.render(hint[i], False, (255, 255, 255))
        size = text.get_rect()[2::]
        pos = [0, 0]
        pos[0] = hint_pos[0] - size[0] // 2
        pos[1] = hint_pos[1] - size[1] // 2 + i * 16
        screen.blit(text, pos)

inv_choice = 0

while not done:
    if mode == 0:
        if player.rotate_v != 0:
            player.deg += player.rotate_v
    #for i in range(len(items)):
    #    items[i].deg -= 3
    #    items[i].calc_points()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN:
            if e.scancode == 77:
                player.rotate_v = 1
            elif e.scancode == 75:
                player.rotate_v = -1
            elif e.scancode == 17:
                player.v = 0.05
            elif e.scancode == 31:
                player.v = -0.05
        if e.type == pygame.KEYUP:
            if e.scancode == 77 and player.rotate_v > 0:
                player.rotate_v = 0
            elif e.scancode == 75 and player.rotate_v < 0:
                player.rotate_v = 0
            elif e.scancode == 17 and player.v > 0:
                player.v = 0
            elif e.scancode == 31 and player.v < 0:
                player.v = 0
            elif e.scancode == 18:
                if mode == 0:
                    if "pick up" in hint:
                        ind = -1
                        for i in range(len(items)):
                            if dist(items[i].pos, player.pos) < 2:
                                ind = i
                                break
                        if ind >= 0:
                            player.inv.append(ItemInv(items[ind].name, items[ind].stats, items[ind].t))
                            del items[ind]
                    elif "talk" in hint:
                        characters[talkative].talk()
                elif mode == 2:
                    mode = 0
            elif e.scancode == 23:
                if mode == 0:
                    mode = 1
                elif mode == 1:
                    mode = 0
            elif e.scancode == 72:
                if mode == 1 and len(player.inv) > 0:
                    inv_choice -= 1
                    inv_choice %= len(player.inv)
            elif e.scancode == 80:
                if mode == 1 and len(player.inv) > 0:
                    inv_choice += 1
                    inv_choice %= len(player.inv)
    talkative = -1
    hint = ""
    
    if mode == 0:
        screen.fill((125, 125, 255))
    elif mode == 1:
        screen.fill((0, 0, 0))

    if mode == 0:

        for i in items:
            if dist(i.pos, player.pos) < 2:
                hint = "Press [E] to pick up"

        if player.v != 0:
            px = cos(radians(player.deg + Camera_view)) * player.v
            py = sin(radians(player.deg + Camera_view)) * player.v
            player.pos[0] += px
            points = False
            for i in list(objects):
                if i.inv:
                    a = coll_circle_line(i.get_p1(), i.get_p2(), player.pos, pr)
                    if a:
                        points = True
                        break
            if points:
                player.pos[0] -= px
            player.pos[1] += py
            points = False
            for i in list(objects):
                if i.inv:
                    a = coll_circle_line(i.get_p1(), i.get_p2(), player.pos, pr)
                    if a:
                        points = True
                        break
            if points:
                player.pos[1] -= py
        #pygame.draw.rect(screen, (125, 125, 0), (0, H // 2, W, H // 2))
        for i in range(H // 2):
            c = 125 / (H // 2) * i / 2
            c = int(c + 50)
            pygame.draw.line(screen, (c, c - 50, 0), (0, H // 2 + i), (W, H // 2 + i))

        for i in range(W):
            try:
                d = find_pixel(i, player.pos, objects, player.deg, characters, items)
                d = list(reversed(d))
                if d[0]:
                    for j in d:
                        screen.blit(j[1], (i, j[2]), (j[3], 0, 1, j[4]))
            except:
                pass

        if hint != "":
            show_hint(hint)
    elif mode == 1:
        pygame.draw.rect(screen, (50, 50, 50), (0, int(inv_choice * H / 4), int(W / 3), int(H / 4)))
        for i in range(4):
            pygame.draw.rect(screen, (255, 255, 255), (0, int(i * H / 4), int(W / 3), int(H / 4)), 1)
        for j in range(min(len(player.inv), 4)):
            text = player.inv[j].name
            text = font.render(text, 0, (255, 255, 255))
            size = text.get_rect()[2::]
            pos = [5, int((j + 1) * H / 4 - 23)]
            screen.blit(text, pos)
    elif mode == 2:
        pygame.draw.rect(screen, (255, 255, 255), (0, H // 2, W, H // 2))
        pygame.draw.rect(screen, (0, 0, 0), (1, H // 2 + 1, W - 2, H // 2 - 2))
        text_tex = font.render(text, False, (255, 255, 255))
        screen.blit(text_tex, (10, H // 2 + 10))
    pygame.display.update()
pygame.quit()
