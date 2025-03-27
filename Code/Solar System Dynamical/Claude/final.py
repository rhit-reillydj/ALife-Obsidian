import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import datetime  # Use the standard datetime module instead

# Planet data: [name, mass (relative), distance, color]
planets = [
    ["Mercury", 0.1, 4, "gray"],
    ["Venus", 0.2, 7, "bisque"],
    ["Earth", 0.3, 10, "dodgerblue"],
    ["Mars", 0.15, 15, "indianred"],
    ["Jupiter", 2.0, 22, "burlywood"],
    ["Saturn", 1.8, 30, "khaki"],
    ["Uranus", 0.8, 36, "lightblue"],
    ["Neptune", 1.0, 42, "royalblue"]
]

# Create figure and 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Create mesh for spacetime fabric - super low resolution for better performance
resolution = 12  # Very low resolution for speed
grid_size = 50
x = np.linspace(-grid_size, grid_size, resolution)
y = np.linspace(-grid_size, grid_size, resolution)
x_mesh, y_mesh = np.meshgrid(x, y)

# Function to calculate spacetime warping
def calculate_warp(x_mesh, y_mesh, objects):
    z_mesh = np.zeros_like(x_mesh)
    for mass, x_pos, y_pos in objects:
        # Simplified distance calculation
        distance = np.sqrt((x_mesh - x_pos)**2 + (y_mesh - y_pos)**2) + 0.5
        # Add depression based on mass
        z_mesh += -mass / distance
    return z_mesh

# Speed control - increase for faster animation
speed_factor = 5.0

# Initial setup for planets (including the sun)
num_objects = len(planets) + 1
initial_xs = np.zeros(num_objects)
initial_ys = np.zeros(num_objects)
initial_zs = np.zeros(num_objects)
initial_sizes = np.zeros(num_objects)
initial_sizes[0] = 30  # Sun size

# Colors for all objects including the sun
colors = ['yellow'] + [p[3] for p in planets]

# Initial scatter plot with correct dimensions
planet_scatter = ax.scatter(initial_xs, initial_ys, initial_zs, s=initial_sizes, c=colors)

# Initial surface plot
initial_z_mesh = np.zeros_like(x_mesh)
surface = ax.plot_surface(x_mesh, y_mesh, initial_z_mesh, cmap='Blues', 
                         alpha=0.6, linewidth=0, antialiased=False)

# Initialize probe
probe_pos = np.array([40.0, 0.0, 0.0])
probe_vel = np.array([-0.5, 0.2, 0.0])
probe_scatter = ax.scatter([probe_pos[0]], [probe_pos[1]], [0], color='red', s=50)
probe_active = False

# FPS tracking
time_text = ax.text2D(0.02, 0.98, '', transform=ax.transAxes)
last_frame_time = datetime.datetime.now()  # Using standard datetime
fps_history = []

# Pre-calculate some values to improve performance
frame_count = 0
warp_update_freq = 3  # Update spacetime warp every X frames
view_update_freq = 6  # Update view angle every X frames

def update(frame):
    global surface, probe_active, probe_pos, probe_vel, last_frame_time, fps_history, frame_count
    
    frame_count += 1
    
    # Calculate FPS
    current_time = datetime.datetime.now()  # Using standard datetime
    delta = (current_time - last_frame_time).total_seconds()
    last_frame_time = current_time
    if delta > 0:
        fps = 1.0 / delta
        fps_history.append(fps)
        if len(fps_history) > 5:
            fps_history.pop(0)
        avg_fps = sum(fps_history) / len(fps_history)
        time_text.set_text(f'FPS: {avg_fps:.1f}')
    
    # Clear old surface plot - using a safer method
    if hasattr(ax, 'collections'):
        for coll in list(ax.collections):
            if not (coll is planet_scatter or coll is probe_scatter):
                try:
                    coll.remove()
                except:
                    pass
    
    # Update positions
    xs = np.zeros(num_objects)
    ys = np.zeros(num_objects)
    zs = np.zeros(num_objects)
    sizes = np.zeros(num_objects)
    
    # Sun at the center
    xs[0], ys[0], zs[0] = 0, 0, 0
    sizes[0] = 30
    
    # Objects for calculating spacetime warp
    objects = [[10.0, 0, 0]]  # Sun
    
    # Update planets
    for i, planet in enumerate(planets):
        name, mass, distance, color = planet
        # Faster orbital speed for inner planets
        orbital_speed = 1 / np.sqrt(distance) * speed_factor
        angle = (frame * orbital_speed * 0.1) % (2 * np.pi)
        
        x = distance * np.cos(angle)
        y = distance * np.sin(angle)
        
        xs[i+1], ys[i+1], zs[i+1] = x, y, 0
        sizes[i+1] = mass * 10 + 5
        objects.append([mass, x, y])
    
    # Update planet scatter plot
    planet_scatter._offsets3d = (xs, ys, zs)
    planet_scatter.set_sizes(sizes)
    
    # Only calculate spacetime warp occasionally for performance
    if frame_count % warp_update_freq == 0:
        try:
            z_mesh = calculate_warp(x_mesh, y_mesh, objects)
            surface = ax.plot_surface(x_mesh, y_mesh, z_mesh, cmap='Blues', 
                                    alpha=0.6, linewidth=0, antialiased=False, 
                                    rcount=resolution, ccount=resolution)
        except Exception as e:
            print(f"Error updating surface: {e}")
    
    # Update probe
    if frame > 5:  # Start probe sooner
        if not probe_active:
            probe_active = True
            
        # Calculate gravitational forces
        accel = np.zeros(3)
        for mass, x, y in objects:
            direction = np.array([x, y, 0]) - probe_pos
            distance = np.linalg.norm(direction)
            if distance > 0.5:
                force = mass / (distance**2)
                accel += (direction / distance) * force
        
        # Update velocity and position
        probe_vel += accel * 0.1
        probe_vel *= 0.98  # Add damping
        probe_pos += probe_vel * 0.1
        
        # Approximate probe height
        min_dist = float('inf')
        closest_obj = None
        
        for mass, x, y in objects:
            dist = np.sqrt((probe_pos[0] - x)**2 + (probe_pos[1] - y)**2)
            if dist < min_dist:
                min_dist = dist
                closest_obj = (mass, x, y)
        
        # Simple approximation instead of mesh lookup
        if closest_obj:
            mass, x, y = closest_obj
            probe_pos[2] = -mass / (min_dist + 0.5)
        
        # Update probe scatter
        probe_scatter._offsets3d = ([probe_pos[0]], [probe_pos[1]], [probe_pos[2]])
    
    # Update view angle less frequently
    if frame_count % view_update_freq == 0:
        ax.view_init(elev=30, azim=frame / 8)  # Slower rotation
    
    return planet_scatter, probe_scatter, time_text

# Set up the scene
ax.set_xlim(-grid_size, grid_size)
ax.set_ylim(-grid_size, grid_size)
ax.set_zlim(-15, 5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Spacetime Warp')
ax.set_title('Solar System Spacetime Visualization')

# Create animation with faster frame rate
anim = FuncAnimation(fig, update, frames=500, interval=10, blit=False)

plt.tight_layout()
plt.show()