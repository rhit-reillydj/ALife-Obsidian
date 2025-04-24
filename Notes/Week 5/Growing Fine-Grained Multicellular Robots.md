### MapDevo3D
- Self-Assembly
	- Cells are spheres that can attract or repel other cells
	- Each cell has self-assembly genes to specific division rate, attractions, range, etc.
- Pattern Information
	- Gene Regulatory Networks in each cell take nearby gradients as inputs
		- Output a cells identity
	- Differentiate cells into different varieties (body vs limb)
- Recursive Gene Regulation
	- Each region of same-identity cells can trigger its own GRN
	- These cells now adjust their division rates and adhesion to divide into subdomains (muscle vs bone)
### Functionality
- After development, the organism is placed in a virtual world with gravity, collision, drag, etc.
- There is no local controller to control the body
	- Behaves through local rules on a schedule
	- Muscles contract and stretch according to some simple signal pattern
- Could be combined with evolutionary search for full evo-devo
- Could add a neural network controller for more efficient bodily control