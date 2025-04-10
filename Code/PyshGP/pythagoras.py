import random
import numpy as np
import pandas as pd
from math import sqrt

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.instruction import SimpleInstruction

seed = 45

random.seed(seed)
np.random.seed(seed)



num_samples = 50
X = np.random.uniform(1, 10, (num_samples, 2))
y = np.array([[sqrt(x[0] ** 2 + x[1] ** 2)] for x in X])





iset = InstructionSet().register_core_by_stack({"float", "bool"})

if hasattr(iset, "_instructions"):
    
    iset._instructions = {name: inst for name, inst in iset._instructions.items() if name != "sqrt"}
    
    iset._instructions["sqrt"] = SimpleInstruction(
        name="sqrt",
        f=lambda x: (sqrt(x),),
        input_types=["float"],
        output_types=["float"],
        code_blocks=0,
        docstring="Computes the square root of a float."
    )




spawner = GeneSpawner(
    n_inputs=2,
    instruction_set=iset,
    literals=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
    erc_generators=[lambda: random.uniform(-10, 10)]
)




est = PushEstimator(
    spawner=spawner,
    population_size=300,
    max_generations=100,
    initial_genome_size=(10, 50),
    simplification_steps=2000,
    verbose=1,
    selector="elite"
)




print("Starting evolution to approximate the hypotenuse calculation...")
est.fit(X, y)

print("\nBest evolved program:")
print(est.solution.program.pretty_str())




test_X = np.array([
    [3.0, 4.0],
    [6.0, 8.0],
    [5.0, 12.0]
])
predictions = est.predict(test_X)


print("\nTest inputs (a, b):")
print(test_X)

print("\nReal hypotenuse values:")
real_values = [sqrt(x[0]**2 + x[1]**2) for x in test_X]
print(real_values)

print("\nPredicted hypotenuse values:")
print(predictions)





'''
Best evolved program:
(input_0 input_1 float_max 1.0 float_sin float_div)

sin(1) / max(input_1, input_0)

Test inputs (a, b):
[[ 3.  4.]
 [ 6.  8.]
 [ 5. 12.]]

Real hypotenuse values:
[5.0, 10.0, 13.0]

Predicted hypotenuse values:
[[4.753580423112485], [9.50716084622497], [14.260741269337455]]
'''



'''
Best evolved program:
(input_0 input_1 float_sub input_0 float_dec 2.0 float_div float_max input_1 float_add)  

max((input_1 - input_0), 2.0 / (input_0 - 1)) + input_1

Test inputs (a, b):
[[ 3.  4.]
 [ 6.  8.]
 [ 5. 12.]]

Real hypotenuse values:
[5.0, 10.0, 13.0]

Predicted hypotenuse values:
[[5.0], [10.5], [14.0]]
'''



'''
seed = 50

Best evolved program:
(4.0 input_1 float_max float_cos 3.0 float_sin float_tan float_tan float_add input_0 float_add input_1 float_max float_inc)

max(input_1, cos(max(input_1, 4.0)) + tan(tan(sin(3.0))) + input_0) + 1

Test inputs (a, b):
[[ 3.  4.]
 [ 6.  8.]
 [ 5. 12.]]

Real hypotenuse values:
[5.0, 10.0, 13.0]

Predicted hypotenuse values:
[[5.0], [9.0], [13.0]]
'''