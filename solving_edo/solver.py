"""
Object implementation of a ODE solver.
"""
from typing import Callable
import inspect


class EdoSolver:
    """
    Args:
    - x0: initial position (float)
    - v0: initial velocity (float | None) - initialized as None because 
    it is unused in the second order solver
    - t: time of the simulation (float) - initialized as 10
    """

    def __init__(self, x0: float, v0: float | None = None, t: float = 10):
        self.x0 = x0
        self.v0 = v0
        self.delta = min(0.001, t/1000)
        self.t = t


    def solve(self, function: Callable):
        """
        Function designed to switch between first and second order ode 
        based on the number of parameters that the function has.
        """
        sig = inspect.signature(function)
        params = len(sig.parameters)

        if params == 1:
            return self._solve_second_order(function)
        if params == 2:
            return self._solve_first_order(function)
        raise ValueError(f"{params} parameters given: not implemented")

    def explicit_euler(self, f: Callable) -> list[float]:
        """
        [UNUSED]
        Simplest Euler method to solve ode. It's highly unstable for long 
        simulation time.
        It's currently unused: implemented only for learning purpose.
        """
        t0 = 0 # time interval for the simulation
        x = self.x0
        v = self.v0 if self.v0 is not None else 0.0
        pos = [x]

        while t0 < self.t:
            a = f(x)
            x += v * self.delta
            v += a * self.delta
            pos.append(x)
            t0 += self.delta

        return pos


    def _solve_second_order(self, f: Callable) -> tuple[list[float], list[float]]:
        """
        Semi-Implicit Euler method. Called only when the input function 
        accepts a single parameter. More stable than the explicit Euler 
        method and simple enough to implement.
        """
        t0, x, v = 0.0, self.x0, self.v0
        times, pos = [t0], [x]

        while t0 < self.t:
            v += f(x) * self.delta
            x += v * self.delta
            t0 += self.delta
            times.append(t0)
            pos.append(x)

        return times, pos

    def _solve_first_order(self, f: Callable):
        t, y = 0.0 , self.x0
        times, sol = [t], [y]
        while t < self.t:
            y += f(t, y) * self.delta
            t += self.delta
            times.append(t)
            sol.append(y)

        return times, sol
