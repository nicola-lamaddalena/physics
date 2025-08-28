import sys
import functions
import matplotlib.pyplot as plt
from solver import EdoSolver

def main():
    try:
        t = int(sys.argv[1])
        edo = EdoSolver(-0.5, 0.9, t)
    except ValueError:
        edo = EdoSolver(-0.5, 0.2)
    except IndexError:
        edo = EdoSolver(-0.5, 0.2)

    e1 = edo.solve(functions.harmonic_oscillator)
    plt.plot(e1[0], e1[1], color="blue", label= "Harmonic oscillator with semi-implicit Euler method")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
