#
# Ball class with basic movement and normalized velocity.
#
from Core import config
import math


class Ball:
    def __init__(self, x: float, y: float, radius: int = None, speed: float = None, vx: float = 0.0, vy: float = -1.0):
        self.radius = int(radius or config.BALL_RADIUS)
        self.x = float(x)
        self.y = float(y)
        self.speed = float(speed or config.BALL_SPEED)

        #
        # Normalize initial velocity
        #
        mag = math.hypot(vx, vy)
        if mag == 0:
            vx, vy = 0.0, -1.0
            mag = 1.0
        self.vx = vx / mag
        self.vy = vy / mag

    def update(self, dt: float) -> None:
        self.x += self.vx * self.speed * dt
        self.y += self.vy * self.speed * dt  # update position

    def rect(self):
        return (int(self.x - self.radius), int(self.y - self.radius), int(self.radius * 2), int(self.radius * 2))  # return rect tuple

    def __repr__(self):
        return f"Ball(x={self.x:.1f},y={self.y:.1f},vx={self.vx:.2f},vy={self.vy:.2f})"  # return string repr
