# Importing needed libraries
import pygame
import random

# Variables
window = pygame.display.set_mode((500, 500), pygame.FULLSCREEN)
WIDTH = window.get_width()
HEIGHT = window.get_height()

# Demonic Soldier enemy sprite
dSoldier = pygame.transform.scale(pygame.image.load("Resources/dSoldier.png").convert_alpha(), (75, 75))

# Demon Soldier class
class dEnemy:
    def __init__ (self, xpos, ypos):
        self.image = dSoldier
        self.health = 100
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.lungeTimer = 120
        self.lungeSteps = 5
        self.contactDamage = True
       

        window.blit(dSoldier, (xpos, ypos))

# Spawn function for the Demonic Soldier
def spawnDoldier(Hilbox):

    randx = random.randint(0, WIDTH - 100)
    randy = random.randint(0, HEIGHT - 100)

    while Hilbox.collidepoint(randx, randy):
         randx = random.randint(0, WIDTH - 100)
         randy = random.randint(0, HEIGHT - 100)

    enemy1 = dEnemy(randx, randy)
    window.blit(dSoldier, (randx, randy))
    return enemy1