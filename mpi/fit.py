import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# number of processes
sizes = np.array([2, 4, 8, 16, 32, 64, 128, 256]) 
# 10 execution times for each case 
times = np.array([[1.206496, 1.249228, 1.186479, 1.178838, 1.185821, 1.178749, 1.231941, 1.207286, 1.178388, 1.244971],
                  [0.696229, 0.704933, 0.692426, 0.678094, 0.678371, 0.654786, 0.694719, 0.701237, 0.747455, 0.682750],
                  [0.406984, 0.440676, 0.403153, 0.356672, 0.340014, 0.447963, 0.435164, 0.427108, 0.386391, 0.503272],
                  [0.296546, 0.350694, 0.393596, 0.348008, 0.321084, 0.368499, 0.359577, 0.397056, 0.296921, 0.315270],
                  [0.259065, 0.343517, 0.328899, 0.228369, 0.251328, 0.262712, 0.346113, 0.314659, 0.254058, 0.239217],
                  [0.283996, 0.273704, 0.324474, 0.269711, 0.297539, 0.341424, 0.301552, 0.284397, 0.314262, 0.301697],
                  [0.646985, 0.656064, 0.714164, 0.660563, 0.674421, 0.701120, 0.644161, 0.719139, 0.713670, 0.660456],
                  [4.198140, 4.377847, 4.349366, 4.428361, 4.353365, 4.343055, 4.326812, 4.408251, 4.231253, 4.336702]])

means = np.mean(times, axis=1)

def performance_model(p, a, b, c, d, e):
        with np.errstate(invalid='ignore', divide='ignore'):
                return a/(p+d) + b*(p+d)**c + e

params, params_covariance = curve_fit(performance_model, sizes, means)

plt.figure(figsize=(10, 7))
plt.plot(sizes, means, marker='o', linestyle='-', label='Measured Data')
plt.plot(sizes, performance_model(sizes, *params), color='red', label='Fitted function: a/(p+d) + b*(p+d)^c + e')
plt.xlabel('Number of Processes')
plt.ylabel('Execution Time (seconds)')
plt.title('Performance Modeling of Distributed Matrix Multiplication')
plt.xticks(sizes)
plt.legend()
plt.savefig('model.png')

print("Fitted parameters: a =", params[0], ", b =", params[1], ", c =", params[2], ", d =", params[3], ", e =", params[4])
