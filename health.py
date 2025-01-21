# health bar sample 01

# importing libraries
import pygame
from pygame.pixelcopy import surface_to_array

# initializing pygame
pygame.init()

max_health = 100
health = 20
result = health / max_health

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Health bar')

# health bar
class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        result = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * result, self.h))

health_bar = HealthBar(250, 200, 300, 40, 100)


run = True
while run:
    screen.fill("indigo")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw the health bar
    health_bar.draw(screen)

    pygame.display.flip()

pygame.quit()
