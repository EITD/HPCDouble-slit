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


def calculate_speedup_and_efficiency_S(Ts, Tp):
        speedups = [Ts / t for t in Tp]
        efficiencies = []
        for i, speedup in enumerate(speedups):
                efficiencies.append(speedup / (2 ** (i+1)))
        return speedups, efficiencies

def calculate_speedup_and_efficiency_W(Ts, Tp):
        speedups = [s / p for s,p in zip(Ts,Tp)]
        efficiencies = []
        a = [256, 64, 16]
        for i, speedup in enumerate(speedups):
                efficiencies.append(speedup / a[i])
        return speedups, efficiencies

TsS = 0.948367014
TpS = [1.2048197, 0.6931, 0.4147397, 0.3447251, 0.2827937, 0.2992756, 0.6790743, 4.3353152]

speedups_S, efficiencies_S = calculate_speedup_and_efficiency_S(TsS, TpS)

ideal_speedups_S = [2 ** i for i in range(1, len(TpS) + 1)]

print("Results for TpS (same problem size and increasing number of processes):")
for i, (speedup, efficiency, ideal_speedup) in enumerate(zip(speedups_S, efficiencies_S, ideal_speedups_S), start=1):
        print(f"Processes: {2**i}, Speed-Up: {speedup:.3f}, Ideal Speed-Up: {ideal_speedup}, Efficiency: {efficiency:.3f}")

TsW = [0.948367014, 0.114787009, 0.022162241]
TpW = [4.3353152, 0.076978, 0.009912]

speedups_W, efficiencies_W = calculate_speedup_and_efficiency_W(TsW, TpW)

ideal_speedups_W = [2 ** i for i in range(1, len(TpW) + 1)]

print("\nResults for TpW (weak scaling):")
a = [256, 64, 16]
for i, (speedup, efficiency, ideal_speedup) in enumerate(zip(speedups_W, efficiencies_W, ideal_speedups_W), start=0):
        print(f"Processes: {a[i]}, Speed-Up: {speedup:.3f}, Ideal Speed-Up: {a[i]}, Efficiency: {efficiency:.3f}")
