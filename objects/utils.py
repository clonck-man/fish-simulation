import math
import pygame


def get_angle(x1, y1, x2, y2):
    """
    Calcul l'angle entre deux positions x, y.

    Args:
        x1: Coordonnée x de la première position.
        y1: Coordonnée y de la première position.
        x2: Coordonnée x de la deuxième position.
        y2: Coordonnée y de la deuxième position.

    Returns:
        L'angle entre les deux positions, en degrés.
    """

    # Calcul du vecteur directeur
    dx = x2 - x1
    dy = y2 - y1

    # Calcul de l'angle en radians
    angle_radian = math.atan2(dy, dx)

    # Conversion de l'angle en degrés
    angle_degre = math.degrees(angle_radian)

    # Modification de l'angle pour qu'il soit compris entre 0 et 360 degrés
    angle_degre = math.fmod(angle_degre, 360)

    return angle_degre


def draw_line(p1, direction, screen, length=1000, color=(0, 255, 0)):
    x, y = p1

    dx = math.cos(math.radians(direction)) * length
    dy = math.sin(math.radians(direction)) * length
    new_x, new_y = x + dx, y + dy

    pygame.draw.line(screen, color, (x, y), (new_x, new_y))


def point_in_fov(point_A, angle1, angle2, point_B, rayon=50):
    """
    Vérifie si le point B est dans le champ de vision défini par les angles angle1 et angle2
    par rapport au point A.
    """
    x_A, y_A = point_A
    x_B, y_B = point_B

    # Calcul des coordonnées polaires des points par rapport à A
    angle_B = math.atan2(y_B - y_A, x_B - x_A)
    distance_B = math.hypot(x_B - x_A, y_B - y_A)

    # Ajustement des angles pour qu'ils soient dans le même intervalle (0, 2*pi)
    angle1 = math.radians(angle1) % (2 * math.pi)
    angle2 = math.radians(angle2) % (2 * math.pi)
    angle_B = (angle_B + 2 * math.pi) % (2 * math.pi)

    # Vérification si l'angle est entre angle1 et angle2 et si la distance est dans la plage
    if angle1 < angle2:
        return angle1 <= angle_B <= angle2 and distance_B <= rayon
    else:
        return (angle_B >= angle1 or angle_B <= angle2) and distance_B <= rayon


def mean_angles(angles):
    x_total = y_total = 0

    for angle in angles:
        x_total += math.cos(math.radians(angle))
        y_total += math.sin(math.radians(angle))

    res = math.degrees(math.atan2(y_total, x_total))

    # Assurer que l'angle est dans l'intervalle [0, 360)
    res = (res + 360) % 360

    return res

