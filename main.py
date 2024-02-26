import time

import pygame
from random import randrange as rnd

def check(dx, dy, ball, rect):
    if dx > 0:
        d_x = ball.right - rect.left
    else:
        d_x = rect.right - ball.left
    if dy > 0:
        d_y = ball.bottom - rect.top
    else:
        d_y = rect.bottom - ball.top
    if abs(d_x - d_y) < 10:
        dx, dy = -dx, -dy
    elif d_x > d_y:
        dy = -dy
    elif d_y > d_x:
        dx = -dx
    return dx, dy

size = w, h = 1200, 800
fps = 100
# start
pygame.init()
start = pygame.image.load('Start.png')
start = pygame.transform.scale(start, size)
sc = pygame.display.set_mode(size)
sc.blit(start, (0, 0))
pygame.display.flip()
flag = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYUP:
            flag = 1
            break
    if flag:
        break
# экран и отступы
pw = 330
ph = 35
ps = 15
p = pygame.Rect(w // 2 - pw // 2, h - ph - 10, pw, ph)
# мяч
br = 20
bs = 6
b_r = int(br * 2 ** 0.5)
b = pygame.Rect(rnd(b_r, w - b_r), h // 2, b_r, b_r)
dx, dy = 1, -1
# блоки
bl = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
cl = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]
clock = pygame.time.Clock()

# main
# задний фон
img = pygame.image.load('background.jpg')
img = pygame.transform.scale(img, size)
heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (64, 64))
game_won = pygame.image.load("Win.png")
game_won = pygame.transform.scale(game_won, size)
game_lose = pygame.image.load("Lose.png")
game_lose = pygame.transform.scale(game_lose, size)

heals = 3


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    if (heals >= 1):
        sc.blit(heart_image, (w - 64 - 1, h - 2 * 64 - 1))
    if heals >= 2:
        sc.blit(heart_image, (w - 64 - 1, h - 3 * 64 - 1))
    if heals == 3:
        sc.blit(heart_image, (w - 64 - 1, h - 4 * 64 - 1))
    # создание карты
    [pygame.draw.rect(sc, cl[c], b) for c, b in enumerate(bl)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('blue'), ball.center, br)
    # движение мяча
    b.x += bs * dx
    b.y += bs * dy
    if b.centerx < br or b.centerx > w - br:
        dx = -dx
    if b.centery < br:
        dy = -dy
    # столкновение
    if dy > 0 and b.colliderect(p):
        dx, dy = check(dx, dy, b, p)
    hi = b.collidelist(bl)
    if hi != -1:
        hr = bl.pop(hi)
        hc = cl.pop(hi)
        dx, dy = check(dx, dy, b, hr)
        pygame.draw.rect(sc, hc, hr)
        fps += 2
    if b.bottom > h:
        heals -= 1
        b.x = 1100
        b.y = 400
        if heals == 0:
            sc.fill((255, 255, 255))
            pygame.display.flip()
            sc.blit(game_lose, (0, 0))
            pygame.display.flip()
            for i in range(300):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                time.sleep(0.01)
            exit()
    elif not len(bl):
        sc.fill((255, 255, 255))
        sc.blit(game_won, (0, 0))
        pygame.display.flip()
        for i in range(300):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            time.sleep(0.01)
        exit()
    # управление платформой
    key = pygame.key.get_pressed()
    if (key[pygame.K_LEFT] or key[pygame.K_a]) and p.left > 0:
        p.left -= ps
    if (key[pygame.K_RIGHT] or key[pygame.K_d]) and p.right < w:
        p.right += ps
    pygame.display.flip()
    clock.tick(fps)