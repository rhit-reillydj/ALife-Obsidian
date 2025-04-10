X = [[random.randint(1, 30), random.randint(1, 30)] for _ in range(training_size)]
y = [pythagorean_theorem(x) for x in X]