import matplotlib.pyplot as plt
import math
import numpy as np

v0 = np.random.randint(10, 30)
angles = np.arange(0, 90, 5)
g = 9.8
dt = 0.05

trajectories = []
# small angles create shorter trajectories
# tracking the longest one will prevent the cutting of the others
t_max = 0

for angle in angles:
    theta = math.radians(angle)
    vx0 = v0 * math.cos(theta)
    vy0 = v0 * math.sin(theta)
    
    x_vals, y_vals = [], []
    t = 0
    x = np.random.random() * 10
    while True:
        x = vx0 * t
        y = vy0 * t - 0.5 * g * t**2
        if y < 0: # check if the projectile goes underground
            break

        x_vals.append(x)
        y_vals.append(y)
        t += dt

    trajectories.append((x_vals, y_vals))
    t_max = max(t_max, len(x_vals))

plt.ion() # the plot will be updated before the plt.show call
fig, ax = plt.subplots()
ax.set_xlim(0, max(max(x) for x, _ in trajectories)*1.1)
ax.set_ylim(0, max(max(y) for _, y in trajectories)*1.1)
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title("Projectile Motion for Different Angles")

lines = [ax.plot([], [], lw=2)[0] for _ in angles]
points = [ax.plot([], [], 'o')[0] for _ in angles]

for step in range(t_max): # run till all the projectiles have landed
    for i, (x_vals, y_vals) in enumerate(trajectories):
        if step < len(x_vals): # avoid to updated a trajectory already landed
            lines[i].set_data(x_vals[:step], y_vals[:step])
            points[i].set_data([x_vals[step]], [y_vals[step]])
    plt.draw()
    plt.pause(dt)

plt.ioff()
plt.show()

