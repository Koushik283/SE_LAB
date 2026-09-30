"""
collisions: puck-vs-paddle collision handling.
"""

import math


def handle_paddle_collision(puck, paddle, previous_x=None, previous_y=None):
    """
    Sweep the puck's movement against the paddle and resolve any overlap.
    Returns True if a collision was handled this frame.
    """
    dx = puck.x - paddle.x
    dy = puck.y - paddle.y
    radius = puck.radius + paddle.radius
    distance = math.hypot(dx, dy)

    if distance < radius:
        if distance == 0:
            speed = math.hypot(puck.vx, puck.vy)
            if speed == 0:
                normal_x, normal_y = 1.0, 0.0
            else:
                normal_x, normal_y = -puck.vx / speed, -puck.vy / speed
        else:
            normal_x, normal_y = dx / distance, dy / distance

        puck.x = paddle.x + normal_x * radius
        puck.y = paddle.y + normal_y * radius
        velocity_into_paddle = puck.vx * normal_x + puck.vy * normal_y
        if velocity_into_paddle < 0:
            puck.vx -= 2 * velocity_into_paddle * normal_x
            puck.vy -= 2 * velocity_into_paddle * normal_y
        return True

    if previous_x is None or previous_y is None:
        return False

    start_x = previous_x - paddle.x
    start_y = previous_y - paddle.y
    move_x = puck.x - previous_x
    move_y = puck.y - previous_y
    a = move_x * move_x + move_y * move_y
    if a == 0:
        return False

    b = 2 * (start_x * move_x + start_y * move_y)
    c = start_x * start_x + start_y * start_y - radius * radius
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return False

    contact_time = (-b - math.sqrt(discriminant)) / (2 * a)
    if not 0 <= contact_time <= 1:
        return False

    contact_x = start_x + move_x * contact_time
    contact_y = start_y + move_y * contact_time
    contact_distance = math.hypot(contact_x, contact_y)
    normal_x = contact_x / contact_distance
    normal_y = contact_y / contact_distance
    velocity_into_paddle = puck.vx * normal_x + puck.vy * normal_y
    if velocity_into_paddle < 0:
        puck.vx -= 2 * velocity_into_paddle * normal_x
        puck.vy -= 2 * velocity_into_paddle * normal_y
        remaining_time = 1 - contact_time
        puck.x = paddle.x + contact_x + normal_x * 1e-6 + puck.vx * remaining_time
        puck.y = paddle.y + contact_y + normal_y * 1e-6 + puck.vy * remaining_time
        return True

    return False
