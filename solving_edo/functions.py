import numpy as np

def harmonic_oscillator(x: float, k: float = 1, m: float = 1) -> float:
    return -(k/m)*x

def sinx(x: float) -> float:
    return np.sin(x)

def pendulum(x: float, g: float = 9.8, l: float = 1) -> float:
    return -(g/l)*np.sin(x)

def f(t: float, y: float) -> float:
    return t**3 * np.sqrt(4 - y**2)
