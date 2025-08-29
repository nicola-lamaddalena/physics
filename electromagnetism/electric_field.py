#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
electric_field.py

A Python script to visualize the electric field of a dipole using matplotlib.
The script plots vectors of uniform length, with their color representing the
true magnitude of the field.
"""

import sys
import matplotlib.pyplot as plt
import numpy as np

# Constants
POINTS = 31
EPSILON_ZERO = 8.85e-12
CHARGE_VALUE = 10e-10
DEFAULT_C_MAP = "inferno"





def electric_field(
    x: np.ndarray, y: np.ndarray, qx: float, qy: float, q: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the electric field at grid points (x,y) due to a charge point at (qx,qy) 
    with charge value q.
    E := q / (4 * pi * epsilon_0 * r**2)

    Args:
        x, y: Meshgrid arrays representing the grid points.
        qx, qy: Coordinates of the point charge.
        q: The value of the charge value in Coulombs.
    
    Returns:
        A tuple containing the Ex and Ey components of the electric field.
    """
    r = np.sqrt((x - qx) ** 2 + (y - qy) ** 2)
    theta = np.arctan2(y - qy, x - qx)

    # If r == 0 => E = \infty, so we put E=0 if r == 0
    e_field = np.where(r == 0, 0, q / (4 * np.pi * EPSILON_ZERO * r**2))
    E_x = e_field * np.cos(theta)
    E_y = e_field * np.sin(theta)
    return E_x, E_y


def filter_values(x: np.ndarray, y: np.ndarray, u: np.ndarray, v: np.ndarray, charges_coords: list[tuple[float, float]], r_min: float = 0.1) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Filters grid points to avoid singularities near point charges.

    Args:
        x, y: Meshgrid arrays representing the grid points
        u, v: The electric field components.
        charges_coords: A list of (qx,qy) tuples for each point charge.
        r_min: The minimum radius of exclusion around each charge.

    Returns:
        A tuple with the filtered values of x, y, u and v arrays.
    """
    mask = np.full(x.shape, True)
    for qx, qy in charges_coords:
        r = np.sqrt((x - qx)**2 + (y - qy)**2)
        mask &= r >= r_min

    return x[mask], y[mask], u[mask], v[mask]

def vector_c_map(
    f_u: np.ndarray, f_v: np.ndarray, c_map: str = DEFAULT_C_MAP
) -> np.ndarray:
    """
    Generates colors for the vectors based on their magnitude.

    Args:
        f_u, f_v: The filtered electric field components.
        c_map: The name of the matplotlib colormap to use.

    Returns:
        An array of colors for each vector.
    """
    magn = np.sqrt(f_u**2 + f_v**2)
    magn_norm = np.log10(np.where(magn == 0, 1e-10, magn))
    magn_norm = (magn_norm - np.min(magn_norm)) / (np.max(magn_norm) - np.min(magn_norm))
    colormap = plt.get_cmap(c_map)
    colors = colormap(magn_norm)
    return colors

def main():
    # Grid initialization
    x, y = np.meshgrid(np.linspace(-3, 3, POINTS), np.linspace(-3, 3, POINTS))

    qx1, qy1 = 1.2, 0.0
    qx2, qy2 = -1.2, 0.0

    u1, v1 = electric_field(x, y, qx1, qy1, q=-CHARGE_VALUE)
    u2, v2 = electric_field(x, y, qx2, qy2, q=CHARGE_VALUE)
    u, v = u1 + u2, v1 + v2

    charges_coords = [(qx1, qy1), (qx2, qy2)]
    fx, fy, fu, fv = filter_values(x, y, u, v, charges_coords)

    cmap_arg = DEFAULT_C_MAP
    if len(sys.argv) > 1:
        cmap_arg = sys.argv[1]

    colors = vector_c_map(fu, fv, c_map=cmap_arg)

    magnitude = np.sqrt(fu**2 + fv**2)
    magnitude_safe = np.where(magnitude == 0, 1, magnitude)
    fu_norm = fu / magnitude_safe
    fv_norm = fv / magnitude_safe

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.quiver(fx, fy, fu_norm, fv_norm, color=colors)
    ax.set_title("Electric dipole field visualization", color="white")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, color="dimgray")
    ax.set_facecolor("black")
    fig.set_facecolor("black")
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")

    plt.show()

if __name__ == "__main__":
    main()
