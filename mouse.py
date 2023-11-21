import random
import pygame


class mouse:
    def __init__(self, terrain):
        self.size = 20
        self.color = (random.random() * 255, random.random() * 255, random.random() * 255)
        self.terrain = terrain
        self.position = []

    def update(self):
        self.position = pygame.mouse.get_pos()

    def draw(self, screen):
        x, y = self.position
        s = self.size
        pygame.draw.rect(screen, (0, 255, 0), (x-s/2, y-s/2, s, s))
