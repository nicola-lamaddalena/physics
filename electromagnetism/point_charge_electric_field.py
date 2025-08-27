#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 18:01:11 2025

@author: nico
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

points = 21
# Creazione di una griglia di punti
x, y = np.meshgrid(np.linspace(-2, 2, points), np.linspace(-2, 2, points))


# Calcolo dei componenti del campo vettoriale (u, v)
def electric_field(
    x: list[float], y: list[float], qx: float, qy: float, q: float = 10e-10
) -> tuple[list[float], list[float]]:
    r = np.sqrt((x - qx) ** 2 + (y - qy) ** 2)
    eps_zero = 8.85 * 10e-12
    theta = np.arctan2(y - qy, x - qx)
    # avoid singularity
    E = np.where(r == 0, 0, q / (4 * np.pi * eps_zero * r**2))
    Ex = E * np.cos(theta)
    Ey = E * np.sin(theta)
    return Ex, Ey


def filter_values(x, y, u, v, qx1, qy1, qx2, qy2):
    # Raggio minimo di esclusione
    r_min = 0.8

    # Calcola la distanza di ogni punto dalla prima carica
    r1 = np.sqrt((x - qx1) ** 2 + (y - qy1) ** 2)

    # Calcola la distanza di ogni punto dalla seconda carica
    r2 = np.sqrt((x - qx2) ** 2 + (y - qy2) ** 2)

    # Crea una maschera che include solo i punti lontani da entrambe le cariche
    mask = (r1 >= r_min) & (r2 >= r_min)

    # Applica la maschera ai dati per filtrare i valori
    filter_x = x[mask]
    filter_y = y[mask]
    filter_u = u[mask]
    filter_v = v[mask]

    return filter_x, filter_y, filter_u, filter_v


def vector_c_map(
    f_u: list[float], f_v: list[float], c_map: str = "hot"
) -> list[float]:
    magn = np.sqrt(f_u**2 + f_v**2)
    magn_norm = np.log10(magn)
    magn_norm = magn_norm / np.max(magn_norm)
    colormap = matplotlib.colormaps[c_map]
    colors = colormap(magn_norm)
    return colors


qx1, qy1 = 1.2, 0
qx2, qy2 = -1.2, 0
u1, v1 = electric_field(x, y, qx1, qy1)
u2, v2 = electric_field(x, y, qx2, qy2, q=-10e-10)
u, v = u1 + u2, v1 + v2
fx, fy, fu, fv = filter_values(x, y, u, v, qx1, qy1, qx2, qy2)
colors = vector_c_map(u, v)
# u, v = electric_field(x, y, qx2, qy2)

# Creazione del plot
plt.figure()
plt.quiver(fx, fy, fu, fv)
# plt.quiver(x,y, u, v)
# plt.title("Electric field of a point charge in the origin (0,0)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()
