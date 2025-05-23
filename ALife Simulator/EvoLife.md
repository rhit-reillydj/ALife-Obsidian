### What is EvoLife?
- Early access game on steam
- Simulates the boundary between single-celled and multicellular organisms in a sandbox environment
- Generate world of various sizes, tweak simulation constants
- Observe how simple mutation rules and environmental pressures drive species differentiation over time

### What does it do?
- Build or auto-generate 2D landscapes
- Place and edit cells, rocks, fluids, scents, and more
- Edit cells DNA and species' genomes
- Evolution mode for random mutation
	- See how populations adapt, diversify, or perish
- Watch cells compete for resources and even develop primitive organisms

### How does it do it?
- Three intertwined simulations running at once
- Physics engine
	- Handles objects (cells, particles, biomaterials, rocks)
	- Supports joints and can simulate hundreds of thousands of bodies in real time
- Fluid Dynamics
	- Grid-based fluid solver carries physics bodies and up to 8 distinct smells
	- Cells can excrete or detect these smells for pheromone-style communication
- Game Logic
	- Handles cell chemisty via 26 biomaterials, each with custom weight, stickiness, brittleness, and energy value
	- Oversees cell growth, DNA execution, division, mutation, and long-term species evolution

### World Objects
- Rocks
	- Static or dynamic with varying weights
- Gas Bubbles
	- Spawned by deep-sea vents; contain energy for cells to harvest
- Dead cells
	- When a cell dies it becomes a particle carrying its leftover energy
- Biomaterials
	- Produced or broken down by cells. Each sticks to specific objects and has an energy yield

### Cell Internals
- 16 behavior slots per cell, each dictating behavior
- Has an opcode, inputs, and an output
	- No-op, math, sequence, organal, egg, fission, jump, and, die, vit
	- DNA pieces act like subroutines
- Each instruction costs time and energy, so complex cells take longer to "think"

### Organelles
- > 65,000 organelles available
- Development cost/time, usage energy, and up to 2 inputs + 1 output
- Categories:
	- **Structural:** spikes (damage), cell wall, size, color
	- **Motion:** flagellum (propel in a direction), flex (change radius)
	- **Metabolic:** heal, breakdown biomaterials, siphon energy from others
	- **Sensing:** fluid direction, smell ID, touch, damage, color sampling, cell-count in radius
	- **Communication:** produce smell, transfer data/energy between cells
	- **Connection:** stick (adhesion), muscle (contractile joint), transfer (share energy/info)

### Evolution & Species Dynamics
- At the start, there is a handful of random species (5 cells each) on top of an energy field
- Mutations occur on each reproduction
- When a species reaches 50 live cells, it breeds a new mutated variant
- This leads to evolutionary dynamics