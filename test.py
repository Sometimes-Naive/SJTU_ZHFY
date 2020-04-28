import numpy as np
import matplotlib.pyplot as plt

x = list(range(100))
y = np.sin(x)
plt.figure()
plt.plot(x, y)
plt.show()