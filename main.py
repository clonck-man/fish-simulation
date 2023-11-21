import pygame
import sys
from objects import fish_data
from terrain import terrain

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
dimension_1 = (800, 600)
screen_1 = pygame.display.set_mode(dimension_1)
pygame.display.set_caption("Mon Petit Jeu")

terrain = terrain(dimension_1, screen_1)
for _ in range(fish_data.FISH_NBR):
    terrain.add_fish()

# Boucle principale du jeu
while True:
    events = pygame.event.get()
    for event in events:

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    terrain.run()

    # Limiter la fréquence d'images
    terrain.clock.tick(60)
