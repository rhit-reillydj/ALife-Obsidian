import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Set up simulation grid for warp field with reduced resolution
x_min, x_max = -15, 15
y_min, y_max = -15, 15
nx, ny = 150, 150  # lower resolution for speed
x = np.linspace(x_min, x_max, nx)
y = np.linspace(y_min, y_max, ny)
X, Y = np.meshgrid(x, y)

# Simulation parameters
dt = 0.05         # time step
G = 2.0           # gravitational constant (scaled for demo effect)
warp_width = 2.5  # controls width of warp dips
epsilon = 0.5     # gravitational softening to avoid extreme accelerations
warp_update_interval = 3  # update warp field every 3 frames

# Define bodies (Sun + planets) with visual and orbital parameters
bodies = [
    {'name': 'Sun',     'mass': 1000, 'orbit': 0,  'omega': 0,   'phase': 0,   'color': 'yellow',    'radius': 1.2},
    {'name': 'Mercury', 'mass': 50,   'orbit': 3,  'omega': 2.0, 'phase': 0,   'color': 'lightgrey', 'radius': 0.3},
    {'name': 'Venus',   'mass': 70,   'orbit': 4,  'omega': 1.6, 'phase': 0.5, 'color': 'orange',    'radius': 0.5},
    {'name': 'Earth',   'mass': 80,   'orbit': 5,  'omega': 1.4, 'phase': 1.0, 'color': 'blue',      'radius': 0.5},
    {'name': 'Mars',    'mass': 40,   'orbit': 6,  'omega': 1.2, 'phase': 1.5, 'color': 'red',       'radius': 0.4},
    {'name': 'Jupiter', 'mass': 300,  'orbit': 8,  'omega': 1.0, 'phase': 0.8, 'color': 'saddlebrown','radius': 0.9},
    {'name': 'Saturn',  'mass': 250,  'orbit': 10, 'omega': 0.9, 'phase': 1.2, 'color': 'gold',      'radius': 0.8},
]

# Test object (massless) dropped via a mouse click
test_object = None

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8,8))
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal')
ax.set_title("Optimized Warped Space-Time Solar System Demo")

# Initialize the warp field image with a smooth colormap
warp_field = np.zeros_like(X)
warp_im = ax.imshow(warp_field, extent=(x_min, x_max, y_min, y_max),
                    origin='lower', cmap='coolwarm', alpha=0.6)

# Create planet patches using Circle patches
planet_patches = []
for body in bodies:
    if body['orbit'] == 0:
        patch = Circle((0, 0), body['radius'], color=body['color'],
                       ec='darkorange', lw=2, zorder=3)
    else:
        patch = Circle((body['orbit'], 0), body['radius'], color=body['color'],
                       ec='black', lw=1, zorder=3)
    planet_patches.append(patch)
    ax.add_patch(patch)

# Create a patch for the test object (a small white circle)
test_patch = Circle((0, 0), 0.2, color='white', ec='black', lw=1, zorder=4)
ax.add_patch(test_patch)
test_patch.set_visible(False)

# Dynamically set contour levels to emphasize the warp field
max_mass = max(body['mass'] for body in bodies)
contour_levels = np.linspace(-max_mass * 1.2, 0, 10)
contour_plot = ax.contour(X, Y, warp_field, levels=contour_levels,
                          colors='black', linewidths=0.5, alpha=0.5)

def compute_body_position(body, t):
    """Return the (x, y) position for a body at time t."""
    if body['orbit'] == 0:
        return np.array([0, 0])
    angle = body['omega'] * t + body['phase']
    return np.array([body['orbit'] * np.cos(angle), body['orbit'] * np.sin(angle)])

def compute_warp_field(t):
    """Calculate the warp field as a sum of dips from each body."""
    Z = np.zeros_like(X)
    for body in bodies:
        pos = compute_body_position(body, t)
        Z += -body['mass'] * np.exp(-((X - pos[0])**2 + (Y - pos[1])**2) / warp_width**2)
    return Z

def update(frame):
    global test_object, contour_plot, warp_field
    t = frame * dt

    # Update positions of planets
    positions = []
    for i, body in enumerate(bodies):
        pos = compute_body_position(body, t)
        positions.append(pos)
        planet_patches[i].center = pos

    # Update warp field and contour lines only every few frames
    if frame % warp_update_interval == 0:
        warp_field = compute_warp_field(t)
        warp_im.set_data(warp_field)
        # Remove old contours and redraw new ones for clarity
        for coll in contour_plot.collections:
            coll.remove()
        contour_plot = ax.contour(X, Y, warp_field, levels=contour_levels,
                                  colors='black', linewidths=0.5, alpha=0.5)

    # Update test object dynamics if it exists
    if test_object is not None:
        pos = test_object['pos']
        vel = test_object['vel']
        total_acc = np.array([0.0, 0.0])
        for body, p in zip(bodies, positions):
            disp = p - pos
            r = np.linalg.norm(disp)
            # Use gravitational softening to smooth accelerations
            r_soft = np.sqrt(r**2 + epsilon**2)
            acc = (G * body['mass'] / r_soft**3) * disp
            total_acc += acc
        vel += total_acc * dt
        pos += vel * dt
        test_object['vel'] = vel
        test_object['pos'] = pos
        test_patch.center = pos
        test_patch.set_visible(True)
    return planet_patches + [warp_im, test_patch] + contour_plot.collections

def on_click(event):
    global test_object
    if event.inaxes != ax:
        return
    # Left-click: drop (or reposition) the test object
    if event.button == 1:
        if test_object is None:
            test_object = {
                'pos': np.array([event.xdata, event.ydata]),
                'vel': np.array([0.0, 0.0])
            }
        else:
            test_object['pos'] = np.array([event.xdata, event.ydata])
            test_object['vel'] = np.array([0.0, 0.0])
    # Right-click: remove the test object
    elif event.button == 3:
        test_object = None
        test_patch.set_visible(False)

fig.canvas.mpl_connect('button_press_event', on_click)

anim = FuncAnimation(fig, update, frames=600, interval=30, blit=False)
plt.show()