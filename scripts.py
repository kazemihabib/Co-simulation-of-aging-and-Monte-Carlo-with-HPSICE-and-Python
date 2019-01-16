import numpy as np
runs = 10
mu, sigma = 0, 0.1 # mean and standard deviation
c = np.random.normal(mu, sigma, 10)
distibution_map = {"c": c}