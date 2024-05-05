import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

sizes = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256]) 


times = np.array([[0.855233, 0.857655, 0.903995, 0.858751, 0.939731, 0.929982, 0.886140, 0.895321, 0.855924, 0.881856],
                  [1.176524, 1.149516, 1.174430, 1.225668, 1.171996, 1.127724, 1.223919, 1.173755, 1.171542, 1.172521],
                  [0.689314, 0.646258, 0.698834, 0.569037, 0.723095, 0.540439, 0.694611, 0.668536, 0.622521, 0.668473],
                  [0.404791, 0.425242, 0.489234, 0.394461, 0.420023, 0.464104, 0.423230, 0.426055, 0.455935, 0.480139],
                  [0.291018, 0.282722, 0.302218, 0.298662, 0.257225, 0.366549, 0.263186, 0.261281, 0.370914, 0.288185],
                  [0.331694, 0.292552, 0.230698, 0.243015, 0.310713, 0.322971, 0.276226, 0.252928, 0.309957, 0.333583],
                  [0.315389, 0.358768, 0.332182, 0.259272, 0.328407, 0.338051, 0.317154, 0.300339, 0.304252, 0.280079],
                  [1.754447, 1.754077, 1.792931, 1.786865, 1.770696, 1.811642, 1.772769, 1.742173, 1.785157, 1.790668],
                  [4.356557, 4.251764, 4.266816, 4.275980, 4.293016, 4.338333, 4.280883, 4.351467, 4.295181, 4.305166]])

means = np.mean(times, axis=1)

def performance_model(p, a, b, c):
        return a/p + b*p**c

params, params_covariance = curve_fit(performance_model, sizes, means)

plt.figure(figsize=(10, 7))
plt.plot(sizes, means, marker='o', linestyle='-', label='Measured Data')
plt.plot(sizes, performance_model(sizes, *params), color='red', label='Fitted function: a/p + b*p^c')
plt.xlabel('Number of Processes')
plt.ylabel('Execution Time (seconds)')
plt.title('Performance Modeling of Distributed Matrix Multiplication')
plt.xticks(sizes)
plt.legend()
plt.savefig('model.png')

print("Fitted parameters: a =", params[0], ", b =", params[1], ", c =", params[2])
