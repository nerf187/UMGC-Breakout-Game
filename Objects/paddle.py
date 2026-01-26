#
# Paddle class with movement and clamp logic.
#
from Core import config


class Paddle:
    def __init__(self, x: float, y: float, width: int = None, height: int = None, speed: float = None):
        self.width = width or config.PADDLE_WIDTH
        self.height = height or config.PADDLE_HEIGHT
        self.x = float(x)  # center x
        self.y = float(y)  # center y
        self.speed = float(speed or config.PADDLE_SPEED)

    #
    # Move paddle horizontally. Direction is -1 (left) .. 1 (right).
    #
    def move(self, direction: float, dt: float) -> None:
        self.x += direction * self.speed * dt
        half = self.width / 2
        #
        # Clamp to screen
        #
        self.x = max(half, min(config.SCREEN_WIDTH - half, self.x))  # clamp x position

    def rect(self):
        return (int(self.x - self.width / 2), int(self.y - self.height / 2), int(self.width), int(self.height))  # return rect tuple

    def __repr__(self):
        return f"Paddle(x={self.x:.1f},y={self.y:.1f},w={self.width})"  # return string repr
