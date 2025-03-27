import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up the simulation domain and grid for the "warped tarp"
x_min, x_max = -15, 15
y_min, y_max = -15, 15
nx, ny = 300, 300
x = np.linspace(x_min, x_max, nx)
y = np.linspace(y_min, y_max, ny)
X, Y = np.meshgrid(x, y)

# Simulation parameters
dt = 0.1         # time step
G = 1.0          # gravitational constant (arbitrary units)
warp_width = 3.0  # controls how wide each planet's dip appears

# Define our bodies
# For each body, orbit is the distance from center (0 means fixed, e.g. Sun)
# omega is the angular speed, and phase is initial phase offset.
bodies = [
    {'name': 'Sun',     'mass': 1000, 'orbit': 0, 'omega': 0,   'phase': 0,   'color': 'yellow', 'size': 200},
    {'name': 'Mercury', 'mass': 3,    'orbit': 3, 'omega': 1.6, 'phase': 0,   'color': 'grey',   'size': 30},
    {'name': 'Venus',   'mass': 4,    'orbit': 4, 'omega': 1.2, 'phase': 1.0, 'color': 'orange', 'size': 40},
    {'name': 'Earth',   'mass': 5,    'orbit': 5, 'omega': 1.0, 'phase': 2.0, 'color': 'blue',   'size': 40},
    {'name': 'Mars',    'mass': 2.5,  'orbit': 6, 'omega': 0.8, 'phase': 1.5, 'color': 'red',    'size': 30},
    {'name': 'Jupiter', 'mass': 10,   'orbit': 8, 'omega': 0.6, 'phase': 0.5, 'color': 'brown',  'size': 60},
    {'name': 'Saturn',  'mass': 9,    'orbit': 10,'omega': 0.5, 'phase': 1.2, 'color': 'gold',   'size': 50},
]

# Initialize the dropped object (None until the user clicks)
test_object = None

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8,8))
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal')
ax.set_title("Solar System Space-Time Warp Demo")

# Plot the initial warped background (we will update its data)
warp_im = ax.imshow(np.zeros_like(X), extent=(x_min,x_max,y_min,y_max),
                    origin='lower', cmap='plasma', alpha=0.6)

# Prepare scatter artists for bodies
scatter = ax.scatter([], [], s=[], c=[])

# Prepare artist for the test object (if any)
test_scatter = ax.scatter([], [], s=50, c='white', marker='o')

def compute_body_position(body, t):
    """Return (x, y) position for a body given time t."""
    if body['orbit'] == 0:  # e.g., the Sun
        return 0, 0
    angle = body['omega'] * t + body['phase']
    x_pos = body['orbit'] * np.cos(angle)
    y_pos = body['orbit'] * np.sin(angle)
    return x_pos, y_pos

def compute_warp_field(t):
    """Compute the warped field Z(x,y) from all bodies."""
    Z = np.zeros_like(X)
    for body in bodies:
        bx, by = compute_body_position(body, t)
        # Add a dip for each body (the warp is deeper for higher mass)
        Z += -body['mass'] * np.exp(-((X - bx)**2 + (Y - by)**2) / warp_width**2)
    return Z

def update(frame):
    global test_object
    t = frame * dt

    # Update bodies positions
    positions = [compute_body_position(body, t) for body in bodies]
    xs, ys = zip(*positions)
    sizes = [body['size'] for body in bodies]
    colors = [body['color'] for body in bodies]
    scatter.set_offsets(np.column_stack((xs, ys)))
    scatter.set_sizes(sizes)
    scatter.set_color(colors)

    # Update the warped background field
    Z = compute_warp_field(t)
    warp_im.set_data(Z)

    # If a test object exists, update its motion due to gravitational pull from bodies
    if test_object is not None:
        pos = test_object['pos']
        vel = test_object['vel']
        ax_total = np.array([0.0, 0.0])
        for body, (bx, by) in zip(bodies, positions):
            # Compute vector from test object to body
            disp = np.array([bx, by]) - pos
            r = np.linalg.norm(disp) + 1e-2  # avoid division by zero
            # Simple inverse-square acceleration
            a = G * body['mass'] / (r**2)
            # Add acceleration component in the direction of disp
            ax_total += a * disp/ r
        # Euler integration for velocity and position
        vel += ax_total * dt
        pos += vel * dt
        test_object['vel'] = vel
        test_object['pos'] = pos
        test_scatter.set_offsets(pos.reshape(1, -1))
    return scatter, warp_im, test_scatter

def on_click(event):
    global test_object
    # Only respond if click is inside the axes
    if event.inaxes != ax:
        return
    # On left-click, drop the test object at the click location if one doesn't exist
    if test_object is None:
        test_object = {
            'pos': np.array([event.xdata, event.ydata]),
            'vel': np.array([0.0, 0.0])
        }
    # On right-click, reset the test object
    elif event.button == 3:
        test_object = None
        test_scatter.set_offsets(np.empty((0, 2)))

# Connect the mouse click event
fig.canvas.mpl_connect('button_press_event', on_click)

# Create the animation
anim = FuncAnimation(fig, update, frames=600, interval=30, blit=False)

plt.show()