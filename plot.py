import numpy as np
import matplotlib.pyplot as plt
import os

fig = plt.figure(figsize=(6,6), dpi=80)
cmap = plt.cm.bwr
cmap.set_bad('gray')

folder_path = 'serial/output'
entries = sorted(os.listdir(folder_path))

for filename in entries:
    file_path = os.path.join(folder_path, filename)
    plt.cla()
    matrix = np.genfromtxt(file_path, delimiter=' ', filling_values=np.nan)
    plt.imshow(matrix, cmap=cmap)
    plt.clim(-3, 3)
    ax = plt.gca()
    ax.invert_yaxis()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)        
    ax.set_aspect('equal')        
    plt.pause(0.001)
plt.show()

