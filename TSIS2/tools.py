import pygame
import math

def flood_fill(surface, x, y, new_color):
    try:
        target_color = surface.get_at((x, y))
    except IndexError:
        return 

    if target_color == new_color:
        return 

    pixels_to_check = [(x, y)]
    width, height = surface.get_size()

    set_at = surface.set_at
    get_at = surface.get_at

    while pixels_to_check:
        px, py = pixels_to_check.pop()

        if px < 0 or px >= width or py < 100 or py >= height:
            continue

        if get_at((px, py)) == target_color:
            set_at((px, py), new_color)
            
            pixels_to_check.append((px + 1, py))
            pixels_to_check.append((px - 1, py))
            pixels_to_check.append((px, py + 1))
            pixels_to_check.append((px, py - 1))


def draw_rect(surf, color, start, end, thickness):
    x, y = min(start[0], end[0]), min(start[1], end[1])
    w, h = abs(start[0]-end[0]), abs(start[1]-end[1])
    pygame.draw.rect(surf, color, (x, y, w, h), thickness)

def draw_circle(surf, color, start, end, thickness):
    rad = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
    pygame.draw.circle(surf, color, start, rad, thickness)

def draw_square(surf, color, start, end, thickness):
    side = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
    x = start[0] if end[0] > start[0] else start[0] - side
    y = start[1] if end[1] > start[1] else start[1] - side
    pygame.draw.rect(surf, color, (x, y, side, side), thickness)

def draw_equi_tri(surf, color, start, end, thickness):
    side = math.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
    height = (math.sqrt(3)/2) * side
    p1 = start
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side/2, start[1] - height)
    pygame.draw.polygon(surf, color, [p1, p2, p3], thickness)

def draw_right_tri(surf, color, start, end, thickness):
    points = [start, end, (start[0], end[1])]
    pygame.draw.polygon(surf, color, points, thickness)

def draw_rhombus(surf, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
    pygame.draw.polygon(surf, color, points, thickness)