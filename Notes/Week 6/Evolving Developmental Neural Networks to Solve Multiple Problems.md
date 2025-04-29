### Motivation
- Most ANNs use fixed architectures and encode knowledge via weights
	- This can lead to catastrophic forgetting
- Biological brains involve developmental processes
- The goal is to evolve developmental programs that can build, adapt, and grow neural networks
- Extract multiple ANNs from one evolved network that can each solve a different problem

### Key Innovation
- Developmental neural model where two evolving programs control the growth, movement, replication, and death, of neurons and their connections
	- Soma Program
		- Soma in a brain
			- Main cell body
			- Contains the nucleus and decides when to fire an action potential
		- In the soma program
			- Governs neuron health, bias, position, replication, and death
	- Dendrite Program
		- Dendrites in a brain
			- Branching structures extending from the soma
			- Receive signals from other neurons
		- In the dendrite program
			- Governs dendrite health, weight, extension, replication, and death
	- ![[Pasted image 20250429134018.png]]
- The neural network develops over time through interaction of these programs
- Conventional ANNs are extracted to solve problems

### Cartesian Genetic Programming
- A form of evolutionary algorithm where programs are represented as directed graphs
- The graph has:
	- Inputs: External data fed into the graph on the left side
	- Nodes: Perform operations on inputs or outputs from other nodes
	- Outputs: Selected from certain nodes
- ![[Pasted image 20250429133930.png]]

### Pre-Learning Development
- Start with a random initial network
	- Each problem has its own set of inputs and output neurons
- For ~6 steps, the soma and dendrite programs (governed by their respective CGPs) grow and change without feedback
- Neurons and dendrites move, change bias/weight, replicate, or die
- No evaluation yet, just free uncontrolled development, like early embryo growth

### Learning Development
- Now, the network will develop with feedback
- After each timestep, extract ANNs for each problem we are trying to solve
	- Do this by snapping each dendrite to its nearest neighbor to the left (including inputs)
	- This forces a feedforward structure with no loops
- Test the performance on each problem
- For the next step, our dendrites/soma programs adjust health, position, etc.
	- Pass position, health, weight, etc. of each soma/dendrite as inputs into the CGP network
	- Outputs new positions, healths, weights, etc.

### Evolution
- After a few epochs, evaluate each problem and find the fitness of the current soma/dendrite programs
- Use an evolutionary strategy to evolve the programs
	- Population of pairs of CGPs
	- Mutate, test, select, and repeat
- After evolution, you have two evolved programs (soma + dendrite) that can:
	- Grow a brain from scratch
	- Self-adapt during learning
	- Solve multiple unrelated problems by extracting networks at runtime

### Outcomes
- Model was tested on four tasks
- Two classification problems
	- Diabetes (binary)
	- Glass (multiclass)
- Reinforcement learning problems
	- Ball throwing
	- Double pole balancing
- High success rate for single problems: ~85%
- Incremental evolution improved performance with multiple tasks
- Brains could reuse neurons
- Only ~8 non-output neurons could handle multiple tasks