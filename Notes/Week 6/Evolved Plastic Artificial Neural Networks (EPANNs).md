### Main Concept
- EPANNs combine plastic (adaptive) artificial neural networks with evolutionary algorithms
- They evolve weights, learning rules, plasticity mechanisms, and adaptation strategies
- Learning through evolution and plasticity
	- Evolution shapes the networks between generations
	- Plasticity allows a network to adapt and learn during their lifetime
	- Both processes work together and accelerate each other (learning can guide evolution)
- ![[Pasted image 20250427215354.png]]

### What Are We Evolving?
- Evolving Plasticity Rules
	- Early work developed parameters of known rules (Hebbian learning)
	- Later work evolved entirely new learning rules
- Evolving Learning Architectures
	- Evolution discovers weights, network topologies, plastic connection layouts (some weights are fixed), and modular architectures (organized into specialized regions)
- ![[Pasted image 20250427215422.png]]
### Discovery of Learning Mechanisms
- Initially, static strategies dominate
	- No weights
- Learning mechanisms (plasticity) will suddenly arise and dominate once discovered
- ![[Pasted image 20250427215139.png]]
### Neuron Weights
- Neuromodulatory signals can evolve to enable *conditional* learning
- Some neurons may evolve to produce a dopamine-like signal that strengthens certain synapses
- Instead of evolving every weight separately, indirect encodings (HyperNEAT) are evolved that generate large-scale networks

### Evolutionary Algorithm
- Variable genotype length (allows for growing complexity)
- Indirect encoding (compact with scalable genotype-phenotype mappings)
- Effective mutation and recombination
- Genetic encoding of plasticity rules (how neuron weights change)
- Maintain diversity
- Low selection pressure allows for creative solutions
- Algorithms like NEAT and HyperNEAT are good examples