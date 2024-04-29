import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(6,6), dpi=80)
cmap = plt.cm.bwr
cmap.set_bad('gray')


plt.cla()
matrix = np.genfromtxt('./output/uplot_data_0.301073.txt', delimiter=' ', filling_values=np.nan)
plt.imshow(matrix, cmap=cmap)
plt.clim(-3, 3)
ax = plt.gca()
ax.invert_yaxis()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)        
ax.set_aspect('equal')        
plt.pause(0.001)
plt.show()