import numpy as np

def harmonic_oscillator(x: float) -> float:
    k = m = 1
    return -(k/m)*x

def sinx(x: float) -> float:
    return np.sin(x)

def pendulum(x: float, g: float = 9.8, l: float = 1) -> tuple[float, str]:
    return -(g/l)*np.sin(x), "-(g/l) * sin(x)"

def f(t: float, y: float) -> float:
    return t**3 * np.sqrt(4 - y**2)
