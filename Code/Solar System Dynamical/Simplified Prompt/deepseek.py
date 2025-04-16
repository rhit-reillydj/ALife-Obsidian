import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Planetary data (scaled for visualization)
planets_data = [
    {'name': 'Mercury', 'distance': 0.39, 'size': 0.38, 'period': 0.24, 'color': 'gray'},
    {'name': 'Venus',   'distance': 0.72, 'size': 0.95, 'period': 0.62, 'color': 'orange'},
    {'name': 'Earth',   'distance': 1.00, 'size': 1.00, 'period': 1.00, 'color': 'blue'},
    {'name': 'Mars',    'distance': 1.52, 'size': 0.53, 'period': 1.88, 'color': 'red'},
    {'name': 'Jupiter', 'distance': 5.20, 'size': 11.2, 'period': 11.86, 'color': 'brown'},
    {'name': 'Saturn',  'distance': 9.58, 'size': 9.45, 'period': 29.46, 'color': 'gold'},
    {'name': 'Uranus',  'distance': 19.2, 'size': 4.01, 'period': 84.01, 'color': 'lightblue'},
    {'name': 'Neptune', 'distance': 30.1, 'size': 3.88, 'period': 164.8, 'color': 'darkblue'}
]

# Scaling factors
distance_scale = 0.08  # Scale down orbital distances
size_scale = 0.8       # Scale up planet sizes for visibility

# Apply scaling and add inclination angles
for planet in planets_data:
    planet['distance'] *= distance_scale
    planet['size'] = planet['size']**0.5 * size_scale  # Soften size differences
    planet['inclination'] = np.radians(np.random.uniform(-10, 10))  # Random orbital tilt

# Setup figure and 3D axis
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.grid(False)
ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False

# Set plot boundaries
max_dist = max(p['distance'] for p in planets_data) * 1.2
ax.set_xlim(-max_dist, max_dist)
ax.set_ylim(-max_dist, max_dist)
ax.set_zlim(-max_dist, max_dist)

# Create Sun
ax.scatter([0], [0], [0], s=500, color='yellow', alpha=0.8)

# Initialize planets and orbits
planets = []
orbits = []

for p in planets_data:
    # Planet markers
    planet = ax.plot([], [], [], 'o', markersize=p['size'], 
                    color=p['color'], markeredgecolor='white')[0]
    planets.append(planet)
    
    # Orbit paths
    orbit = ax.plot([], [], [], color=p['color'], alpha=0.4, linewidth=0.7)[0]
    orbits.append(orbit)

# Animation function
def update(frame):
    time = frame * 0.02  # Time step (years per frame)
    
    for i, p in enumerate(planets_data):
        # Calculate orbital position
        theta = 2 * np.pi * time / p['period']
        x = p['distance'] * np.cos(theta)
        y = p['distance'] * np.sin(theta) * np.cos(p['inclination'])
        z = p['distance'] * np.sin(theta) * np.sin(p['inclination'])
        
        # Update planet position
        planets[i].set_data([x], [y])
        planets[i].set_3d_properties([z])
        
        # Update orbit path
        orbits[i].set_data(
            np.append(orbits[i].get_xdata(), x),
            np.append(orbits[i].get_ydata(), y)
        )
        orbits[i].set_3d_properties(
            np.append(orbits[i].get_3d_properties(), z)
        )
    
    return planets + orbits

# Create animation
ani = animation.FuncAnimation(
    fig, update, frames=500, interval=20, blit=True, repeat=True
)

# Add legend and title
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=p['name'],
                   markerfacecolor=p['color'], markersize=8) for p in planets_data]
ax.legend(handles=legend_elements, loc='upper left', fontsize=8)

plt.title('3D Solar System Animation', color='white', fontsize=14)
plt.show()