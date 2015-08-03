#!/usr/bin/env python

""" Handles collision detection """

from vec2d import Vec2D

from box import Box
from circle import Circle

# Meta information
__author__ = "Matthias Wagner"
__copyright__ = "Copyright 2015"
__license__ = "GPL v2"
__version__ = "0.1.0"
__maintainer__ = "Matthias Wagner"
__email__ = "wagner.matthias@hotmail.com"
__status__ = "Development"


class collision_detection:

    # Collision detection

    def is_collision(self, obj_a, obj_b):
        if self.is_box(obj_a) and self.is_box(obj_b):
            return self.is_collision_box_vs_box(obj_a, obj_b)
        elif self.is_circle(obj_a) and self.is_circle(obj_b):
            return self.is_collision_circle_vs_circle(obj_a, obj_b)
        else:
            return False

    def is_collision_box_vs_box(self, box_a, box_b):
        # Look for separating axis
        if box_a.pos2.x < box_b.pos1.x or box_a.pos1.x > box_b.pos2.x:
            return False
        if box_a.pos2.y < box_b.pos1.y or box_a.pos1.y > box_b.pos2.y:
            return False

        # No separating axis found -> collision
        return True

    def is_collision_circle_vs_circle(self, circle_a, circle_b):
        radii_sum = circle_a.radius + circle_b.radius
        radii_sum *= radii_sum
        distance_squared = (circle_a.pos.x + circle_b.pos.x)**2 + \
            (circle_a.pos.y + circle_b.pos.y)**2

        # If the distance between the two center points is smaller than
        # the sum of the two radii -> collision
        return radii_sum < distance_squared

    # Class checking
    def is_box(self, obj):
        if isinstance(obj, Box):
            return True
        else:
            return False

    def is_circle(self, obj):
        if isinstance(obj, Circle):
            return True
        else:
            return False

    # Collision handling

    def handle_collision(self, collision):
        relative_velocity = collision.get_relative_velocity()

        velocity_along_normal = \
            collision.get_velocity_along_normal(relative_velocity)

        if velocity_along_normal > 0:
            return

        restitution = collision.get_restitution()

        # Get impulse scalar
        scalar = collision.get_impulse_scalar(restitution,
                                              velocity_along_normal)

        # Apply impulse, update object velocity
        impulse = collision.get_impulse(scalar)
        collision.update_velocity(impulse)

    def positional_correction(self, collision):
        correction_percent = 0.2
        threshold = 0.1

        if collision.penetration > threshold:
            correction_factor = collision\
                .get_positional_correction_factor(
                    threshold, correction_percent)

            collision.apply_correction_factor(correction_factor)

class Collision:

    def __init__(self, obj_a, obj_b, penetration, normal):
        self.obj_a = obj_a
        self.obj_b = obj_b
        self.penetration = penetration
        self.normal = normal

    def get_relative_velocity(self):
        return self.obj_b.velocity - self.obj_a.velocity

    def get_velocity_along_normal(self, relative_velocity):
        return relative_velocity.dot_product(self.normal)

    def get_restitution(self):
        return min(self.obj_a.restitution, self.obj_b.restitution)

    def get_impulse_scalar(self, restitution, velocity_along_normal):
        scalar = -(1 + restitution) * velocity_along_normal
        scalar /= self.obj_a.mass_inv + self.obj_b.mass_inv
        return scalar

    def get_impulse(self, impulse_scalar):
        return impulse_scalar * self.normal

    def update_velocity(self, impulse):
        self.obj_a.velocity -= self.obj_a.mass_inv * impulse
        self.obj_b.velocity += self.obj_b.mass_inv * impulse

    def get_positional_correction_factor(self, threshold, correction_percent):
        return (self.penetration - threshold) / \
                (self.obj_a.mass_inv + self.obj_b.mass_inv) * \
                correction_percent * self.normal

    def apply_correction_factor(self, correction_factor):
        self.obj_a.add_to_position(-self.obj_a.inv_mass * correction_factor)
        self.obj_b.add_to_position(self.obj_b.inv_mass * correction_factor)
