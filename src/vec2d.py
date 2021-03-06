#!/usr/bin/env python

""" 2D-Vector
This class is based on the Vec2D class obtained here:
http://physics.gac.edu/~miller/jterm_2013/vec2d_jdm.txt
"""

import math

# Meta information
__author__ = "Matthias Wagner"
__copyright__ = "Copyright 2015"
__license__ = "GPL v2"
__version__ = "0.1.0"
__maintainer__ = "Matthias Wagner"
__email__ = "wagner.matthias@hotmail.com"
__status__ = "Development"


class Vec2D:
    """ 2D-Vector class """

    def __init__(self, x, y, is_int=False):
        self.x = x
        self.y = y

        if is_int:
            self.x = int(round(self.x))
            self.y = int(round(self.y))
        else:
            self.x = float(self.x)
            self.y = float(self.y)

    # String representation
    def __str__(self):
        return 'Vec2D(%s, %s)' % (self.x, self.y)

    # Coordinates as tuple
    def get_tuple(self, as_int=False):
        if as_int:
            return (int(round(self.x)), int(round(self.y)))
        else:
            return (self.x, self.y)

    # Vector arithmetic, including operator overload
    # Addition
    def add(self, vec2):
        return Vec2D(self.x + vec2.x, self.y + vec2.y)

    def __add__(self, vec2):
        return Vec2D(self.x + vec2.x, self.y + vec2.y)

    # Subtraction
    def subtract(self, vec2):
        return Vec2D(self.x - vec2.x, self.y - vec2.y)

    def __sub__(self, vec2):
        return Vec2D(self.x - vec2.x, self.y - vec2.y)

    # Scale (=Multiply with scalar)
    def scale(self, factor):
        return Vec2D(self.x * factor, self.y * factor)

    def __mul__(self, factor):
        return Vec2D(self.x * factor, self.y * factor)

    def __div__(self, factor):
        return Vec2D(self.x / factor, self.y / factor)

    # Comparison
    def is_equal(self, vec2):
        return (self.x == vec2.x) and (self.y == vec2.y)

    # Length
    def get_length(self):
        return (self.x * self.x + self.y * self.y)**0.5

    def get_length_squared(self):
        return (self.x * self.x + self.y * self.y)

    # Normalized vector
    def get_normal_vector(self):
        return self / self.get_length()

    # Magnitude
    def set_magnitude(self, magnitude):
        return self.get_normal_vector() * magnitude

    # Dot product
    def dot_product(self, vec2):
        return (self.x * vec2.x) + (self.y * vec2.y)

    # Vector projection
    def project_onto(self, vec2):
        vec2_length_squared = vec2.dot_product(vec2)

        if(vec2_length_squared > 0):
            return vec2 * (self.dot_product(vec2) / vec2_length_squared)
        else:
            return self * 0

    # Rotation
    def rotate90(self):
        return Vec2D(-self.y, self.x)

    def rotate180(self):
        return Vec2D(-self.x, -self.y)

    def rotate(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)

        _x = self.x * cos - self.y * sin
        _y = self.x * sin + self.y * cos

        return Vec2D(_x, _y)

    def set_angle(self, angle_degrees):
        self.x = self.length()
        self.y = 0
        return self.rotate(angle_degrees)

    def get_angle(self):
        if (self.length_squared() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def get_angle_between(self, vec2):
        cross = self.x * vec2.y - self.y * vec2.x
        dot_product = self.dot_product(vec2)

        return math.degrees(math.atan2(cross, dot_product))
