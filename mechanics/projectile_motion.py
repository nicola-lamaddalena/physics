import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random, math

angles = [theta for theta in range(90) if theta % 15 == 0]
v0 = random.randint(10, 30)
dt = 0.001

def motion(x0: float, y0: float, vx0: int | float, vy0: int | float, t: float):
    xs = []
    ys = []
    ax, ay = 0, -9.8
    t0 = 0
    while t0 < t:
        x = x0 + vx0 * t0 + 0.5 * ax * t0**2
        y = y0 + vy0 * t0 + 0.5 * ay * t0**2
        if y < 0:
            break
        xs.append(x)
        ys.append(y)
        t0 += dt

    return xs, ys

colors = ["black", "red", "blue", "yellow", "green", "orange"]

for i, angle in enumerate(angles):
    vx = v0 * math.cos(math.radians(angle))
    vy = v0 * math.sin(math.radians(angle))
    x_vals, y_vals = motion(0, 0, vx, vy, 10)
    plt.plot(x_vals, y_vals, color=colors[i])
    plt.pause(0.1)

plt.show()
