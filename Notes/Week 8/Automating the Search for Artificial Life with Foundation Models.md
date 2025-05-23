https://pub.sakana.ai/asal_blog_assets/cover_video_square_small_compressed.mp4
### Background
- ALife explores "life as it could be"
- Traditionally relies on human intuition and laborious trial-and-error
- How to automate this?
	- Option 1: Mathematically define interestingness, open-endedness, emergence
	- **Option 2: Ask a foundation model**
- We can utilize vision-based foundation models (FMs) to automate this process

### Automated Search for Artificial Life (ASAL) Framework
- Use vision-language FMs to score rendered videos of simulation
- Three search methods
	- Supervised target: Attempt to align with a user-specified text prompt
	- Open-endedness: Identify simulations with trajectories that continually produce novel imagery
	- Illumination: Illuminates diversity by finding a set of simulations with final states that are maximally distant from each other
	- ![[Pasted image 20250512230137.png]]
- Enables quantitative analysis
	- Particle life caterpillar requires > 1000 particles

### ALife Substrates
- Life-Like Cellular Automata
	- https://pub.sakana.ai/asal_blog_assets/oe_gol_1.mp4
- Neural Cellular Automata
	- ![[Pasted image 20250512230225.png]]
- Lenia
- Boids
- Particle Life
	- https://pub.sakana.ai/asal_blog_assets/supervised_3x6_compressed.mp4

### Contributions & Impact
- Automate the search for ALife
- Applicable for automating search in many domains
- Provide quantitative information for interpreting and fine-tuning simulations