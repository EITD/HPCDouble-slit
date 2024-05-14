import matplotlib.pyplot as plt
import numpy as np

# Data
threads = [1, 2, 4, 8, 16, 32, 64, 128, 256]
exec_time = [1.77119931, 1.60838459, 0.88118148, 0.53694686, 0.37435735, 0.32451078, 0.29646319, 0.32650735, 0.63228685]
cpu_usage = [99.78, 99.65, 99.17, 98.35, 97.35, 96.53, 95.52, 93.53, 88.65]
frontend_idle = [0.01, 0.063, 0.082, 0.074, 0.08, 0.133, 0.085, 0.088, 0.451]
backend_idle = [77.15, 86.66, 87.84, 90.00, 92.67, 94.78, 95.85, 97.62, 5.57]
ipc = [[1.78, 1.77, 1.78, 1.77, 1.77, 1.78, 1.77, 1.78, 1.77, 1.77],
       [0.98, 0.98, 0.98, 0.97, 1.02, 1.02, 0.98, 0.98, 0.98, 1.03],
       [0.92, 0.91, 0.93, 0.92, 0.92, 0.92, 0.92, 0.92, 0.92, 0.92],
       [0.77, 0.77, 0.77, 0.77, 0.78, 0.77, 0.77, 0.77, 0.78, 0.77],
       [0.60, 0.60, 0.60, 0.60, 0.60, 0.59, 0.59, 0.59, 0.59, 0.60],
       [0.41, 0.39, 0.40, 0.39, 0.41, 0.40, 0.41, 0.39, 0.40, 0.40],
       [0.25, 0.25, 0.27, 0.24, 0.26, 0.26, 0.25, 0.27, 0.26, 0.25],
       [0.16, 0.16, 0.17, 0.16, 0.16, 0.16, 0.15, 0.15, 0.16, 0.16],
       [0.18, 0.19, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18]]

means = np.mean(ipc, axis=1)
print(means)

exit()

# Plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# First axis (left y-axis)
color = 'tab:red'
ax1.set_xlabel('Threads')
ax1.set_ylabel('Execution Time (s)', color=color)
ax1.plot(threads, exec_time, color=color, label='Execution Time (s)', marker='o')
ax1.tick_params(axis='y', labelcolor=color)

# Second axis (right y-axis)
ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Percentage (%)', color=color)
ax2.plot(threads, cpu_usage, color='blue', label='CPU Usage (%)', marker='s')
ax2.plot(threads, frontend_idle, color='green', label='Frontend Idle (%)', marker='^')
ax2.plot(threads, backend_idle, color='purple', label='Backend Idle (%)', marker='x')
ax2.tick_params(axis='y', labelcolor=color)

# Legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left', bbox_to_anchor=(1.05, 1))

# Show plot
plt.subplots_adjust(right=0.75)
plt.title('Performance Metrics by Number of Threads')
plt.xticks(threads, labels=threads)
plt.xscale('log', base=2) 
plt.grid(True)
plt.savefig('scale.png')
plt.show()