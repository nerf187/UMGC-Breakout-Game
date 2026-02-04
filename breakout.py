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
from UI.menu import MenuManager, hex_to_rgb  # CHANGED: Import from UI module

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4
    LIFE_LOST = 5

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

        # Game state
        self.game_state = GameState.MENU
        self.running = True
        self.score = 0
        self.lives = 3
        self.ball_launched = False
        
        # UI Manager
        self.ui = MenuManager()

    def reset_game_state(self):
        self.blocks = list(self.level.blocks)
        
        # Paddle positioned near bottom center
        paddle_y = config.SCREEN_HEIGHT - 40
        self.paddle = Paddle(config.SCREEN_WIDTH / 2, paddle_y)
        
        # Ball starts on top of paddle
        ball_x = self.paddle.x
        ball_y = self.paddle.y - self.paddle.height / 2 - config.BALL_RADIUS - 2
        self.ball = Ball(ball_x, ball_y)
        
        self.score = 0
        self.lives = 3
        self.ball_launched = False

    def handle_input(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        dir = 0.0
        
        if self.game_state == GameState.PLAYING:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dir -= 1.0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dir += 1.0
        
        # Only move paddle if we're playing
        if self.game_state == GameState.PLAYING:
            self.paddle.move(dir, dt)

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
            # keep ball on paddle
            self.ball.x = self.paddle.x
            self.ball.y = self.paddle.y - self.paddle.height / 2 - self.ball.radius - 2
            return

        self.ball.update(dt)

        #
        # Wall collisions
        #
        if self.ball.x - self.ball.radius <= 0:  # left wall
            self.ball.x = self.ball.radius
            self.ball.vx = abs(self.ball.vx)  # reflect right
        if self.ball.x + self.ball.radius >= config.SCREEN_WIDTH:  # right wall
            self.ball.x = config.SCREEN_WIDTH - self.ball.radius
            self.ball.vx = -abs(self.ball.vx)  # reflect left
        if self.ball.y - self.ball.radius <= 0:  # top wall
            self.ball.y = self.ball.radius
            self.ball.vy = abs(self.ball.vy)  # reflect down

        #
        # Bottom (life loss)
        #
        if self.ball.y - self.ball.radius > config.SCREEN_HEIGHT:  # ball fell
            self.lives -= 1
            if self.lives <= 0:
                self.game_state = GameState.GAME_OVER
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
            if self.ball.vy > 0:
                self.ball.bounce_from_paddle(self.paddle.x, self.paddle.width)
                # position ball above paddle to prevent sticking
                self.ball.y = py - self.ball.radius - 1

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

        # Check level completion
        if len(self.blocks) == 0:
            self.game_state = GameState.LEVEL_COMPLETE

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
        self.ui.draw_hud(self.screen, self.score, self.lives)

        pygame.display.flip()

    def run(self, max_frames: int = None) -> None:
        frames = 0
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0

            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                    # game state transitions
                    if self.game_state == GameState.MENU:
                        if event.key == pygame.K_SPACE:
                            self.game_state = GameState.PLAYING
                    
                    elif self.game_state == GameState.PLAYING:
                        if event.key == pygame.K_p:
                            self.game_state = GameState.PAUSED
                    
                    elif self.game_state == GameState.PAUSED:
                        if event.key == pygame.K_p:
                            self.game_state = GameState.PLAYING
                    
                    elif self.game_state in [GameState.GAME_OVER, GameState.LEVEL_COMPLETE]:
                        if event.key == pygame.K_r:
                            self.reset_game_state()
                            self.game_state = GameState.PLAYING

            # Update based on game state
            if self.game_state == GameState.MENU:
                self.ui.draw_menu(self.screen)
                pygame.display.flip()
                
            elif self.game_state == GameState.PLAYING:
                self.handle_input(dt)
                self.update(dt)
                self.render()
                
            elif self.game_state == GameState.PAUSED:
                self.render()  # Draw game in background
                self.ui.draw_pause_screen(self.screen)
                pygame.display.flip()
                
            elif self.game_state in [GameState.GAME_OVER, GameState.LEVEL_COMPLETE]:
                self.ui.draw_game_over(self.screen, self.lives, self.score)
                pygame.display.flip()

            frames += 1
            if max_frames is not None and frames >= max_frames:
                break

        pygame.quit()


def main(argv=None):
    argv = argv or sys.argv[1:]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    level_path = os.path.join(base_dir, config.LEVELS_DIR, "testlevel.json")
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
    