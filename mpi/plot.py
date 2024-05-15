import matplotlib.pyplot as plt
import numpy as np

# Data
threads = [2, 4, 8, 16, 32, 64, 128, 256]
exec_time = [1.2048197, 0.6931, 0.4147397, 0.3447251, 0.2827937, 0.2992756, 0.6790743, 4.3353152]
mpi_func = [32.6, 57.1, 60.5, 70.0, 72.1, 84.8, 95.4, 99.0]
algorithm_func = [59.7, 33.1, 31.1, 20.3, 14.8, 6.0, 0.8, 0.1]
imb_samp = [63.1, 70.1, 51.6, 49.7, 59.9, 78.2, 82.4, 89.8]

# Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

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
ax2.plot(threads, mpi_func, color='blue', label='MPI Func Samp Hits (%)', marker='s')
ax2.plot(threads, algorithm_func, color='green', label='Algorithm Func Samp Hits (%)', marker='^')
ax2.plot(threads, imb_samp, color='purple', label='Algorithm Func Imbalance Samp Hits (%)', marker='x')
ax2.tick_params(axis='y', labelcolor=color)

# Legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left', bbox_to_anchor=(1.05, 1))

# Show plot
plt.subplots_adjust(right=0.65)
plt.title('Performance Metrics by Number of Processes')
plt.xticks(threads, labels=threads)
plt.xscale('log', base=2) 
plt.grid(True)
plt.savefig('scale.png')

plt.show()