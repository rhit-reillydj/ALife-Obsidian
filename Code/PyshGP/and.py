import random
import numpy as np

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.type_library import PushTypeLibrary

training_size = 30
testing_size = 50

random.seed(42)
np.random.seed(42)

    

def and_gate(input1, input2):
    return 1 if input1 and input2 else 0
    
    
    
    
X = [[random.randint(0,1), random.randint(0,1)] for _ in range(training_size)]
y = [[and_gate(input1, input2)] for input1, input2 in X]

test_X = [[random.randint(0,1), random.randint(0,1)] for _ in range(testing_size)]
test_y = [[and_gate(input1, input2)] for input1, input2 in test_X]





spawner = GeneSpawner(
    n_inputs=2,
    instruction_set="core",
    literals=[0,1],
    erc_generators=[lambda: random.randint(0, 1)]
)


if __name__ == "__main__":
    est = PushEstimator(
        spawner=spawner,
        max_generations=20,
        population_size=300,
        verbose=2
    )
    
    
    est.fit(X=X, y=y)
    print()
    
    
    print("Best program found:")
    print(est.solution.program.pretty_str())

    print("Test errors:")
    scores = est.score(test_X, test_y)
    print(scores)
    print(sum(scores) / len(scores))
    
    
    
'''
Best Seen Individual
    Genome:
        pvector([Input(input_index=0), Literal(value=0, push_type=<pyshgp.push.types.PushIntType object at 0x0000018FFFD06E70>), Input(input_index=1), InstructionMeta(name='int_yank', code_blocks=0)])
        
    Program:
        (input_0 0 input_1 int_yank)
       
    Error vector:
        [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
 0. 0. 0. 0. 0. 0.]
 
    Total error:
        0.0
'''