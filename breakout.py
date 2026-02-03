#
# Auto-detect and use virtual environment if available
#
from enum import Enum
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(script_dir, '..', '.venv', 'Scripts', 'python.exe')
venv_python = os.path.abspath(venv_python)

if os.path.exists(venv_python) and sys.executable != venv_python:
    import subprocess
    subprocess.run([venv_python] + sys.argv)
    sys.exit()

#
# A variant of the classic breakout arcade game.
# This file contains a `Game` class which manages a Pygame loop and renders
# `Block`, `Paddle`, and `Ball` objects. A headless test mode is provided via
# the `--headless` CLI flag to run a small smoke test without opening a window.
#
from typing import Tuple

import pygame

from Core import config
from Objects.level import Level
from Objects.paddle import Paddle
from Objects.ball import Ball

#
# Convert `#RRGGBB` to an (r,g,b) tuple.
#
def hex_to_rgb(hexstr: str) -> Tuple[int, int, int]:
    s = hexstr.lstrip("#")
    if len(s) != 6:
        return (255, 255, 255)
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))  # return rgb tuple

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4

#
# Simple Breakout game runner handling input, update and render.
#
class Game:
    def __init__(self, level_path: str):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout - Test")
        self.clock = pygame.time.Clock()

        self.level = Level.from_file(level_path)
        self.blocks = list(self.level.blocks)

        #
        # Paddle positioned near bottom center
        #
        paddle_y = config.SCREEN_HEIGHT - 40
        self.paddle = Paddle(config.SCREEN_WIDTH / 2, paddle_y)  # paddle init

        #
        # Ball starts on top of paddle
        #
        ball_x = self.paddle.x
        ball_y = self.paddle.y - self.paddle.height / 2 - config.BALL_RADIUS - 2
        self.ball = Ball(ball_x, ball_y)

        self.running = True
        self.score = 0
        self.lives = 3
        self.ball_launched = False

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        font_large = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)
        
        title = font_large.render("BREAKOUT", True, (255, 255, 255))
        start = font_small.render("Press SPACE to Start", True, (200, 200, 200))
        
        self.screen.blit(title, (config.SCREEN_WIDTH//2 - title.get_width()//2, 150))
        self.screen.blit(start, (config.SCREEN_WIDTH//2 - start.get_width()//2, 250))
        
        pygame.display.flip()

    def handle_input(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        dir = 0.0
        if keys[pygame.K_LEFT]:
            dir -= 1.0  # left key
        if keys[pygame.K_RIGHT]:
            dir += 1.0  # right key

        self.paddle.move(dir, dt)  # move paddle

    def launch_ball_if_needed(self) -> None:
        if not self.ball_launched:
            #
            # Keep ball above paddle until launched
            #
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.ball_launched = True  # space to launch
                #
                # Give initial velocity
                #
                self.ball.vx = 0.0
                self.ball.vy = -1.0  # set initial velocity

    def update(self, dt: float) -> None:
        if not self.ball_launched:
            self.launch_ball_if_needed()

        self.ball.update(dt)

        #
        # Wall collisions
        #
        if self.ball.x - self.ball.radius <= 0:  # left wall
            self.ball.x = self.ball.radius
            self.ball.vx *= -1
        if self.ball.x + self.ball.radius >= config.SCREEN_WIDTH:  # right wall
            self.ball.x = config.SCREEN_WIDTH - self.ball.radius
            self.ball.vx *= -1
        if self.ball.y - self.ball.radius <= 0:  # top wall
            self.ball.y = self.ball.radius
            self.ball.vy *= -1

        #
        # Bottom (life loss)
        #
        if self.ball.y - self.ball.radius > config.SCREEN_HEIGHT:  # ball fell
            self.lives -= 1
            if self.lives <= 0:
                self.game_state = GameState.GAME_OVER
                self.running = False  # game over
                return

            self.ball_launched = False
            # reset ball above paddle
            self.ball.x = self.paddle.x
            self.ball.y = self.paddle.y - self.paddle.height / 2 - self.ball.radius - 2
            self.ball.vx = 0.0
            self.ball.vy = -1.0

        #
        # Paddle collision (AABB vs circle simple approximation)
        #
        px, py, pw, ph = self.paddle.rect()
        bx, by, bw, bh = self.ball.rect()
        if (bx < px + pw and bx + bw > px and by < py + ph and by + bh > py):
            #
            # Reflect upward and adjust vx based on hit location on paddle
            #
            overlap_x = (self.ball.x - self.paddle.x) / (self.paddle.width / 2)
            self.ball.vx = max(-1.0, min(1.0, overlap_x))
            self.ball.vy = -abs(self.ball.vy)

        #
        # Block collisions
        #
        remaining = []
        for b in self.blocks:
            bx, by, bw, bh = b.rect()
    
            # Find closest point on block to ball
            closest_x = max(bx, min(self.ball.x, bx + bw))
            closest_y = max(by, min(self.ball.y, by + bh))
    
            # Calculate distance from closest point
            distance_x = self.ball.x - closest_x
            distance_y = self.ball.y - closest_y
            distance_squared = distance_x**2 + distance_y**2
    
            # Check collision
            if distance_squared <= self.ball.radius**2:
                destroyed = b.hit()
        
                # Determine bounce direction based on hit location
                if abs(distance_x) > abs(distance_y):
                    # Hit from left/right
                    self.ball.vx *= -1
                else:
                    # Hit from top/bottom
                    self.ball.vy *= -1
            
                if destroyed:
                    self.score += b.score
                else:
                    remaining.append(b)
            else:
                remaining.append(b)

        self.blocks = remaining

    def render(self) -> None:
        self.screen.fill((0, 0, 0))

        #
        # Draw blocks
        #
        for b in self.blocks:  # draw each block
            r = b.rect()
            color = hex_to_rgb(b.color)
            pygame.draw.rect(self.screen, color, pygame.Rect(*r))
            #
            # Draw white outline
            #
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(*r), width=1)
        # for b in self.blocks:

        #
        # Draw paddle
        #
        pr = self.paddle.rect()
        pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(*pr))

        #
        # Draw ball
        #
        pygame.draw.circle(self.screen, (255, 255, 255), (int(self.ball.x), int(self.ball.y)), self.ball.radius)

        #
        # HUD
        #
        font = pygame.font.SysFont(None, 24)
        hud = font.render(f"Score: {self.score}  Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(hud, (8, 8))

        pygame.display.flip()

    def run(self, max_frames: int = None) -> None:
        frames = 0
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.handle_input(dt)
            self.update(dt)
            self.render()

            frames += 1
            if max_frames is not None and frames >= max_frames:
                break

        pygame.quit()


def main(argv=None):
    argv = argv or sys.argv[1:]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    level_path = os.path.join(base_dir, config.LEVELS_DIR, "level1.json")
    if not os.path.exists(level_path):
        print("Level file not found:", level_path)  # if level file path exists
        return

    # headless test mode (run small number of frames and exit)
    headless = "--headless" in argv
    if headless:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")  # set dummy video driver

    game = Game(level_path)
    if headless:
        game.run(max_frames=10)  # run a short headless smoke test
    else:
        game.run()  # run interactive loop


if __name__ == "__main__":
    main()
