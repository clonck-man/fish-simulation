import pygame
import math
import numpy as np
import random
from objects.utils import draw_line, point_in_fov, mean_angles
from objects import fish_data


class fish:
    def __init__(self, terrain, direction, position):
        self.terrain = terrain

        self.direction = direction
        self.position = position

        self.color = (random.random() * 255, random.random() * 255, random.random() * 255)

        self.influences = []

    def update(self):
        self.get_influences(self.terrain.fish)
        self.get_direction()
        self.move()

    def move(self):
        x, y = self.position
        terrain_largeur, terrain_hauteur = self.terrain.dimension

        dx = math.cos(math.radians(self.direction)) * fish_data.FISH_SPEED
        dy = math.sin(math.radians(self.direction)) * fish_data.FISH_SPEED
        new_x, new_y = x + dx, y + dy

        if new_x < 0:
            self.direction = (180 - self.direction) % 360
            new_x = 0
        elif new_x > terrain_largeur:
            self.direction = (180 - self.direction) % 360
            new_x = terrain_largeur

        if new_y < 0:
            self.direction = (-self.direction) % 360
            new_y = 0
        elif new_y > terrain_hauteur:
            self.direction = (-self.direction) % 360
            new_y = terrain_hauteur

        self.position = (new_x, new_y)

    def get_influences(self, fish_list):
        fishInFov = []

        # Calcul des angles minimum et maximum du champ de vision
        angle_min = self.direction - fish_data.FISH_FOV / 2
        angle_max = self.direction + fish_data.FISH_FOV / 2

        # Parcours de tous les poissons
        for f in fish_list:
            if point_in_fov(self.position, angle_min, angle_max, f.position, 1000):
                dist = np.linalg.norm(np.array(self.position) - np.array(f.position))

                if dist < fish_data.FISH_SECURE_SPACE*fish_data.FISH_SIZE:
                    fishInFov.append(f)

        # Tri des poissons en fonction de leur distance par rapport à votre position
        fishInFov = sorted(fishInFov, key=lambda x: np.linalg.norm(np.array(self.position) - np.array(x.position)))[:fish_data.FISH_INFLUENCES]

        self.influences = fishInFov

    def get_direction(self):
        directions = [self.direction]
        for f in self.influences:
            directions.append(f.direction)

        self.direction = self.direction * fish_data.FISH_INERTIA + mean_angles(directions) * (1 - fish_data.FISH_INERTIA)

    def draw(self, screen, see_angle=False, see_dist=False):
        x, y = self.position

        pygame.draw.circle(screen, self.color, (int(x), int(y)), fish_data.FISH_SIZE)

        # queue
        q_x = x + fish_data.FISH_SIZE * 4 * math.cos(math.radians((180 + self.direction) % 360))
        q_y = y + fish_data.FISH_SIZE * 4 * math.sin(math.radians((180 + self.direction) % 360))

        # epaule droite
        # ed_x = x + fish_data.FISH_SIZE/2 * math.cos(math.radians((90 + self.direction) % 360))
        # ed_y = y + fish_data.FISH_SIZE/2 * math.sin(math.radians((90 + self.direction) % 360))

        # epaule gauche
        eg_x = x + (fish_data.FISH_SIZE/2 * math.cos(math.radians((270 + self.direction) % 360)))/4
        eg_y = y + (fish_data.FISH_SIZE/2 * math.sin(math.radians((270 + self.direction) % 360)))/4

        # pygame.draw.line(screen, self.color, (ed_x, ed_y), (q_x, q_y), fish_data.FISH_SIZE)
        pygame.draw.line(screen, self.color, (eg_x, eg_y), (q_x, q_y), fish_data.FISH_SIZE)
        # pygame.draw.line(screen, self.color, (x, y), (q_x, q_y), fish_data.FISH_SIZE)

        if see_angle:
            draw_line(self.position, self.direction - fish_data.FISH_FOV / 2, screen, fish_data.FISH_SECURE_SPACE*fish_data.FISH_SIZE)
            draw_line(self.position, self.direction + fish_data.FISH_FOV / 2, screen, fish_data.FISH_SECURE_SPACE*fish_data.FISH_SIZE)
            # draw_line(self.position, self.direction, screen, fish_data.FISH_ATTRACTIVE_SPACE*fish_data.FISH_SIZE, (255, 0, 0))
            # draw_line(self.position, self.direction, screen, fish_data.FISH_SECURE_SPACE*fish_data.FISH_SIZE, (255, 255, 0))
            # draw_line(self.position, self.direction, screen, fish_data.FISH_LEBENSRAUM*fish_data.FISH_SIZE, (255, 255, 255))

        if see_dist:
            for f in self.influences:
                pygame.draw.line(screen, (0, 0, 255), self.position, f.position)

