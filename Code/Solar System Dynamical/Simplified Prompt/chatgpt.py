from vpython import sphere, vector, color, rate, scene, pi, cos, sin
import math

# Set up the scene
scene.title = "3D Solar System Demo"
scene.width = 800
scene.height = 600
scene.background = color.black

# Create the Sun at the center.
sun = sphere(pos=vector(0, 0, 0), radius=0.5, color=color.yellow, emissive=True)

# Define planet parameters.
# The following list holds dictionaries for each planet.
# The properties are chosen to:
#   - give each planet a visually distinct orbit
#   - scale the sizes so planets are visible relative to one another
#   - assign an angular speed (in radians per second) for a full orbit
#     (these speeds are not physically accurate—they’re set for visual interest)

planets_data = [
    {"name": "Mercury", "radius": 0.1, "color": color.gray(0.5), "orbit_radius": 1.0, "angular_speed": 2 * pi / 8},
    {"name": "Venus",   "radius": 0.15, "color": color.orange, "orbit_radius": 1.5, "angular_speed": 2 * pi / 12},
    {"name": "Earth",   "radius": 0.15, "color": color.blue,   "orbit_radius": 2.0, "angular_speed": 2 * pi / 16},
    {"name": "Mars",    "radius": 0.12, "color": color.red,    "orbit_radius": 2.5, "angular_speed": 2 * pi / 20},
    {"name": "Jupiter", "radius": 0.3,  "color": color.orange, "orbit_radius": 3.5, "angular_speed": 2 * pi / 30},
    {"name": "Saturn",  "radius": 0.25, "color": color.yellow, "orbit_radius": 4.5, "angular_speed": 2 * pi / 36},
    {"name": "Uranus",  "radius": 0.2,  "color": color.cyan,   "orbit_radius": 5.5, "angular_speed": 2 * pi / 42},
    {"name": "Neptune", "radius": 0.2,  "color": color.blue,   "orbit_radius": 6.5, "angular_speed": 2 * pi / 48},
]

# Create a list to hold the planet objects.
planets = []

# For each planet, create its sphere with a trail (to show the orbit)
for pdata in planets_data:
    # Start the planet at its orbit radius on the x-axis.
    planet = sphere(pos=vector(pdata["orbit_radius"], 0, 0),
                    radius=pdata["radius"],
                    color=pdata["color"],
                    make_trail=True,       # This shows the path (orbit) 
                    retain=150)            # Length of the trail to display.
    # Attach extra properties to update positions later.
    planet.orbit_radius = pdata["orbit_radius"]
    planet.angular_speed = pdata["angular_speed"]
    planet.theta = 0  # initial angle (in radians)
    planets.append(planet)

# Animation loop
# This infinite loop updates each planet's position.
while True:
    rate(100)  # Limits the number of iterations per second (animation smoothness)
    dt = 0.01  # Time step for each iteration
    for planet in planets:
        # Update the angular position (theta) based on the angular speed.
        planet.theta += planet.angular_speed * dt
        
        # Compute new x and y (keeping z = 0 so orbits are planar).
        x = planet.orbit_radius * math.cos(planet.theta)
        y = planet.orbit_radius * math.sin(planet.theta)
        planet.pos = vector(x, y, 0)