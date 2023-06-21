# Import libraries
import pygame
import sys
import math
import random
from Cucodemon import *
from pygame import mixer
from Sniffer import *
from DSoldier import *

# Initialize pygame
pygame.init()

# Variables
aKeyPressed = False
dKeyPressed = False
wKeyPressed = False
sKeyPressed = False
leftMPressed = False
speed = 10
shotsPerSecond = 0.5
shotTimer = 60 // shotsPerSecond
cucosDead = 0
LevelOne = True
LevelTwo = False
levelOne = True
cucosDeadT = True
gOver = False
gameOver = pygame.font.SysFont("Comic Sans MS", 56) 
title = pygame.font.Font("Resources/Doom2016Right.ttf", 90)
win = False
gunMode = 1
startScreen = True

FPS = pygame.time.Clock()

# Create the display screen
window = pygame.display.set_mode((500, 500), pygame.FULLSCREEN)

WIDTH = window.get_width()
HEIGHT = window.get_height()

# Needed colours
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Background (level 1) and assorted music
Hell = pygame.transform.scale(pygame.image.load("Resources/Hell.png").convert_alpha(), (WIDTH, HEIGHT))
e1m1 = mixer.Sound("Resources/E1M1.wav")

# Background (level 2)
Hell2 = pygame.transform.scale(pygame.image.load("Resources/Hell2.png").convert_alpha(), (WIDTH, HEIGHT))
e2m1 = mixer.Sound("Resources/E2M1.wav")

# Start Screen Text
Start = title.render("Press SPACE to Start!", 0, RED)
Title = title.render("DOOM", 0, RED)
Quit = title.render("Press ESC to Quit", 0, RED)

# Game Over Screen Text
GameOver = gameOver.render("You Died!", 0, BLUE)
GameOver2 = gameOver.render("Game Over!", 0, BLUE)

# Win Screen Text
Win = gameOver.render("You won!", 0, BLUE)
Win2 = gameOver.render("You killed all the demons!", 0, BLUE)

# Player Character and all of its needed variables (hitbox, hurtbox, health, etc.)
Hilbert = pygame.transform.scale(pygame.image.load("Resources/Hilbert.png").convert_alpha(), (50, 50))
HilBX = WIDTH/2
HilBY = HEIGHT/2
HilBox = Hilbert.get_rect()
HilBox.x = HilBX
HilBox.y = HilBY
Health = 150

# Shotgun bullet projectile list
projectiles = []

# Enemy list
enemies = []

# Enemy shot projectile list
cProjectiles = []

# Cucodemon character
Cucodemon = pygame.transform.scale(pygame.image.load("Resources/Cucodemon.png").convert_alpha(), (75, 75))

# Sniffer character
Sniffer = pygame.transform.scale(pygame.image.load("Resources/Sniffer.png").convert_alpha(), (75, 75))

# Shotgun Shot Projectile
def sShot():
    global shotTimer, shotsPerSecond, HilBox, projectiles

    if shotTimer != 0:
        return
    else:
        shotTimer = 60 // shotsPerSecond

        sPellet = pygame.transform.scale(pygame.image.load("Resources/Bullet.png").convert_alpha(), (25, 25))
        sPx = HilBox.x + 10
        sPy = HilBox.y + 10

        mousePos = pygame.mouse.get_pos()

        for i in range(-1, 2):
            sBox = sPellet.get_rect()
            sBox.x = sPx
            sBox.y = sPy

            angle = math.atan2(mousePos[1] - HilBox.centery, mousePos[0] - HilBox.centerx)
            projectiles.append((sPellet, sBox, angle+(i * 0.3)))

def aShot():
    global shotTimer, shotsPerSecond, HilBox, projectiles

    if shotTimer != 0:
        return
    else:
        shotTimer = 20 // shotsPerSecond

        sPellet = pygame.transform.scale(pygame.image.load("Resources/Bullet.png").convert_alpha(), (25, 25))
        sPx = HilBox.x + 10
        sPy = HilBox.y + 10

        mousePos = pygame.mouse.get_pos()

        sBox = sPellet.get_rect()
        sBox.x = sPx
        sBox.y = sPy

        angle = math.atan2(mousePos[1] - HilBox.centery, mousePos[0] - HilBox.centerx)
        projectiles.append((sPellet, sBox, angle))

# Shoot function for the Cucodemon
def cucoShoot():

    global cProjectiles

    for enemy in enemies:
        if type(enemy) is not Enemy:
            continue

        if enemy.cucTimer != 0:
            return
        else:
            enemy.cucTimer = 60 // enemy.cucDPS

            cProj = pygame.transform.scale(pygame.image.load("Resources/CucodemonProjectile.png").convert_alpha(), (25, 25))
            cPx = enemy.rect.centerx + 10
            cPy = enemy.rect.centery + 10
    
            cBox = cProj.get_rect()
            cBox.x = cPx
            cBox.y = cPy

            angleShot = math.atan2(HilBox.centery - enemy.rect.centery, HilBox.centerx - enemy.rect.centerx)
            cProjectiles.append((cProj, cBox, angleShot))

# Run function for the demon soldier
def demonRun():
    for enemy in enemies:
        if type(enemy) is not dEnemy:
            continue

        box = enemy.rect
        if box.centerx < HilBox.x:
            if (HilBox.x - box.centerx) > 5:
                box.move_ip(2, 0)
        elif (box.centerx - HilBox.x) > 5:
            box.move_ip(-2, 0)

        if box.centery < HilBox.y:
            if (HilBox.y - box.centery) > 5:
                box.move_ip(0, 2)
        elif (box.centery - HilBox.y) > 5:
            box.move_ip(0, -2)


# Timers for the enemy spawns
pygame.time.set_timer(pygame.USEREVENT+1, 4000)
pygame.time.set_timer(pygame.USEREVENT+2, 6000)
pygame.time.set_timer(pygame.USEREVENT+3, 5000)

# Start screen while loop; everything on the start screen happens here
while startScreen:
    # Sets the FPS
    FPS.tick(60)

    # Prints the three texts (title, start, and quit)
    window.blit(Start, (WIDTH // 2 - 300, HEIGHT // 2))
    window.blit(Title, (WIDTH // 2 - 75, 100))
    window.blit(Quit, (WIDTH // 2 - 300, HEIGHT // 2 + 100))

    # Update the pygame display
    pygame.display.update()

    # Check to see if the player presses "space" to start or "quit" to exit
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                startScreen = False
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

# Update section; whatever happens here happens every frame
while startScreen == False:
    FPS.tick(60)

    # Game over screen
    if gOver == True:
        window.blit(GameOver, (WIDTH/2, HEIGHT/2))
        window.blit(GameOver2, (WIDTH/2, HEIGHT/2 + 50))
        pygame.display.update()
        pygame.time.wait(3000)
        sys.exit(0)

    # Win screen
    if win == True:
        window.blit(Win, (WIDTH/2, HEIGHT/2))
        window.blit(Win2, (WIDTH/2 - 250, HEIGHT/2 + 50))
        pygame.display.update()
        pygame.time.wait(3000)
        sys.exit(0)
        
    # Enemy attack functions
    cucoShoot()
    demonRun()

    # If the user tries to exit the game using the "x", it will work and won't close until then.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit(0)

        # Enemy spawning functions
        if event.type == pygame.USEREVENT+1:
            enemies.append(spawnCuco(Hilbox=HilBox))
        elif event.type == pygame.USEREVENT+2 and not levelOne:
            enemies.append(spawnSnif(Hilbox=HilBox))
        elif event.type == pygame.USEREVENT+3:
            enemies.append(spawnDoldier(Hilbox=HilBox))

        # Input detection; Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                aKeyPressed = True
            if event.key == pygame.K_d:
                dKeyPressed = True
            if event.key == pygame.K_w:
                wKeyPressed = True
            if event.key == pygame.K_s:
                sKeyPressed = True
            if event.key == pygame.K_1:
                gunMode = 1
            if event.key == pygame.K_2:
                gunMode = 2
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                aKeyPressed = False
            if event.key == pygame.K_d:
                dKeyPressed = False
            if event.key == pygame.K_w:
                wKeyPressed = False
            if event.key == pygame.K_s:
                sKeyPressed = False

        # Input detection; shotgun blast
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gunMode == 1:
                sShot()
            elif gunMode == 2:
                aShot()

        if event.type == pygame.MOUSEBUTTONUP:
            leftMPressed = False

    # Changes the x and y values to ACTUALLY move the character
    if aKeyPressed == True:
        HilBox.x -= speed
    if dKeyPressed == True:
        HilBox.x += speed
    if wKeyPressed == True:
        HilBox.y -= speed
    if sKeyPressed == True:
        HilBox.y += speed

    # Outer edge collisions
    if HilBox.left < 0:
        HilBox.left = 0
    if HilBox.right > WIDTH:
        HilBox.right = WIDTH
    if HilBox.top < 0:
        HilBox.top = 0
    if HilBox.bottom > HEIGHT:
        HilBox.bottom = HEIGHT
    
    # Check the level number and prints the level to the screen based on the variable
    if levelOne == True:
        window.blit(Hell, (0, 0))
    else:
        window.blit(Hell2, (0, 0))

    # Prints the character to the screen
    window.blit(Hilbert, HilBox)
    
    # Draws and moves the projectile, and deals with the hitboxes of all enemies
    for i in range(len(projectiles)):
        try:
            projectile = projectiles[i]

            box = projectile[1]
            angle = projectile[2]

            if gunMode == 1:
                speed = 5
            elif gunMode == 2:
                speed = 10

            box.move_ip(math.cos(angle) * speed + 0.1, math.sin(angle) * speed + 0.1)

            if box.right > WIDTH or box.left < 0 or box.bottom > HEIGHT or box.top < 0:
                del projectiles[i]

            window.blit(projectile[0], projectile[1])

            indices = box.collidelistall(enemies)
            
            for index in indices:
                cuco = enemies[index]
                if gunMode == 1:
                    enemies[index].health -= 50
                elif gunMode == 2:
                    enemies[index].health -= 100
                del projectiles[i]

                if enemies[index].health <= 0:
                    del enemies[index]
                    cucosDead += 1

        except IndexError:
            continue

    # Draws the cucodemon projectile(s), and deals with player hitboxes
    for i in range(len(cProjectiles)):
        try:
            cProjectile = cProjectiles[i]

            box = cProjectile[1]
            angle = cProjectile[2]
            speed = 5

            box.move_ip(math.cos(angle) * speed + 0.1, math.sin(angle) * speed + 0.1)

            if box.right > WIDTH or box.left < 0 or box.bottom > HEIGHT or box.top < 0:
                del cProjectiles[i]

            window.blit(cProjectile[0], cProjectile[1])

            if box.colliderect(HilBox):
                Health -= 50
                del cProjectiles[i]

                if Health <= 0:
                    del Hilbert
                    gOver = True

        except IndexError:
            continue

    # Allows the player to take damage from running into the enemies
    for i in enemies:
        if HilBox.colliderect(i.rect):
            if i.contactDamage:
                Health -= 50

                if Health <= 0:
                    del Hilbert
                    gOver = True
                
                i.contactDamage = False
        else:
            i.contactDamage = True

    # Cooldown for the bullet
    if shotTimer > 0:
        shotTimer -= 1

    # Play the background sounds
    if LevelOne == True:
        e1m1.play()
        LevelOne = False
    if LevelTwo == True:
        e1m1.stop()
        e2m1.play()
        LevelTwo = False

    # Cooldown for the Cucodemon proj
    for cucodemon in enemies:
        if type(cucodemon) == Enemy:
            if cucodemon.cucTimer > 0:
                cucodemon.cucTimer -= 1
        if type(cucodemon) == dEnemy:
            if cucodemon.lungeTimer > 0:
                cucodemon.lungeTimer -= 1
                
    # Checks if enough enemies were killed, allowing the level to be switched
    if cucosDeadT == True and cucosDead >= 10:
        LevelTwo = True
        levelOne = False
        cucosDeadT = False
    elif cucosDead >= 15:
        win = True

    # Draws the cucodemon
    for enemy in enemies:
        window.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

    # Update the pygame display
    pygame.display.update()