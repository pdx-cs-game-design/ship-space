# Spaceship Game
# Bart Massey and Portland State CS 410/510 Game Design 2023

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
sdim_min = min(sdim_x, sdim_y)
# Center of screen.
scenter = (sdim[0] // 2, sdim[1] // 2)
scenter_x, scenter_y = scenter

# Scale of spaceship.
scale = 0.10 * sdim_min
# Maximum spaceship velocity, because space friction.
v_max = 3

screen = pygame.display.set_mode(sdim)

def vector(start, end):
    start_x, start_y = start
    end_x, end_y = end
    start = (start_x, sdim_y - start_y)
    end = (end_x, sdim_y - end_y)
    pygame.draw.line(screen, vcolor, start, end, width=vwidth)

# Facing right, unit size.
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

class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rot = 0
        # Velocities
        self.vx = 0
        self.vy = 0
        # Accelerations
        self.ax = 0
        self.ay = 0
        self.model = spaceship_model

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx = min(self.vx + self.ax * dt, v_max)
        self.vy = min(self.vy + self.ay * dt, v_max)
        while self.x < 0:
            self.x += sdim_x
        while self.y < 0:
            self.y += sdim_y
        while self.x > sdim_x:
            self.x -= sdim_x
        while self.y > sdim_x:
            self.y -= sdim_y

    def rotate(self, dr):
        self.rot += dr
        self.vx, self.vy = rotate((self.vx, self.vy), self.rot)
        self.ax, self.ay = rotate((self.ax, self.ay), self.rot)

    def thrust(self, a):
        ax, ay = rotate((a, 0), self.rot)
        self.ax = ax
        self.ay = ay

    def render(self):
        display(self.model, (self.x, self.y), self.rot)

ship = Spaceship(sdim_x / 4, sdim_y / 4)
ship.thrust(sdim_min / 10)
ship.rotate(pi / 6)

running = True
while running:
    # Get user input.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    ship.update(0.01)
    ship.render()
    pygame.display.flip()

pygame.quit()
