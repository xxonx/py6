#!/usr/bin/env python

""" Handles collision detection """

from box import Box
from circle import Circle
from vec2d import Vec2D

# Meta information
__author__ = "Matthias Wagner"
__copyright__ = "Copyright 2015"
__license__ = "GPL v2"
__version__ = "0.1.0"
__maintainer__ = "Matthias Wagner"
__email__ = "wagner.matthias@hotmail.com"
__status__ = "Development"


class CollisionDetection:

    def detect_and_handle_collision(self, obj_a, obj_b):
        if self._is_box(obj_a):
            if self._is_box(obj_b):
                self._detect_collision_box_vs_box(obj_a, obj_b)

            elif self._is_circle(obj_b):
                self._detect_collision_box_vs_circle(obj_a, obj_b)

        elif self._is_circle(obj_a):
            if self._is_box(obj_b):
                self._detect_collision_box_vs_circle(obj_b, obj_a)

            elif self._is_circle(obj_b):
                self._detect_collision_circle_vs_circle(obj_a, obj_b)

    # Type checking
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

    # Collision detection
    def _detect_collision_box_vs_box(self, box_a, box_b):
        # Look for separating axis
        if box_a.pos2.x < box_b.pos1.x or box_a.pos1.x > box_b.pos2.x:
            return
        if box_a.pos2.y < box_b.pos1.y or box_a.pos1.y > box_b.pos2.y:
            return

        # No separating axis found -> collision
        # TODO: calculate normal and penetration
        normal = 0
        penetration = 0
        collision = Collision(box_a, box_b, normal, penetration)
        self._handle_collision(collision)

    def _detect_collision_circle_vs_circle(self, circle_a, circle_b):
        radii_sum = circle_a.radius + circle_b.radius
        radii_sum_squared = radii_sum * radii_sum
        distance_squared = (circle_a.pos.x - circle_b.pos.x)**2 + \
            (circle_a.pos.y - circle_b.pos.y)**2

        # If the distance between the two center points is smaller than
        # the sum of the two radii -> collision
        if distance_squared < radii_sum_squared:
            # Calculate normal and penetration depth
            normal = circle_a.pos - circle_b.pos
            penetration = radii_sum - distance_squared**0.5

            collision = Collision(circle_a, circle_b, normal, penetration)
            self._handle_collision(collision)

    def _detect_collision_box_vs_circle(self, box, circle):
        # TODO: implement box vs circle collision detection
        pass

    # Collision handling
    def _handle_collision(self, collision):
        obj_a = collision.obj_a
        obj_b = collision.obj_b

        # Calculate the objects velocity along the normal
        obj_a.velocity_on_normal = \
            obj_a.velocity.project_onto(collision.normal)
        obj_b.velocity_on_normal = \
            obj_b.velocity.project_onto(collision.normal)

        self._positional_correction_pre_update(collision)

        # Calculate new velocities
        obj_a.velocity = self._update_velocity(obj_a, obj_b)
        obj_b.velocity = self._update_velocity(obj_b, obj_a)

        self._positional_correction_post_update(collision)

    def _update_velocity(self, obj_a, obj_b):
        relative_velocity_on_normal = \
            obj_b.velocity_on_normal - obj_a.velocity_on_normal

        restitution = min(obj_a.restitution, obj_b.restitution)

        return ((relative_velocity_on_normal * restitution * obj_b.mass) +
                (obj_a.velocity_on_normal * obj_a.mass +
                 obj_b.velocity_on_normal * obj_b.mass)) \
            .scale(1 / (obj_a.mass + obj_b.mass))

    def _positional_correction_pre_update(self, collision):
        """ Sets the object's position back to the collision point """
        obj_a = collision.obj_a
        obj_b = collision.obj_b

        relative_velocity_on_normal = \
            obj_b.velocity_on_normal - obj_a.velocity_on_normal
        collision.penetration_time = \
            collision.penetration / relative_velocity_on_normal.get_length()

        # Set object position back to collision point
        obj_a.add_to_position(obj_a.velocity * collision.penetration_time * -1)
        obj_b.add_to_position(obj_b.velocity * collision.penetration_time * -1)

    def _positional_correction_post_update(self, collision):
        """ Moves the object to the correct position, using the new
        velocities """
        obj_a = collision.obj_a
        obj_b = collision.obj_b

        # Set object position back to collision point
        obj_a.add_to_position(obj_a.velocity * collision.penetration_time)
        obj_b.add_to_position(obj_b.velocity * collision.penetration_time)


class Collision:

    def __init__(self, obj_a, obj_b, normal, penetration):
        self.obj_a = obj_a
        self.obj_b = obj_b
        self.normal = normal
        self.penetration = penetration
