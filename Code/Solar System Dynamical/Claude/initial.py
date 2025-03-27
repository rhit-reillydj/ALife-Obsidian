import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors

# Constants
G = 6.67430e-11  # Gravitational constant
SUN_MASS = 1.989e30  # Mass of the Sun in kg
SCALING_FACTOR = 1e9  # Scaling factor for visualization

# Planet data: [name, mass (kg), distance from sun (m), orbital velocity (m/s), color]
planets = [
    ["Mercury", 3.301e23, 5.791e10, 47400, "gray"],
    ["Venus", 4.867e24, 1.082e11, 35000, "bisque"],
    ["Earth", 5.972e24, 1.496e11, 29800, "dodgerblue"],
    ["Mars", 6.417e23, 2.279e11, 24100, "indianred"],
    ["Jupiter", 1.898e27, 7.786e11, 13100, "burlywood"],
    ["Saturn", 5.683e26, 1.434e12, 9700, "khaki"],
    ["Uranus", 8.681e25, 2.871e12, 6800, "lightblue"],
    ["Neptune", 1.024e26, 4.495e12, 5400, "royalblue"]
]

def create_grid(size=100, resolution=50):
    """Create a grid for spacetime fabric visualization."""
    x = np.linspace(-size, size, resolution)
    y = np.linspace(-size, size, resolution)
    return np.meshgrid(x, y)

def calculate_spacetime_warp(x_grid, y_grid, bodies):
    """Calculate the spacetime warping caused by massive bodies."""
    z_grid = np.zeros_like(x_grid)
    
    for body in bodies:
        mass = body[0]
        pos_x, pos_y = body[1], body[2]
        
        # Calculate distance from each point to the body
        distance = np.sqrt((x_grid - pos_x)**2 + (y_grid - pos_y)**2)
        
        # Add warping effect (simplified gravitational potential)
        # Adding a small constant to avoid division by zero
        z_grid -= (mass * SCALING_FACTOR) / (distance + 1)
    
    return z_grid

def update(frame, ax, scatter_objects, fabric_surface, probe_scatter):
    """Update function for animation."""
    ax.clear()
    
    # Set plot limits and labels
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)
    ax.set_zlim(-50, 10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z (Spacetime Warp)')
    ax.set_title('Solar System Spacetime Warping Visualization', fontsize=14)
    
    # Update positions of planets
    updated_bodies = []
    scatter_objects = []
    
    # Sun position is fixed at the center
    sun_pos = [0, 0]
    sun_mass = SUN_MASS / 1e25  # Scaled for visualization
    updated_bodies.append([sun_mass, sun_pos[0], sun_pos[1]])
    
    # Draw the Sun
    sun_scatter = ax.scatter(sun_pos[0], sun_pos[1], 0, color='yellow', s=500, edgecolor='orange', alpha=0.7)
    scatter_objects.append(sun_scatter)
    
    # Update planet positions based on orbital motion
    for i, planet in enumerate(planets):
        name, mass, distance, velocity, color = planet
        
        # Calculate angular velocity (ω = v/r)
        angular_velocity = velocity / distance
        
        # Calculate new position based on time
        angle = (frame * angular_velocity / 500) % (2 * np.pi)
        x = distance * np.cos(angle) / 1e10
        y = distance * np.sin(angle) / 1e10
        
        # Scale mass for visualization
        visual_mass = mass / 1e25
        
        # Store updated positions and masses
        updated_bodies.append([visual_mass, x, y])
        
        # Draw the planet
        size = max(100, np.log10(mass) * 10)
        planet_scatter = ax.scatter(x, y, 0, color=color, s=size, edgecolor='white', alpha=0.8)
        scatter_objects.append(planet_scatter)
        
        # Add planet name
        ax.text(x, y, 2, name, fontsize=8, ha='center', va='bottom')
    
    # Create the spacetime fabric
    x_grid, y_grid = create_grid(size=150, resolution=50)
    z_grid = calculate_spacetime_warp(x_grid, y_grid, updated_bodies)
    
    # Normalize z_grid for better visualization
    z_grid = np.clip(z_grid, -50, 10)
    
    # Draw the warped spacetime fabric
    fabric_surface = ax.plot_surface(
        x_grid, y_grid, z_grid, 
        cmap='Blues_r', 
        alpha=0.6,
        antialiased=True,
        norm=colors.PowerNorm(gamma=0.5)
    )
    
    # Update probe position if it exists
    if frame > 20:  # Start the probe after 20 frames
        # Initialize probe position if it doesn't exist
        if frame == 21:
            probe_pos = [130, 0, 0]
            probe_vel = [-0.5, 0.1, 0]
        else:
            probe_pos = probe_scatter._offsets3d
            probe_vel = getattr(probe_scatter, 'velocity', [-0.5, 0.1, 0])
        
        # Calculate gravitational influence on the probe
        ax_probe = 0
        ay_probe = 0
        
        for body in updated_bodies:
            mass, bx, by = body
            dx = bx - probe_pos[0]
            dy = by - probe_pos[1]
            r = np.sqrt(dx**2 + dy**2)
            
            if r > 0.1:  # Avoid extremely close encounters
                force = 0.1 * mass / (r**2)  # Simplified gravitational force
                ax_probe += force * dx / r
                ay_probe += force * dy / r
        
        # Update probe velocity and position
        probe_vel[0] += ax_probe
        probe_vel[1] += ay_probe
        
        new_x = probe_pos[0] + probe_vel[0]
        new_y = probe_pos[1] + probe_vel[1]
        
        # Calculate z-position based on spacetime warping
        grid_size = x_grid.shape[0]
        grid_half = grid_size // 2
        
        # Map probe coordinates to grid indices
        ix = int(np.clip((new_x + 150) * grid_size / 300, 0, grid_size - 1))
        iy = int(np.clip((new_y + 150) * grid_size / 300, 0, grid_size - 1))
        
        # Get z value from spacetime grid
        new_z = z_grid[iy, ix]
        
        # Draw the probe
        probe_scatter = ax.scatter(new_x, new_y, new_z, color='red', s=100, marker='o', edgecolor='white')
        probe_scatter._offsets3d = (new_x, new_y, new_z)
        probe_scatter.velocity = probe_vel
    else:
        probe_scatter = ax.scatter(0, 0, 0, alpha=0)  # Invisible placeholder
    
    # Set the viewing angle
    ax.view_init(elev=30, azim=frame / 2)
    
    return scatter_objects + [fabric_surface, probe_scatter]

# Create the figure and 3D axis
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Initial fabric and scatter objects
x_grid, y_grid = create_grid()
initial_bodies = [[SUN_MASS / 1e25, 0, 0]]  # Just the sun initially
z_grid = calculate_spacetime_warp(x_grid, y_grid, initial_bodies)
fabric_surface = ax.plot_surface(x_grid, y_grid, z_grid, cmap='Blues_r', alpha=0.6)
scatter_objects = []
probe_scatter = ax.scatter(0, 0, 0, alpha=0)  # Initial invisible probe

# Create animation
ani = FuncAnimation(
    fig, 
    update, 
    frames=200, 
    fargs=(ax, scatter_objects, fabric_surface, probe_scatter),
    interval=50,
    blit=False
)

# Save the animation (optional)
# ani.save('solar_system_spacetime.mp4', writer='ffmpeg', fps=20, dpi=100)

plt.tight_layout()
plt.show()