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

    # Collision
    def detect_and_handle_collision(self, obj_a, obj_b):
        if(self._is_collision(obj_a, obj_b)):
            self._handle_collision(obj_a, obj_b)

    # Collision detection

    def _is_collision(self, obj_a, obj_b):
        if self._is_box(obj_a):
            if self._is_box(obj_b):
                return self._is_collision_box_vs_box(obj_a, obj_b)
            elif self._is_circle(obj_b):
                return self._is_collision_box_vs_circle(obj_a, obj_b)
        elif self._is_circle(obj_a):
            if self._is_box(obj_b):
                return self._is_collision_box_vs_circle(obj_b, obj_a)
            elif self._is_circle(obj_b):
                return self._is_collision_circle_vs_circle(obj_a, obj_b)

        return False

    def _is_collision_box_vs_box(self, box_a, box_b):
        # Look for separating axis
        if box_a.pos2.x < box_b.pos1.x or box_a.pos1.x > box_b.pos2.x:
            return False
        if box_a.pos2.y < box_b.pos1.y or box_a.pos1.y > box_b.pos2.y:
            return False

        # No separating axis found -> collision
        return True

    def _is_collision_circle_vs_circle(self, circle_a, circle_b):
        radii_sum = circle_a.radius + circle_b.radius
        radii_sum_squared = radii_sum * radii_sum
        distance_squared = (circle_a.pos.x - circle_b.pos.x)**2 + \
            (circle_a.pos.y - circle_b.pos.y)**2

        # If the distance between the two center points is smaller than
        # the sum of the two radii -> collision
        return radii_sum_squared > distance_squared

    def _is_collision_box_vs_circle(self, box, circle):
        # TODO: implement box vs circle collision detection

        return False

    # Class checking
    def _is_box(self, obj):
        if isinstance(obj, Box):
            return True
        else:
            return False

    def _is_circle(self, obj):
        if isinstance(obj, Circle):
            return True
        else:
            return False

    # Collision handling

    def _handle_collision(self, obj_a, obj_b):
        normal = self._get_collision_normal(obj_a, obj_b)
        # TODO: implement penetration
        # penetration = self._get_collision_penetration(obj_a, obj_b)

        # Calculate the objects velocity along the normal
        obj_a.velocity_on_normal = obj_a.velocity.project_onto(normal)
        obj_b.velocity_on_normal = obj_b.velocity.project_onto(normal)

        # Calculate new velocities
        obj_a.velocity = self._update_velocity(obj_a, obj_b)
        obj_b.velocity = self._update_velocity(obj_b, obj_a)

    def _get_collision_normal(self, obj_a, obj_b):
        # TODO: calculate normal
        return obj_a.pos - obj_b.pos

    def _get_collision_penetration(self, obj_a, obj_b):
        pass  # TODO: calculate penetration

    def _update_velocity(self, obj_a, obj_b):
        relative_velocity_on_normal = \
            obj_b.velocity_on_normal - obj_a.velocity_on_normal

        restitution = min(obj_a.restitution, obj_b.restitution)

        return ((relative_velocity_on_normal * restitution * obj_b.mass) +
                (obj_a.velocity_on_normal * obj_a.mass +
                 obj_b.velocity_on_normal * obj_b.mass)) \
            .scale(1 / (obj_a.mass + obj_b.mass))

    """ unused at the moment """
    def _positional_correction(self, collision):
        correction_percent = 0.2
        threshold = 0.1

        if collision.penetration > threshold:
            correction_factor = collision\
                .get_positional_correction_factor(
                    threshold, correction_percent)

            collision.apply_correction_factor(correction_factor)
