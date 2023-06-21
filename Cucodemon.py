# Importing needed libraries
import pygame
import random

# Variables
window = pygame.display.set_mode((500, 500), pygame.FULLSCREEN)
WIDTH = window.get_width()
HEIGHT = window.get_height()

# Cucodemon enemy sprite
Cucodemon = pygame.transform.scale(pygame.image.load("Resources/Cucodemon.png").convert_alpha(), (75, 75))

# Cucodemon class
class Enemy:
    def __init__ (self, xpos, ypos):
        self.image = Cucodemon
        self.health = 100
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.cucDPS = 0.7
        self.cucTimer = 60 // self.cucDPS
        self.contactDamage = True

        window.blit(Cucodemon, (xpos, ypos))

# Spawn function for the Cucodemon
def spawnCuco(Hilbox):

    randx = random.randint(0, WIDTH - 100)
    randy = random.randint(0, HEIGHT - 100)

    while Hilbox.collidepoint(randx, randy):
        randx = random.randint(0, WIDTH - 100)
        randy = random.randint(0, HEIGHT - 100)

    enemy1 = Enemy(randx, randy)
    window.blit(Cucodemon, (randx, randy))
    return enemy1