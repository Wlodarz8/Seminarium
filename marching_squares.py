import numpy as np
import pygame
import sys

height = 60
width = 60
point_size = 15

def kolko(x,y, srodek):
    return (x-srodek[0])**2 + (y-srodek[1])**2

def funkcja2(x,y):
    return (x-30)**2 + (y-30)**2

def serce(x,y,srodek):
    wart = kolko(x,y,srodek)
    if wart <5**2:
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

def interpolacja(p1,p2,mid):
    return (5**2 - kolko(p1[0],p1[1],mid))/(kolko(p2[0],p2[1],mid) - kolko(p1[0],p1[1],mid)) #tu promien^2


def find_isolines(field,mid):
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

            a = (i,j + interpolacja(A,B,mid))
            b = (i + interpolacja(B,C,mid), j+1)
            c = (i+1,j + interpolacja(D,C,mid))
            d = (i + interpolacja(A,D,mid), j)
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

mids = [[30,5],[30,55]]
counters = [1,-1]

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(GREY)
    for c,mid in enumerate(mids):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        field = np.empty((height, width))
        for i in range(height):
            for j in range(width):
                field[i][j] = serce(i, j, mid)
        # for i in range(height):
        #     for j in range(width):
        #         if field[i, j]:
        #             pygame.draw.circle(screen, BLACK, (j * point_size, i * point_size), point_size // 3.14)
        #         else:
        #             pygame.draw.circle(screen, WHITE, (j * point_size, i * point_size), point_size // 3.14)

        isolines = find_isolines(field,mid)
        for line in isolines:
            pygame.draw.line(screen, RED, (line[0][1] * point_size, line[0][0] * point_size),
                             (line[1][1] * point_size, line[1][0] * point_size), 3)

        mid[1] += counters[c]
        if mid[1] == width - 5:
            counters[c] = -1
        if mid[1] == 4:
            counters[c] = 1

        # Wyświetlenie zmian
        pygame.display.flip()
        clock.tick(30)

# Wyjście z programu
pygame.quit()
sys.exit()