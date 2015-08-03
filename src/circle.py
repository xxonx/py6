#!/usr/bin/env python

""" Circle shaped rigid body """

import math

# Meta information
__author__ = "Matthias Wagner"
__copyright__ = "Copyright 2015"
__license__ = "GPL v2"
__version__ = "0.1.0"
__maintainer__ = "Matthias Wagner"
__email__ = "wagner.matthias@hotmail.com"
__status__ = "Development"


class Circle:

    def __init__(self, pos, radius, velocity=0.0, mass_per_px2=1.0,
                 restitution=1.0):
        self.pos = pos
        self.radius = radius

        self.velocity = velocity

        self.mass_per_px2 = mass_per_px2
        self.mass = self.get_area() * mass_per_px2
        self.mass_inv = 1.0 / self.mass

        self.restitution = restitution

    # Getters
    def get_momentum(self):
        return self.mass * self.velocity

    def get_area(self):
        return 2 * self.radius * math.pi

    def get_width(self):
        return abs(self.pos1.x - self.pos2.x)

    def get_height(self):
        return abs(self.pos1.y - self.pos2.y)
