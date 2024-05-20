import numpy as np
import pygame
import sys

height = 60
width = 60
point_size = 15

def diamond(x, y, srodek):
    return abs(x-srodek[0]) + abs(y-srodek[1])

def diamonds(x,y,srodki,promienie):
    suma = 0
    for i,srodek in enumerate(srodki):
        if diamond(x,y,srodek) == 0:
            suma+=1
        else:
            suma += (promienie[i]) / diamond(x,y,srodek)
    return suma

def cell(x,y,srodki,promienie):
    wart = diamonds(x,y,srodki,promienie)
    if wart >= 1:
        return 1
    else:
        return 0

# Inicjalizacja pygame
pygame.init()

# Ustawienie rozmiaru okna
window_width = width * point_size
window_height = height * point_size
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255,0,0)

#Isolines
def get_state(a,b,c,d):
    return a*8+b*4+c*2+d

def interpolacja(p1,p2,mids,promienie):
    dist = diamonds(p2[0], p2[1], mids, promienie) - diamonds(p1[0], p1[1], mids, promienie)
    if dist == 0:
        return 0
    else:
        return (1**2 - diamonds(p1[0], p1[1], mids, promienie)) / dist

def find_isolines(field,mids,promienie):
    lines = []
    for i in range(height - 1):
        for j in range(width - 1):
            # A(i,j) B(i,j+1) C(i+1,j+1) D(i+1,j)
            A = (i,j)
            B = (i,j+1)
            C = (i+1, j+1)
            D = (i+1, j)

            # a = (i,j+0.5)
            # b = (i+0.5, j+1)
            # c = (i+1, j+0.5)
            # d = (i+0.5, j)

            a = (i,j + interpolacja(A,B,mids,promienie))
            b = (i + interpolacja(B,C,mids,promienie), j+1)
            c = (i+1,j + interpolacja(D,C,mids,promienie))
            d = (i + interpolacja(A,D,mids,promienie), j)

            state = get_state(field[i][j], field[i][j+1], field[i + 1][j + 1], field[i+1][j])
            if state == 1:
                lines.append((c, d))
            elif state == 2:
                lines.append((c, b))
            elif state == 3:
                lines.append((b, d))
            elif state == 4:
                lines.append((a, b))
            elif state == 5:
                lines.append((a, d))
                lines.append((b, c))
            elif state == 6:
                lines.append((a, c))
            elif state == 7:
                lines.append((a, d))
            elif state == 8:
                lines.append((a,d))
            elif state == 9:
                lines.append((a,c))
            elif state == 10:
                lines.append((a, b))
                lines.append((c, d))
            elif state == 11:
                lines.append((a,b))
            elif state == 12:
                lines.append((b,d))
            elif state == 13:
                lines.append((b,c))
            elif state == 14:
                lines.append((c,d))
    return lines

# Rysowanie punktów

mids = [[30,5],[25,55],[5,10],[55,30],[30,30],[55,40]]
promienie = [3,3,2,1,3,2]
counters = [[1,-1],[1,1],[1,0],[-1,-1],[0,1],[-1,0]]

# w prawo [0,1], w lewo [0, -1], w gore [-1,0], w dol [1,0]
# lewa-gora [-1,-1], lewy-dol [1,-1], prawa-gora [-1,1], prawy-dol [1,1]

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BLACK)
    field = np.empty((height, width))
    for i in range(height):
        for j in range(width):
            field[i][j] = cell(i, j, mids,promienie)

    # for i in range(height):
    #     for j in range(width):
    #         if field[i, j]:
    #             pygame.draw.circle(screen, RED, (j * point_size, i * point_size), point_size // 3.14)
    #         else:
    #             pygame.draw.circle(screen, WHITE, (j * point_size, i * point_size), point_size // 3.14)

    isolines = find_isolines(field,mids,promienie)
    for line in isolines:
        pygame.draw.line(screen, RED, (line[0][1] * point_size, line[0][0] * point_size),
                         (line[1][1] * point_size, line[1][0] * point_size), 3)
        
    for c,mid in enumerate(mids):
        wektor = counters[c]
        mid[0]+=wektor[0]
        mid[1]+=wektor[1]

         # Odbicie od ścian poziomych
        if mid[1] >= width - promienie[c]-1:
            wektor[1] = -abs(wektor[1])  # Ruch w lewo
        if mid[1] <= promienie[c]:
            wektor[1] = abs(wektor[1])   # Ruch w prawo

        # Odbicie od ścian pionowych
        if mid[0] >= height - promienie[c]-1:
            wektor[0] = -abs(wektor[0])  # Ruch w górę
        if mid[0] <= promienie[c]:
            wektor[0] = abs(wektor[0])   # Ruch w dół

        counters[c] = wektor

    # Wyświetlenie zmian
    pygame.display.flip()
    #clock.tick(20)

# Wyjście z programu
pygame.quit()
sys.exit()