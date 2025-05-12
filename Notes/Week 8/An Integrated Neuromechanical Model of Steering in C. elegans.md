1. **What they wanted to do**  

    They built a simple “brain” that can steer a virtual worm toward higher concentrations of a chemical (like food scent) on a 2D surface. The goal was to see if a tiny neural circuit, placed just at the front of the worm, is enough to steer its whole body reliably .
    
2. **How the worm is modeled**
    
    - **Body mechanics**: The worm is split into many small linked segments (like a snake made of springy rods), so it undulates naturally when its “muscles” pull on these joints.
        
    - **Muscles**: Each segment has muscles on its top and bottom that can contract or relax, turning neural signals into bending motions.
        
3. **The “brain” (neural circuit)**
    
    - **Forward-motion controller**: A repeating chain of basic units drives the undulating movement: each unit senses stretch in the body and triggers the next one, creating a traveling wave that propels the worm forward.
        
    - **Steering circuit**: A tiny four-neuron network sits at the front (“neck”) and responds to changes in the chemical level. It watches whether the scent is increasing or decreasing, and at which point in the undulation cycle it happens. Depending on that, it nudges the front muscles to turn left or right.
        
4. **Tuning by evolution**  
    Because we don’t know exactly how strong each connection should be, they used an evolutionary algorithm to “evolve” the best weights and timing parameters:
    
    - They ran many simulated worms, each with different random neural-connection values.
        
    - They scored each one by how directly it steered up the gradient in short test runs.
        
    - Over hundreds of generations, the population “bred” better steerers.
        
5. **Key findings**
    
    - **Minimal is enough**: Just steering the first few neck muscles (not the whole body) was sufficient for robust, reliable turns.
        
    - **Phase matters**: If the chemical level rises when the worm’s head is swinging right, it turns right; if it rises while swinging left, it turns left. This matches real‐worm data.
        
    - **Generalizes**: The evolved controller worked across different gradient shapes and strengths, not just the one used during evolution.
        
6. **Why it matters**
    
    - Shows how a very small, anatomically grounded neural network can produce a complex, adaptive behavior in an embodied agent.
        
    - Bridges ideas from artificial‐life evolutions-of-behavior, neural‐network control, and biomechanics in one integrated model.
        
    - Predicts specific “turning modes” (patterns of body shape change) that real worms could be tested for in future experiments .
        

In short: by combining a realistic spring-and-joint body, simple muscle models, and a tiny neural circuit tuned by evolution, they demonstrated that minimal neural “brains” can steer an embodied agent toward goals in a robust, phase-dependent way.