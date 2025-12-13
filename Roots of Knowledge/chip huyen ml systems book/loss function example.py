import numpy as np

def cross_entropy(p, q):
    return -sum([p[i] * np.log(q[i]) for i in range(len(p))])

p, q = [0, 0, 0, 1], [.33, .2, .02, .45]
print(cross_entropy(p, q))