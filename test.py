from Constants import * 

import numpy as np
import time
import matplotlib.pyplot as plt

simulation_time = 86400 # s --> 1 year 
dt = 1 # s --> watch simulation per 1 second

x = np.linspace(0, 10, 100)
y = np.cos(x)

plt.ion() # Enable interactive mode

figure, ax = plt.subplots(figsize=(8,6))
line1, = ax.plot(x, y)

plt.title('Satellite Motion around the Earth')
plt.xlabel('x (Earth radii)')
plt.ylabel('y (Earth radii)')
plt.axis('equal')

circle = plt.Circle((0,0), R, facecolor='blue', edgecolor='black')

ax.add_artist(circle)

for time_slot in range(int(simulation_time / dt)):
    
    updated_y = np.cos(x-0.05*p)
    
    line1.set_xdata(x)
    line1.set_ydata(updated_y)
    
    figure.canvas.draw()
    
    figure.canvas.flush_events()
    time.sleep(0.1)