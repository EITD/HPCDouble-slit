import matplotlib.pyplot as plt

# 128
# 0.072517
# 0.085885
# 0.072686
# 0.077344
# 0.076618
# 0.080899
# 0.073543
# 0.076136
# 0.074420
# 0.079730

# 64
# 0.010302
# 0.009208
# 0.009689
# 0.009708
# 0.009842
# 0.009546
# 0.009968
# 0.011271
# 0.009648
# 0.009939

events_per_process = ["256/256", "128/64", "64/16"]
times = [4.3353152, 0.076978, 0.009912]

plt.figure(figsize=(10, 7))
plt.plot(events_per_process, times, marker='o', linestyle='-')

# Adding titles and labels
plt.title('Scaling Results of Distributed Matrix Multiplication')
plt.xlabel('Events per Process')
plt.ylabel('Execution Time (seconds)')
plt.xticks(events_per_process)
plt.savefig('scale.png')
