import math
import pygame
from pygame import mixer
import random

pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# background
background_img = pygame.image.load('space_background.jpg')
background_img = pygame.transform.scale(background_img, (800, 600))

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = 1
bullet_state = 'loaded'

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(0.1)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = 'fired'
    screen.blit(bulletImg, (x + 16, y + 10))


def collison_detected(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    return False


score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score_font = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_font, (x, y))


def game_over():
    over_font = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_font, (200, 250))


    # game loop
running = True
while running:
    # screen background color
    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed check wheather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                #fireBullet(bulletX, bulletY)
                if bullet_state == 'loaded':
                    bulletX = playerX
                    bullet_state = 'fired'
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # spaceship boundries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 736
    elif playerX >= 736:
        playerX = 0

    # enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]

        if enemyY[i] > 550:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY_change[i] = 0.01
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY_change[i] = 0.01

        if collison_detected(enemyX[i], enemyY[i], bulletX, bulletY):
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = playerY
            bullet_state = 'loaded'
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        if collison_detected(enemyX[i], enemyY[i], playerX, playerY):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = 'loaded'

    if bullet_state == "fired":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
