from solver import EdoSolver
import matplotlib.pyplot as plt
import sys
import functions

try:
    t = int(sys.argv[1])
    edo = EdoSolver(-0.5, 0.2, t)
except ValueError:
    edo = EdoSolver(-0.5, 0.2)
except IndexError:
    edo = EdoSolver(-0.5, 0.2)
gen = edo._solve_first_order(f)
harm = edo._solve_second_order(harmonic_oscillator)
plt.plot(harm[0], harm[1], color="blue", label= "Semi-Implicit euler Method")
plt.plot(gen[0], gen[1], color="red", label="Semi-Implicit Euler Method") 
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.grid()
plt.legend()
plt.show()
