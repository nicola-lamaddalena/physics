from __future__ import annotations
import math

class Vector3:
    """
    A 3D vector class that supports common vector operations.
    The class is immutable, meaning all operations return a new Vector3 instance.
    """
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        """
        Return the string representation of the vector.
        """
        return f"Vector3(x={self.x}, y={self.y}, z={self.z})"

    def __add__(self, other: Vector3) -> Vector3:
        """
        Return a new vector that is the sum of two vectors.
        """
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        """
        Return a new vector that is the difference of two vectors.
        """
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3:
        """
        Return a new vector scaled by a scalar value.
        """
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Vector3:
        """
        Return a new vector scaled by a scalar value (supports scalar * vector).
        """
        return self.__mul__(scalar)

    def __eq__(self, other: object) -> bool:
        """
        Check if two vectors are equal.
        """
        if not isinstance(other, Vector3):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    @property
    def mag(self):
        """
        Return the magnitude (length) of the vector.
        """
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self) -> Vector3:
        """
        Return a new normalized vector with a magnitude of 1.
        """
        mag = self.mag
        if mag == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, other: Vector3) -> float:
        """
        Return the dot product of two vectors.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3) -> Vector3:
        """
        Return the cross product of two vectors.
        """
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def rotate_x(self, angle: float) -> Vector3:
        """
        Return a new vector rotated around the x-axis by the given angle in degrees.
        """
        theta = math.radians(angle)
        y = self.y * math.cos(theta) - self.z * math.sin(theta)
        z = self.y * math.sin(theta) + self.z * math.cos(theta)
        return Vector3(self.x, y, z)

    def rotate_y(self, angle: float) -> Vector3:
        """
        Return a new vector rotated around the y-axis by the given angle in degrees.
        """
        theta = math.radians(angle)
        x = self.x * math.cos(theta) + self.z * math.sin(theta)
        z = -self.x * math.sin(theta) + self.z * math.cos(theta)
        return Vector3(x, self.y, z)

    def rotate_z(self, angle: float) -> Vector3:
        """
        Return a new vector rotated around the z-axis by the given angle in degrees.
        """
        theta = math.radians(angle)
        x = self.x * math.cos(theta) - self.y * math.sin(theta)
        y = self.x * math.sin(theta) + self.y * math.cos(theta)
        return Vector3(x, y, self.z)
