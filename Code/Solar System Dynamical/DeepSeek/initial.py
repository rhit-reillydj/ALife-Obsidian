import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (150, 150, 150)

# Grid parameters
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

class CelestialBody:
    def __init__(self, x, y, mass, color, radius, orbital_speed=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.angle = 0
        self.orbital_speed = orbital_speed
        self.orbit_radius = math.hypot(x - WIDTH/2, y - HEIGHT/2)

    def update_position(self):
        if self.orbital_speed != 0:
            self.angle += self.orbital_speed
            self.x = WIDTH/2 + math.cos(self.angle) * self.orbit_radius
            self.y = HEIGHT/2 + math.sin(self.angle) * self.orbit_radius

class Probe:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.active = False

    def update(self, bodies):
        if self.active:
            for body in bodies:
                dx = body.x - self.x
                dy = body.y - self.y
                dist = math.hypot(dx, dy)
                if dist > body.radius:
                    force = body.mass / (dist**2 + 1e-6)
                    self.vx += force * dx / dist * 0.1
                    self.vy += force * dy / dist * 0.1
            self.x += self.vx
            self.y += self.vy

def create_grid(bodies):
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT, 2))
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            x = i * GRID_SIZE
            y = j * GRID_SIZE
            dx_total, dy_total = 0, 0
            
            for body in bodies:
                dx = body.x - x
                dy = body.y - y
                dist = math.hypot(dx, dy)
                strength = body.mass / (dist**2 + 1e-6)
                dx_total += dx * strength * 0.001
                dy_total += dy * strength * 0.001
                
            grid[i][j] = [x + dx_total, y + dy_total]
    return grid

def draw_grid(grid):
    for i in range(GRID_WIDTH-1):
        for j in range(GRID_HEIGHT-1):
            pygame.draw.line(screen, GRAY, grid[i][j], grid[i+1][j], 1)
            pygame.draw.line(screen, GRAY, grid[i][j], grid[i][j+1], 1)

def main():
    sun = CelestialBody(WIDTH/2, HEIGHT/2, 500, YELLOW, 30)
    earth = CelestialBody(WIDTH/2 + 200, HEIGHT/2, 50, BLUE, 15, 0.02)
    mars = CelestialBody(WIDTH/2 + 300, HEIGHT/2, 40, RED, 12, 0.015)
    bodies = [sun, earth, mars]
    probe = Probe()

    running = True
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                probe.x, probe.y = pygame.mouse.get_pos()
                probe.vx = 0
                probe.vy = 0
                probe.active = True

        for body in bodies:
            body.update_position()

        grid = create_grid(bodies)
        draw_grid(grid)

        probe.update(bodies)
        if probe.active:
            pygame.draw.circle(screen, WHITE, (int(probe.x), int(probe.y)), 3)

        for body in bodies:
            pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), body.radius)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()