# Spaceship Game
# Bart Massey and Portland State CS 410/510 Game Design 2023

# Framework based on https://realpython.com/pygame-a-primer

import pygame
from math import pi, sin, cos, sqrt

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
v_max = 20
# Rotation velocity when key is held.
v_rot = pi / 24
# Acceleration when thruster is held.
a_thrust = 5
# Space friction reduces velocity.
space_friction = 0.9995

screen = pygame.display.set_mode(sdim)

def vector(start, end):
    start_x, start_y = start
    end_x, end_y = end
    start = (start_x, sdim_y - start_y)
    end = (end_x, sdim_y - end_y)
    pygame.draw.line(screen, vcolor, start, end, width=vwidth)

def point(posn):
    x, y = posn
    rect = pygame.Rect(x, sdim_y - y, vwidth, vwidth)
    pygame.draw.rect(screen, vcolor, rect)

# Facing right, unit size.
spaceship_model = (
    (-0.3, 0.25),
    (0.5, 0.0),
    (-0.3, -0.25),
    (-0.15, 0.0),
)

def rotate(p, rot, center = (0, 0)):
    x, y = p
    cx, cy = center
    x -= cx
    y -= cy
    rx = x * cos(rot) - y * sin(rot) + cx
    ry = x * sin(rot) + y * cos(rot) + cy
    return (rx, ry)

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
    # Show axis of rotation.
    #point(posn)

class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Rotation.
        self.rot = 0
        # Rotational velocity.
        self.vrot = 0
        # Velocity.
        self.vx = 0
        self.vy = 0
        # Acceleration.
        self.a = 0
        self.model = spaceship_model

    def update(self, dt):
        rx, ry = rotate((1.0, 0.0), self.rot)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx += self.a * rx * dt
        self.vx *= space_friction
        self.vy += self.a * ry * dt
        self.vy *= space_friction
        self.rot += self.vrot * dt
        
        v2 = self.vx**2 + self.vy**2
        if v2 > v_max**2:
            s = sqrt(v2)
            self.vx = v_max * self.vx / s
            self.vy = v_max * self.vy / s

        if self.x < 0:
            self.x += sdim_x
        if self.y < 0:
            self.y += sdim_y
        if self.x > sdim_x:
            self.x -= sdim_x
        if self.y > sdim_x:
            self.y -= sdim_y

        if self.rot < 0:
            self.rot += 2 * pi
        if self.rot > 2 * pi:
            self.rot -= 2 * pi

    def rotation(self, vrot):
        self.vrot = vrot

    def thrust(self, a):
        self.a = a

    def render(self):
        display(self.model, (self.x, self.y), self.rot)

ship = Spaceship(sdim_x / 4, sdim_y / 4)

running = True
while running:
    # Get user input.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.rotation(v_rot)
            elif event.key == pygame.K_RIGHT:
                ship.rotation(-v_rot)
            elif event.key == pygame.K_UP:
                ship.thrust(a_thrust)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ship.rotation(0)
            elif event.key == pygame.K_RIGHT:
                ship.rotation(0)
            elif event.key == pygame.K_UP:
                ship.thrust(0)

    screen.fill((0, 0, 0))
    ship.update(0.01)
    ship.render()
    pygame.display.flip()

pygame.quit()
