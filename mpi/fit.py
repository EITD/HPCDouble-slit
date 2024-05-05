import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

sizes = np.array([2, 4, 8, 16, 32, 64, 128, 256]) 

# [0.855233, 0.857655, 0.903995, 0.858751, 0.939731, 0.929982, 0.886140, 0.895321, 0.855924, 0.881856],
                #   [4.356557, 4.251764, 4.266816, 4.275980, 4.293016, 4.338333, 4.280883, 4.351467, 4.295181, 4.305166]
#                 [1.176524, 1.149516, 1.174430, 1.225668, 1.171996, 1.127724, 1.223919, 1.173755, 1.171542, 1.172521]
# [0.689314, 0.646258, 0.698834, 0.569037, 0.723095, 0.540439, 0.694611, 0.668536, 0.622521, 0.668473]
# [0.404791, 0.425242, 0.489234, 0.394461, 0.420023, 0.464104, 0.423230, 0.426055, 0.455935, 0.480139]
# [0.291018, 0.282722, 0.302218, 0.298662, 0.257225, 0.366549, 0.263186, 0.261281, 0.370914, 0.288185]
# [0.247440, 0.249273, 0.265482, 0.271454, 0.288656, 0.295179, 0.297942, 0.298404, 0.298436, 0.303153]
# [0.290323, 0.318308, 0.323674, 0.334242, 0.335570, 0.337492, 0.341316, 0.342214, 0.342690, 0.349356]
# [1.754447, 1.754077, 1.792931, 1.786865, 1.770696, 1.811642, 1.772769, 1.742173, 1.785157, 1.790668]

# [0.546520, 0.533232, 0.594535, 0.548988, 0.591874, 0.538340, 0.531097, 0.531877, 0.526508, 0.565221],
times = np.array([[1.206496, 1.249228, 1.186479, 1.178838, 1.185821, 1.178749, 1.231941, 1.207286, 1.178388, 1.244971],
                  [0.696229, 0.704933, 0.692426, 0.678094, 0.678371, 0.654786, 0.694719, 0.701237, 0.747455, 0.682750],
                  [0.406984, 0.440676, 0.403153, 0.356672, 0.340014, 0.447963, 0.435164, 0.427108, 0.386391, 0.503272],
                  [0.296546, 0.350694, 0.393596, 0.348008, 0.321084, 0.368499, 0.359577, 0.397056, 0.296921, 0.315270],
                  [0.259065, 0.343517, 0.328899, 0.228369, 0.251328, 0.262712, 0.346113, 0.314659, 0.254058, 0.239217],
                  [0.283996, 0.273704, 0.324474, 0.269711, 0.297539, 0.341424, 0.301552, 0.284397, 0.314262, 0.301697],
                  [0.646985, 0.656064, 0.714164, 0.660563, 0.674421, 0.701120, 0.644161, 0.719139, 0.713670, 0.660456],
                  [4.198140, 4.377847, 4.349366, 4.428361, 4.353365, 4.343055, 4.326812, 4.408251, 4.231253, 4.336702]])

means = np.mean(times, axis=1)
print(means)

def performance_model(p, a, b, c, d, e):
        return a/(p+d) + b*(p+d)**c + e

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