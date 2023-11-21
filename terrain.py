import pygame
import random
from fish import fish
from mouse import mouse
import threading


class terrain:
    def __init__(self, dimension, screen):
        self.dimension = dimension
        self.centre = (dimension[0] // 2, dimension[1] // 2)

        self.screen = screen
        self.clock = pygame.time.Clock()

        self.fish = []

        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.mouse = mouse(self)

    def add_fish(self):
        self.fish.append(fish(self, random.random() * 360, (random.random()*self.dimension[0], random.random()*self.dimension[1])))

    def update_fish(self, f):
        f.update()

    def draw(self):
        # efface le terrain
        self.screen.fill(self.black)

        '''
        self.fish[0].draw(self.screen, True, True)
        for f in self.fish[0].influences:
            f.draw(self.screen)
        '''
        for f in self.fish:
            f.draw(self.screen, False, False)

        # Affichage des FPS
        font = pygame.font.Font(None, 36)
        fps_texte = font.render(f"FPS: {int(self.clock.get_fps())}", True, (0, 0, 255))
        self.screen.blit(fps_texte, (10, 10))

        self.mouse.draw(self.screen)

        # Mettre à jour l'affichage
        pygame.display.flip()

    def run(self):
        for f in self.fish:
            f.update()

        self.mouse.update()

        self.draw()
