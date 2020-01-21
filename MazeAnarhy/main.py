import pygame
from random import randint
import socket
import threading

field = []
enemies = []
bullets = []
nbl = 0
sock = None
f_h = 10
f_w = 10
s_h = 600
s_w = 600
nap = [
       [0,1],
       [1,0],
       [0,-1],
       [-1,0]
       ]
step = 50
msteps = 4
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
main_loop = True

p_x = 1
p_y = 1
p_n = 1
reft = 100
rtt = 0
cbip = dict()

def create_bullet(r):
    x,y,n = r
    bullets.append([x,y,n])

def new_client(conn, addr):
    global enemies
    data = conn.recv(1024)
    print(f"[Connected {addr[0]}]")
    print("[" + str(addr) + " : " + data.decode("UTF-8") + "]")
    if data.decode("UTF-8") != "CT":
        print("Error durning connection")
        conn.close()
        return
    conn.send(b"CA")
    print("[Connection OK]")
    conn_alive = 1
    while conn_alive:
        data = conn.recv(1024)
        if not data:
            conn_alive = 0
        sod = data.decode("UTF-8")
        if sod == "GM":
            conn.send('|'.join(['|'.join([str(j) for j in i]) for i in field]).encode())
        elif len(sod) > 2:
            lo = sod.split(':')
            cbip[addr] = [int(i) for  i in lo[0:2]]
            if(len(lo) > 2):
                create_bullet([int(i) for  i in lo[2:]])
            enemies = []
            for c in cbip:
                enemies.append((int(cbip[c][0]),int(cbip[c][1])))
            enemies.append((p_x,p_y))
            conn.send(('|'.join([str(r[0]) + ":" + str(r[1]) for r in enemies])).encode())
        else:
            conn.send(b"RE")
        #print("[" + str(addr) + " : " + sod + "]")
    conn.close()

def server_thread():
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(10)
    while True:
        conn,addr = sock.accept()
        threading.Thread(target=new_client, args=(conn,addr)).start()

def client_thread():
    global enemies,bullets,nbl,bl
    conn_alive = 1
    while conn_alive:
        if nbl == 1:
            nbl = 0
            sock.send((str(p_x) + ":" + str(p_y)+ ":" + str(bl[0])+ ":" + str(bl[1])+ ":" + str(bl[2])).encode())
        else:
            sock.send((str(p_x) + ":" + str(p_y)).encode())
        data = sock.recv(1024)
        if not data:
            conn_alive = 0
            print("Connection closed")
        sr = data.decode("UTF-8")
        enemies = [(int(e.split(':')[0]),int(e.split(':')[1])) for e in sr.split('|')]
        #print("[Server : " + data.decode("UTF-8") + "]")
    sock.close()

tp = input("Server or Client? [s/C] ")

if tp.lower() == "s":
    enemies = []
    for c in cbip:
        enemies.append(cbip[c])
    enemies.append((p_x,p_y))
    threading.Thread(target=server_thread).start()
else:
    sock = socket.socket()
    ip = input()
    sock.connect((ip, 9090))
    conn_alive = True
    sock.send(b"CT")
    data = sock.recv(1024).decode("UTF-8")
    if data == "CA":
        sock.send(b"GM")
        data = sock.recv(1024).decode("UTF-8").split('|')
        pn = 0
        for i in range(f_h):
            bu = []
            for j in range(f_w):
                bu.append(int(data[pn]))
                pn += 1
            field.append(bu)
        threading.Thread(target=client_thread).start()
pls = [
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       [[]],
       ]

for i in range(msteps):
    pls[0].append([(step * i,step * i),
                   (step * (i + 1),step * (i + 1)),
                   (step * (i + 1),s_h - step * (i + 1)),
                   (step * i,600 - step * i)])

for i in range(msteps):
    pls[1].append([(step * (i + 1), step * (i + 1)),
                   (s_w - step * (i + 1), step * (i + 1)),
                   (s_w - step * (i + 1),s_w - step * (i + 1)),
                   (step * (i + 1),s_w - step * (i + 1))])

for i in range(msteps):
    pls[2].append([(s_w - step * i, step * i),
                   (s_w - step * (i + 1), step * (i + 1)),
                   (s_w - step * (i + 1),s_w - step * (i + 1)),
                   (s_w - step * i,s_w - step * i)])

for i in range(msteps):
    pls[3].append([(step * i, s_h - step * i),
                   (step * (i + 1), s_w - step * (i + 1)),
                   (s_w - step * (i + 1),s_w - step * (i + 1)),
                   (s_w - step * i,s_w - step * i)])

for i in range(msteps):
    pls[4].append([(0, step * (i + 1)),
                   (step * (i + 1), step * (i + 1)),
                   (step * (i + 1),s_w - step * (i + 1)),
                   (0,s_w - step * (i + 1))])
for i in range(msteps):
    pls[5].append([(s_w, step * (i + 1)),
                   (s_w - step * (i + 1), step * (i + 1)),
                   (s_w - step * (i + 1),s_w - step * (i + 1)),
                   (s_w,s_w - step * (i + 1))])

for i in range(msteps):
    pls[6].append([(0, s_h - step * (i + 1)),
                   (step * (i + 1), s_h - step * (i + 1)),
                   (step * i,s_h - step * i),
                   (0,s_h - step * i)])

for i in range(msteps):
    pls[7].append([(s_h, s_h - step * (i + 1)),
                   (s_h - step * (i + 1), s_h - step * (i + 1)),
                   (s_h - step * i,s_h - step * i),
                   (s_h,s_h - step * i)])

for i in range(msteps):
    pls[8].append([(step * i, step * i),
                   (s_h - step * i,step * i),
                   (s_h - step * (i + 1), step * (i + 1)),
                   (step * (i + 1), step * (i + 1))
                   ])
    
for i in range(msteps):
    pls[9].append([(0, step * (i + 1)),
                   (step * (i + 1), step * (i + 1)),
                   (step * i,step * i),
                   (0,step * i)])

for i in range(msteps):
    pls[10].append([(s_h, step * (i + 1)),
                   (s_h - step * (i + 1), step * (i + 1)),
                   (s_h - step * i,step * i),
                   (s_h,step * i)])

if tp == "s":
    for i in range(f_h):
        b = []
        for j in range(f_w):
            if i == 0 or i == f_h - 1 or j == 0 or j == f_w - 1 or (randint(0,100) < 10):
                b.append(1)
            else:
                b.append(0)
        field.append(b)
print('\n'.join([' '.join([str(j) for j in i]) for i in field]))
pygame.init()
screen = pygame.display.set_mode((s_w, s_h))

def hwhite(h):
    m = 5 - h
    return (50 * m, 50 * m, 50 * m)

def hblue(h):
    m = 5 - h
    return (0, 0, 50 * m)

def hred(h):
    m = 5 - h
    return (50 * m, 0, 0)

def okcoord(coord):
    if coord < 0 or coord >= f_h:
        return 0
    return 1

def okenemy(x,y):
    if (x,y) in enemies:
        return 1
    return 0

def okbullet(x,y):
    ok = 0
    for e in bullets:
        if e[0] == x and e[1] == y:
            ok = 1
            break
    return ok


def draw_frame(x, y, n):
    global field,enemies,bullets
    screen.fill(black)
    ln = n - 1
    if ln < 0:
        ln = 3
    rn = n + 1
    if rn > 3:
        rn = 0
    fg = -1
    for sd in range(1, msteps + 1):
        nx = x + sd * nap[n][0]
        ny = y + sd * nap[n][1]
        if okcoord(nx) and okcoord(ny) and field[nx][ny] == 1:
            fg = sd
            break
    fl = msteps
    if fg != -1:
        fl = fg
    for i in range(1, msteps + 1):
        pygame.draw.polygon(screen, hwhite(i), pls[3][i])
        pygame.draw.polygon(screen, black, pls[3][i], 5)
        pygame.draw.polygon(screen, hwhite(i), pls[7][i])
        pygame.draw.polygon(screen, black, pls[7][i], 5)
        pygame.draw.polygon(screen, hwhite(i), pls[6][i])
        pygame.draw.polygon(screen, black, pls[6][i], 5)
        pygame.draw.polygon(screen, hwhite(i), pls[8][i])
        pygame.draw.polygon(screen, black, pls[8][i], 5)
        pygame.draw.polygon(screen, hwhite(i), pls[9][i])
        pygame.draw.polygon(screen, black, pls[9][i], 5)
        pygame.draw.polygon(screen, hwhite(i), pls[10][i])
        pygame.draw.polygon(screen, black, pls[10][i], 5)
        nx = x + nap[n][0] * (i - 1)
        ny = y + nap[n][1] * (i - 1)
        if okcoord(nx) and okcoord(ny) and okenemy(nx,ny):
            pygame.draw.polygon(screen, hblue(i), pls[3][i])
            pygame.draw.polygon(screen, black, pls[3][i], 5)
        if okcoord(nx) and okcoord(ny) and okbullet(nx,ny):
            pygame.draw.polygon(screen, hred(i), pls[3][i])
            pygame.draw.polygon(screen, black, pls[3][i], 5)
        nx = x + nap[n][0] * (i - 1) + nap[ln][0]
        ny = y + nap[n][1] * (i - 1) + nap[ln][1]
        if okcoord(nx) and okcoord(ny) and okenemy(nx,ny):
            pygame.draw.polygon(screen, hblue(i), pls[6][i])
            pygame.draw.polygon(screen, black, pls[6][i], 5)
        if okcoord(nx) and okcoord(ny) and okbullet(nx,ny):
            pygame.draw.polygon(screen, hred(i), pls[6][i])
            pygame.draw.polygon(screen, black, pls[6][i], 5)
        nx = x + nap[n][0] * (i - 1) + nap[rn][0]
        ny = y + nap[n][1] * (i - 1) + nap[rn][1]
        if okcoord(nx) and okcoord(ny) and okenemy(nx,ny):
            pygame.draw.polygon(screen, hblue(i), pls[7][i])
            pygame.draw.polygon(screen, black, pls[7][i], 5)
        if okcoord(nx) and okcoord(ny) and okbullet(nx,ny):
            pygame.draw.polygon(screen, hred(i), pls[7][i])
            pygame.draw.polygon(screen, black, pls[7][i], 5)
    for i in range(fl, 0, -1):
        if field[x + nap[n][0] * (i - 1) + nap[ln][0]][y + nap[n][1] * (i - 1) + nap[ln][1]] == 1:
            pygame.draw.polygon(screen, hwhite(i), pls[0][i])
            pygame.draw.polygon(screen, black, pls[0][i], 5)
        elif field[x + nap[n][0] * (i) + nap[ln][0]][y + nap[n][1] * (i) + nap[ln][1]] == 1:
            pygame.draw.polygon(screen, hwhite(i), pls[4][i])
            pygame.draw.polygon(screen, black, pls[4][i], 5)
    for i in range(fl, 0, -1):
        if field[x + nap[n][0] * (i - 1) + nap[rn][0]][y + nap[n][1] * (i - 1) + nap[rn][1]] == 1:
            pygame.draw.polygon(screen, hwhite(i), pls[2][i])
            pygame.draw.polygon(screen, black, pls[2][i], 5)
        elif field[x + nap[n][0] * (i) + nap[rn][0]][y + nap[n][1] * (i) + nap[rn][1]] == 1:
            pygame.draw.polygon(screen, hwhite(i), pls[5][i])
            pygame.draw.polygon(screen, black, pls[5][i], 5)
    if fg != -1:
        pygame.draw.polygon(screen, hwhite(fg), pls[1][fg])
        pygame.draw.polygon(screen, black, pls[1][fg], 5)
    pygame.display.update()

while main_loop:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            main_loop = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                p_n -= 1
                if p_n < 0:
                    p_n = 3
            if e.key == pygame.K_RIGHT:
                p_n += 1
                if p_n > 3:
                    p_n = 0
            if e.key == pygame.K_UP:
                lx = p_x
                ly = p_y
                lx += nap[p_n][0]
                ly += nap[p_n][1]
                if field[lx][ly] != 1:
                    p_x = lx
                    p_y = ly
            if e.key == pygame.K_SPACE:
                if tp == "s":
                    create_bullet((p_x,p_y,p_n))
                else:
                    nbl = 1
                    bl = [p_x,p_y,p_n]
    if rtt + reft < pygame.time.get_ticks():
        draw_frame(p_x, p_y, p_n)
        #if (p_x,p_y) in enemies:
        #    main_loop = 0
        for b in bullets:
            b[0] += nap[b[2]][0]
            b[1] += nap[b[2]][1]
            if field[b[0]][b[1]] == 1:
                del bullets[bullets.index(b)]
        rtt = pygame.time.get_ticks()
pygame.quit()
exit()
