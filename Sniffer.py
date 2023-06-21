# Importing needed libraries
import pygame
import random

# Variables
window = pygame.display.set_mode((500, 500), pygame.FULLSCREEN)
WIDTH = window.get_width()
HEIGHT = window.get_height()

# Sniffer enemy sprite
Sniffer = pygame.transform.scale(pygame.image.load("Resources/Sniffer.png").convert_alpha(), (75, 75))

# Sniffer class
class sEnemy:
    def __init__ (self, xpos, ypos):
        self.image = Sniffer
        self.health = 100
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.contactDamage = True

        window.blit(Sniffer, (xpos, ypos))

# Spawn function for the Sniffer
def spawnSnif(Hilbox):

    randx = random.randint(0, WIDTH - 100)
    randy = random.randint(0, HEIGHT - 100)

    while Hilbox.collidepoint(randx, randy):
         randx = random.randint(0, WIDTH - 100)
         randy = random.randint(0, HEIGHT - 100)

    enemy1 = sEnemy(randx, randy)
    window.blit(Sniffer, (randx, randy))
    return enemy1