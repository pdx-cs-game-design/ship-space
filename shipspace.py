# Framework based on https://realpython.com/pygame-a-primer

import pygame
from math import pi, sin, cos

pygame.init()

# Width of a "vector".
vwidth = 3
# Color of a "vector".
vcolor = (0, 255, 0)

# Dimensions of screen.
sdim = (800, 800)
sdim_x, sdim_y = sdim
# Center of screen.
scenter = (sdim[0] // 2, sdim[1] // 2)
scenter_x, scenter_y = scenter

# Scale of spaceship.
scale = 0.10 * min(sdim_x, sdim_y)

# Set up the drawing window
screen = pygame.display.set_mode(sdim)

def vector(start, end):
    start_x, start_y = start
    end_x, end_y = end
    start = (start_x, sdim_y - start_y)
    end = (end_x, sdim_y - end_y)
    pygame.draw.line(screen, vcolor, start, end, width=vwidth)

# Facing right
spaceship_model = (
    (0.2, 0.75),
    (1.0, 0.5),
    (0.2, 0.25),
    (0.35, 0.5),
)

def rotate(p, rot):
    x, y = p
    return (
        x * cos(rot) - y * sin(rot),
        x * sin(rot) + y * cos(rot),
    )

def display(display_list, posn, rot):
    scaled = [(x * scale, y * scale) for x, y in display_list]
    rotated = [rotate(p, rot) for p in scaled]
    x_posn, y_posn = posn
    translated = [(x + x_posn, y + y_posn) for (x, y) in rotated]
    npoints = len(translated)
    vecs = [
        (translated[i], translated[(i + 1) % npoints])
        for i in range(npoints)
    ]
    for start, end in vecs:
        vector(start, end)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background.
    screen.fill((0, 0, 0))

    # Draw a spaceship in the lower left quadrant facing up-right
    display(spaceship_model, (sdim_x / 4, sdim_y / 4), pi/4)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
