#!/usr/bin/env python

""" Handles collision detection """

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


class CollisionDetection:

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
        radii_sum_squared = radii_sum * radii_sum
        distance_squared = (circle_a.pos.x - circle_b.pos.x)**2 + \
            (circle_a.pos.y - circle_b.pos.y)**2

        # If the distance between the two center points is smaller than
        # the sum of the two radii -> collision
        return radii_sum_squared > distance_squared

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

    def handle_collision(self, obj_a, obj_b):
        normal = self.get_collision_normal(obj_a, obj_b)
        # TODO: implement penetration
        # penetration = self.get_collision_penetration(obj_a, obj_b)

        # Calculate the objects velocity along the normal
        obj_a.velocity_on_normal = obj_a.velocity.project_onto(normal)
        obj_b.velocity_on_normal = obj_b.velocity.project_onto(normal)

        # Calculate new velocities
        obj_a.velocity = self.update_velocity(obj_a, obj_b)
        obj_b.velocity = self.update_velocity(obj_b, obj_a)

    def get_collision_normal(self, obj_a, obj_b):
        # TODO: calculate normal
        return obj_a.pos - obj_b.pos

    def get_collision_penetration(self, obj_a, obj_b):
        pass  # TODO: calculate penetration

    def update_velocity(self, obj_a, obj_b):
        relative_velocity_on_normal = \
            obj_b.velocity_on_normal - obj_a.velocity_on_normal

        restitution = min(obj_a.restitution, obj_b.restitution)

        return ((relative_velocity_on_normal * restitution * obj_b.mass) +
                (obj_a.velocity_on_normal * obj_a.mass +
                 obj_b.velocity_on_normal * obj_b.mass)) \
            .scale(1 / (obj_a.mass + obj_b.mass))

    """ unused at the moment """
    def positional_correction(self, collision):
        correction_percent = 0.2
        threshold = 0.1

        if collision.penetration > threshold:
            correction_factor = collision\
                .get_positional_correction_factor(
                    threshold, correction_percent)

            collision.apply_correction_factor(correction_factor)
