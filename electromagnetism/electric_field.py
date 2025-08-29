#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
electric_field.py

A Python script to visualize the electric field of a dipole using matplotlib.
The script plots vectors of uniform length, with their color representing the
true magnitude of the field.
"""

import argparse, json, os
import matplotlib.pyplot as plt
import numpy as np

# Constants
POINTS = 31
EPSILON_ZERO = 8.85e-12

# --- Default Configuration ---
DEFAULT_CONFIG = {
    'charges': {
        'charge1': {'x': 1.2, 'y': 0.0, 'q': -1e-10},
        'charge2': {'x': -1.2, 'y': 0.0, 'q': 1e-10}
    },
    'colormap': 'inferno',
    'r_min': 0.1
}
DEFAULT_CONFIG_FILENAME = 'config_default.json'

def electric_field(
    x: np.ndarray, y: np.ndarray, qx: float, qy: float, q: float
) -> tuple[np.ndarray, np.ndarray]:
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

def filter_values(
    x: np.ndarray,
    y: np.ndarray,
    u: np.ndarray,
    v: np.ndarray,
    charges_coords: list[tuple[float, float]],
    r_min: float = 0.1,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
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
        r = np.sqrt((x - qx) ** 2 + (y - qy) ** 2)
        mask &= r >= r_min

    return x[mask], y[mask], u[mask], v[mask]

def vector_c_map(
    f_u: np.ndarray, f_v: np.ndarray, c_map: str) -> np.ndarray:
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
    magn_norm = (magn_norm - np.min(magn_norm)) / (
        np.max(magn_norm) - np.min(magn_norm)
    )
    colormap = plt.get_cmap(c_map)
    colors = colormap(magn_norm)
    return colors

def main():
    parser = argparse.ArgumentParser(
            description="Visualize the electric field of a system of point charge from a JSON configuration file. Otherwise, a default dipole configuration is used"
            )
    parser.add_argument(
            '--config',
            type=str,
            help='Path to a JSON configuration file. Arguments from this file will override the default configuration.'
            )
    args = parser.parse_args()
    config_data = DEFAULT_CONFIG

    if args.config:
        try:
            with open(args.config, 'r') as f:
                user_config = json.load(f)
            config_data.update(user_config)
            print(f"Using configuration from '{args.config}'.")

        except FileNotFoundError:
            parser.error(f"Error: the file '{args.config}' was not found.")
        except json.JSONDecodeError:
            parser.error(f"Errore: the file '{args.config}' is not a valid JSON file.")
    else:
        # If no config file is provided, create the default one if it doesn't exist
        if not os.path.exists(DEFAULT_CONFIG_FILENAME):
            with open(DEFAULT_CONFIG_FILENAME, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            print(f"No configuration file provided. A default configuration has been created at '{DEFAULT_CONFIG_FILENAME}'. You can edit this file and run the program again with `--config {DEFAULT_CONFIG_FILENAME}`.")
        else:
            print(f"No configuration file provided. Using the existing default file at '{DEFAULT_CONFIG_FILENAME}'.")
        
        # Load the default configuration
        with open(DEFAULT_CONFIG_FILENAME, 'r') as f:
            config_data = json.load(f)

    charges_config = config_data["charges"]
    cmap_config = config_data["colormap"]
    r_min_config = config_data["r_min"]

    # Grid initialization
    x, y = np.meshgrid(np.linspace(-3, 3, POINTS), np.linspace(-3, 3, POINTS))

    net_u, net_v = np.zeros_like(x), np.zeros_like(y)
    charges_coords = []

    for key, charge_info in charges_config.items():
        if not all(k in charge_info for k in ("x", "y", "q")):
            parser.error(f"Error: charge '{key}' is missing required keys (x, y, q) in the config file.")
        qx, qy, q = charge_info["x"], charge_info["y"], charge_info["q"]
        u_comp, v_comp = electric_field(x, y, qx, qy, q)
        net_u += u_comp
        net_v += v_comp
        charges_coords.append((qx, qy))

    fx, fy, fu, fv = filter_values(x, y, net_u, net_v, charges_coords, r_min_config)
    colors = vector_c_map(fu, fv, c_map=cmap_config)

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
