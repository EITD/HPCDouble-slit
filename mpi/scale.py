import matplotlib.pyplot as plt

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
