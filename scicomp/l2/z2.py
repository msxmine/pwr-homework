import matplotlib.pyplot as plt
import numpy as np
import math

x = np.linspace(-50, 50, 100000)

y = [(math.e**elem)*(math.log(1+(math.e**(-elem)))) for elem in x]

plt.plot(x,y)
plt.show()
