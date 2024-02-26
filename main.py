import time

import pygame
from random import randrange as rnd

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
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(w // 2 - paddle_w // 2, h - paddle_h - 10, paddle_w, paddle_h)
# мяч
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, w - ball_rect), h // 2, ball_rect, ball_rect)
dx, dy = 1, -1
# блоки
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]
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


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


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
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('blue'), ball.center, ball_radius)
    # движение мяча
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    if ball.centerx < ball_radius or ball.centerx > w - ball_radius:
        dx = -dx
    if ball.centery < ball_radius:
        dy = -dy
    # столкновение
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
    if ball.bottom > h:
        heals -= 1
        ball.x = 1100
        ball.y = 400
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
    elif not len(block_list):
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
    if (key[pygame.K_LEFT] or key[pygame.K_a]) and paddle.left > 0:
        paddle.left -= paddle_speed
    if (key[pygame.K_RIGHT] or key[pygame.K_d]) and paddle.right < w:
        paddle.right += paddle_speed
    pygame.display.flip()
    clock.tick(fps)