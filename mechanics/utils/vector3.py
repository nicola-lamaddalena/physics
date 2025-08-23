from __future__ import annotations
import math


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return f"Vector3(x={self.x}, y={self.y}, z={self.z})"

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def norm(self) -> Vector3:
        mag = self.mag()
        if mag == 0:
            return Vector3((0), 0, 0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def scale(self, k: int):
        self.x *= k
        self.y *= k
        self.z *= k

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other: Vector3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3) -> Vector3:
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def rotate_x(self, angle: float):
        theta = math.radians(angle)
        y, z = self.y, self.z
        self.y = y * math.cos(theta) - z * math.sin(theta)
        self.z = y * math.sin(theta) + z * math.cos(theta)

    def rotate_y(self, angle: float):
        theta = math.radians(angle)
        x, z = self.x, self.z
        self.x = x * math.cos(theta) + z * math.sin(theta)
        self.z = -x * math.sin(theta) + z * math.cos(theta)

    def rotate_z(self, angle: float):
        theta = math.radians(angle)
        x, y = self.x, self.y
        self.x = x * math.cos(theta) - y * math.sin(theta)
        self.y = x * math.sin(theta) + y * math.cos(theta)
