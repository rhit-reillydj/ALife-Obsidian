### A Neuromodulated Meta-Learning Algorithm (ANML)
- Neuromodulation-based system 
- Designed to solve continual learning and catastrophic forgetting in deep networks
- ![[Pasted image 20250427213340.png]]
- Instead of manually designing solutions to prevent forgetting, ANML learns to control when and where neurons activate and learn

### Architecture and Mechanisms
- Two neural networks
	- Prediction Learning Network (PLN)
		- Standard neural network that performs the primary task
	- Neuromodulatory Network (NM)
		- Secondary neural network that modulates activations in the PLN
		- Its output determines which neurons in the PLN activate and learn
- ![[Pasted image 20250427214430.png]]

### Mechanisms
- Neuromodulatory network modulates the forward pass of the PLN
	- Neuron activations in PLN are multiplied by the NM's outputs (some value between 0-1)
- Initial PLN weights and NM parameters are "meta-learned"

### Omniglot Dataset
- Sequentially present different characters from the Omniglot dataset
	- Some real alphabets, some fictional
- For each character, there is dozens of examples
- Characters are not labeled until error calculation
	- The NM network infers classes through training

### Inner Loop: Task Learning
- Train the PLN using the current NM
- NM stays frozen until this character is fully trained on
- First, pass inputs through NM to get neuromodulation gating signals
	- They supress/enhance parts of the PLN
- Do a forward pass and backward pass on the gated PLN
### Meta-Loss Calculation
- Test this PLN on
	- The newly learned class
	- Samples of previous tasks
- Meta-loss = New task loss + Old tasks memory loss
	- Encourages learning new and not forgetting old
### Outer Loop: Meta-Update
- Compute gradients of meta-loss and update
	- PLN initial weights
	- NM network parameters
### Meta-Testing
- Freeze the NM network
- Fine-tune prediction network on new tasks
- Evaluate

### Outcomes
- Compared to Online aware Meta-Learning (OML)
	- Previous state of the art meta-learning model for continuous learning
- After 600 classes:
	- ANML achieved ~64% accuracy
	- OML achieved ~18%
- After neuromodulation, only ~6% of PLN neurons are active
- ![[Pasted image 20250427214518.png]]