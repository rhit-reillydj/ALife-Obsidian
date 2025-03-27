import pygame
import numpy as np
import math
from pygame import gfxdraw
from collections import deque

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Optimization parameters
GRID_CELL_SIZE = 20
GRAVITY_MULTIPLIER = 1
DISPLACEMENT_MULTIPLIER = 15
MAX_DISPLACEMENT = 250

class CelestialBody:
    __slots__ = ['x', 'y', 'mass', 'color', 'radius', 'angle', 'orbital_speed', 'orbit_radius', 'gravity_scale']
    
    def __init__(self, x, y, mass, color, radius, orbital_speed=0, gravity_scale=1.0):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.angle = 0
        self.orbital_speed = orbital_speed
        self.orbit_radius = math.hypot(x - WIDTH/2, y - HEIGHT/2)
        self.gravity_scale = gravity_scale

    def update_position(self):
        if self.orbital_speed:
            self.angle += self.orbital_speed
            self.x = WIDTH/2 + math.cos(self.angle) * self.orbit_radius
            self.y = HEIGHT/2 + math.sin(self.angle) * self.orbit_radius

class Probe:
    __slots__ = ['x', 'y', 'vx', 'vy', 'active', 'trail']
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.active = False
        self.trail = deque(maxlen=40)

    def update(self, bodies):
        if self.active:
            for body in bodies:
                dx = body.x - self.x
                dy = body.y - self.y
                dist_sq = dx*dx + dy*dy
                if dist_sq > (body.radius**2):
                    dist = math.sqrt(dist_sq)
                    force = (body.mass * GRAVITY_MULTIPLIER * body.gravity_scale) / (dist**1.2 + 1e-6)
                    self.vx += force * dx / dist * 0.5
                    self.vy += force * dy / dist * 0.5
            
            self.trail.append((self.x, self.y))
            self.x += self.vx
            self.y += self.vy

def create_grid(bodies):
    grid_w = WIDTH // GRID_CELL_SIZE + 1
    grid_h = HEIGHT // GRID_CELL_SIZE + 1
    
    x_grid, y_grid = np.meshgrid(
        np.arange(grid_w) * GRID_CELL_SIZE,
        np.arange(grid_h) * GRID_CELL_SIZE,
        indexing='ij'
    )
    
    displacement = np.zeros((grid_w, grid_h, 2))
    strength_grid = np.zeros((grid_w, grid_h))
    
    for body in bodies:
        dx = body.x - x_grid
        dy = body.y - y_grid
        dist = np.hypot(dx, dy)
        softening = body.radius * 2.5
        
        strength = (body.mass * body.gravity_scale) / ((dist**1.2) + (softening**1.2))
        angle = np.arctan2(dy, dx)
        
        disp_mag = np.minimum(strength * DISPLACEMENT_MULTIPLIER, MAX_DISPLACEMENT)
        displacement[..., 0] += np.cos(angle) * disp_mag
        displacement[..., 1] += np.sin(angle) * disp_mag
        np.maximum(strength_grid, strength, out=strength_grid)
    
    grid = np.stack([x_grid, y_grid], axis=-1) + displacement
    grid = np.clip(grid, [-1000, -1000], [WIDTH+1000, HEIGHT+1000])
    
    return grid, strength_grid

def draw_grid(grid, strength_grid):
    grid_w, grid_h = grid.shape[:2]
    max_strength = np.max(strength_grid)
    
    # Create blue gradient based on strength
    blue_intensity = np.clip(strength_grid / max_strength if max_strength else 0, 0, 1)
    blue_colors = (blue_intensity * 255).astype(int)
    
    for i in range(grid_w-1):
        for j in range(grid_h-1):
            # Calculate average blue intensity for the cell
            avg_blue = int(np.mean(blue_colors[i:i+2, j:j+2]))
            
            # Only draw if there's significant blue intensity
            if avg_blue > 10:
                points = [
                    (int(grid[i,j,0]), int(grid[i,j,1])),
                    (int(grid[i+1,j,0]), int(grid[i+1,j,1])),
                    (int(grid[i+1,j+1,0]), int(grid[i+1,j+1,1])),
                    (int(grid[i,j+1,0]), int(grid[i,j+1,1]))
                ]
                color = (0, 0, min(255, avg_blue))
                gfxdraw.filled_polygon(screen, points, color)
                gfxdraw.aapolygon(screen, points, BLACK)

def main():
    # Create celestial bodies with individual gravity scaling
    bodies = [
        # Sun (weaker gravity)
        CelestialBody(WIDTH/2, HEIGHT/2, 1000, (255,255,0), 40, gravity_scale=0.5),
        
        # Planets (stronger gravity)
        CelestialBody(WIDTH/2 + 250, HEIGHT/2, 150, (0,128,255), 16, 0.018, gravity_scale=2.0),  # Earth
        CelestialBody(WIDTH/2 + 400, HEIGHT/2, 120, (255,50,50), 14, 0.014, gravity_scale=2.5),  # Mars
        CelestialBody(WIDTH/2 + 550, HEIGHT/2, 200, (255,150,0), 18, 0.012, gravity_scale=3.0),  # Jupiter
        CelestialBody(WIDTH/2 + 150, HEIGHT/2, 80, (200,200,200), 12, 0.022, gravity_scale=1.8), # Mercury
        CelestialBody(WIDTH/2 + 700, HEIGHT/2, 180, (255,200,0), 16, 0.01, gravity_scale=2.8)    # Saturn
    ]
    
    probe = Probe()

    running = True
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                probe.x, probe.y = event.pos
                probe.vx = probe.vy = 0
                probe.active = True
                probe.trail.clear()

        for body in bodies:
            body.update_position()
        
        grid, strength_grid = create_grid(bodies)
        draw_grid(grid, strength_grid)
        
        probe.update(bodies)
        if probe.active:
            for i, pos in enumerate(probe.trail):
                alpha = 255 * (i/len(probe.trail))
                pygame.draw.circle(screen, (255,255,255, alpha), pos, 2)
            pygame.draw.circle(screen, WHITE, (int(probe.x), int(probe.y)), 4)
        
        for body in bodies:
            pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), body.radius)
            pygame.draw.circle(screen, WHITE, (int(body.x), int(body.y)), body.radius+2, 2)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()