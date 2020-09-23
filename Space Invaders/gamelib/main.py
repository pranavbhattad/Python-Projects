# removing Welcome Promp Window
# centering the game
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_VIDEO_CENTERED'] = '1'

# importing all necessary modules
import pygame
from pygame import mixer
import random
import math
import time

# initializing
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

# Background Image
background = pygame.image.load('gamelib/.image lib/background.png')

# Top Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('gamelib/.image lib/Logo.png')
pygame.display.set_icon(icon)


# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


# Game Front Page
StartUp = pygame.image.load('gamelib/.image lib/StartUp.png')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Game Fonts
font = "gamelib/.font lib/FixedSys.fon"
head = "gamelib/.font lib/dungeons.ttf"

# Player
playerImg = pygame.image.load('gamelib/.image lib/spaceship.png')
playerX = 400
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
# to change the num of enemy: 
# change the number below
num_of_enemy = 4

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('gamelib/.image lib/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready State - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('gamelib/.image lib/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
sfont = pygame.font.Font('freesansbold.ttf', 30)

textX = 10
textY = 10

# Game Over Img
gameoverImg = pygame.image.load('gamelib\.image lib\gameover2.png')

def show_score(x,y):
    score = sfont.render("Score : "  + str( score_value), True, (white))
    screen.blit(score, (x, y))

# func Game Over
def gameover():
    screen.blit(gameoverImg, (0, 0))

# defining player
def player(x, y):
    screen.blit(playerImg, (x, y))


# defining enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Definition on line 74 and 125
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollide(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Main Function (Most Important)
def main_func():

    #    recalling everything from up

    # Player
    playerImg = pygame.image.load('gamelib/.image lib/spaceship.png')
    playerX = 400
    playerY = 500
    playerX_change = 0

    # Bullet

    # Ready State - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

    bulletImg = pygame.image.load('gamelib/.image lib/bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"
    
    # score
    score_value = 0
    
    def show_score(x,y):
        score = sfont.render("Score: " + str (score_value), True, (white))
        screen.blit(score, (x, y))


    # funcs
    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))


    def isCollide(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"

                if event.key == pygame.K_RETURN:
                    if selected == "start":

                        # Game Loop
                        running = True
                        while running:
                            # screen optimization
                            screen.fill((0, 0, 0))
                            screen.blit(background, (0, 0))

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False

                                # KeyStroke/ Key Movements Function
                                if event.type == pygame.KEYDOWN:
                                    # Giving Left keys
                                    if event.key == pygame.K_LEFT:
                                        playerX_change = -6
                                    if event.key == pygame.K_a:
                                        playerX_change = -6
                                        # giving Right Key
                                    if event.key == pygame.K_RIGHT:
                                        playerX_change = 6
                                    if event.key == pygame.K_d:
                                        playerX_change = 6

                                    # Fire bullet if key pressed
                                    if event.key == pygame.K_SPACE:
                                        if bullet_state == "ready":
                                            bulletX = playerX
                                            bullet_state = "fire"
                                            lasershoot = mixer.Sound('gamelib\.music lib\laser.wav')
                                            lasershoot.play()
                                            # never going to forget upper line code 
                                            # it made me dance so much...
                                            fire_bullet(playerX, bulletY)

                                    # If ecs is pressed then Game Exit
                                    if event.key == pygame.K_ESCAPE:
                                        running = False

                                # Giving Player Velocity
                                if event.type == pygame.KEYUP:
                                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                                        playerX_change = 0

                            # making player boundaries
                            playerX += playerX_change

                            if playerX <= 0:
                                playerX = 0
                            elif playerX >= 735:
                                playerX = 735

                            #  Enemy Movement
                            for i in range(num_of_enemy):
                               
                                #    Game Over
                                if enemyY[i] > 450:
                                    for j in range (num_of_enemy):
                                        enemyY[j] = 2000
                                        gameover()
                        
                        
                                enemyX[i] += enemyX_change[i]
                                if enemyX[i] <= 0:
                                    enemyX_change[i] = 4
                                    enemyY[i] += enemyY_change[i]
                                elif enemyX[i] >= 735:
                                    enemyX_change[i] = -4
                                    enemyY[i] += enemyY_change[i]

                                # Collision
                                collision = isCollide(enemyX[i], enemyY[i], bulletX, bulletY)
                                if collision:
                                    bulletY = 480
                                    bullet_state = "ready"
                                    score_value += 1
                                    enemyX[i] = random.randint(0, 735)
                                    enemyY[i] = random.randint(50, 150)

                                enemy(enemyX[i], enemyY[i], i)

                            # Bullet Movement
                            if bulletY <= 0:
                                bulletY = 480
                                bullet_state = "ready"

                            if bullet_state == "fire":
                                fire_bullet(bulletX, bulletY)
                                bulletY -= bulletY_change

                            # calling func and obj
                            player(playerX, playerY)
                            show_score(textX, textY)
                            pygame.display.update()

                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(black)
        screen.blit(StartUp, (0, 0))

        title = text_format("Space Invaders", head, 80, white)
        if selected == "start":
            text_start = text_format("START", font, 90, white)
        else:
            text_start = text_format("START", font, 90, black)
        if selected == "quit":
            text_quit = text_format("QUIT", font, 90, white)
        else:
            text_quit = text_format("QUIT", font, 90, black)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (800 / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (800 / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (800 / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        pygame.display.set_caption("Space Invaders")


main_func()
