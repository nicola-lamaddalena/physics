import sys
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np

def harmonic_oscillator(x: float, k: float = 1, m: float = 1) -> float:
    return -(k/m)*x

def sinx(x: float) -> float:
    return np.sin(x)

def pendulum(x: float, g: float = 9.8, l: float = 1) -> float:
    return -(g/l)*np.sin(x)

class EdoSolver:
    def __init__(self, x0: float, v0: float, delta: float, t: float = 100):
        self.x0 = x0
        self.v0 = v0
        self.delta = delta
        self.t = t

    def explicit_euler(self, f: Callable) -> list[float]:
        """
        """
        t0 = 0 # time interval for the simulation
        x, v = self.x0, self.v0
        pos = [x]

        while t0 < self.t:
            a = f(x)
            x += v * self.delta
            v += a * self.delta
            pos.append(x)
            t0 += self.delta

        return pos

    def semi_implicit_euler(self, f: Callable) -> list[float]:
        """
        """
        t0 = 0 # time interval of the simulation
        x, v = self.x0, self.v0
        pos = [x]

        while t0 < self.t:
            v += f(x) * self.delta
            x += v * self.delta
            pos.append(x)
            t0 += self.delta

        return pos

try:
    t = int(sys.argv[1])
    edo = EdoSolver(-0.5, 0.2, 0.01, t)
except ValueError:
    edo = EdoSolver(-0.5, 0.2, 0.01)
pos_implicit = edo.semi_implicit_euler(pendulum)
pos_explicit = edo.explicit_euler(pendulum)
time = [i * edo.delta for i in range(len(pos_implicit))]
plt.plot(time, pos_explicit, color="red", label="Explicit Euler Method")
plt.plot(time, pos_implicit, color="blue", label= "Semi-Implicit euler Method")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.grid()
plt.legend()
plt.show()
