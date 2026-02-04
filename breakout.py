#
# Auto-detect and use virtual environment if available
#
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
import pygame

from Core import config
from Objects.paddle import Paddle
from Objects.ball import Ball
from UI.menu import menu, hex_to_rgb
from Managers import GameState, collisionManager, inputManager, scoreManager

class Game:
    def __init__(self, initial_level: int = 1):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_state = GameState.MENU
        self.running = True
        self.score = 0
        self.lives = 3
        self.ball_launched = False
        
        # Managers
        self.ui = menu()
        self.level_manager = scoreManager()
        
        # Load initial level
        if not self.level_manager.load_level(initial_level):
            print(f"Failed to load level {initial_level}")
            self.running = False
            return
        
        # Initialize game objects
        self.reset_paddle_and_ball()

    def reset_paddle_and_ball(self) -> None:
        # Paddle positioned near bottom center
        paddle_y = config.SCREEN_HEIGHT - 40
        self.paddle = Paddle(config.SCREEN_WIDTH / 2, paddle_y)
        
        # Ball starts on top of paddle
        ball_x = self.paddle.x
        ball_y = self.paddle.y - self.paddle.height / 2 - config.BALL_RADIUS - 2
        self.ball = Ball(ball_x, ball_y)
        self.ball_launched = False

    def reset_level_state(self) -> None:
        self.level_manager.reset_level_blocks()
        self.reset_paddle_and_ball()

    def reset_game_state(self) -> None:
        self.level_manager.reset_level_blocks()
        self.lives = 3
        self.score = 0
        self.reset_paddle_and_ball()

    def next_level(self) -> None:
        success, message = self.level_manager.next_level()
        if success:
            self.reset_paddle_and_ball()
            self.game_state = GameState.PLAYING
        else:   # No more levels = game complete
            self.game_state = GameState.GAME_OVER
            print(message)

    def launch_ball_if_needed(self) -> None:
        if not self.ball_launched:
            self.ui.draw_launch_hint(self.screen)
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if inputManager.check_launch_ball(keys, self.ball_launched):
                self.ball_launched = True
                self.ball.vx = 0.0
                self.ball.vy = -1.0

    def update(self, dt: float) -> None:
        if self.game_state != GameState.PLAYING:
            return
            
        if not self.ball_launched:
            self.launch_ball_if_needed()
            # Keep ball on paddle
            self.ball.x = self.paddle.x
            self.ball.y = self.paddle.y - self.paddle.height / 2 - self.ball.radius - 2
            return

        self.ball.update(dt)

        # Check collisions
        collisionManager.check_ball_walls(self.ball)
        
        # Check bottom collision (life loss)
        if collisionManager.check_ball_bottom(self.ball):
            self.handle_life_loss()
            return
            
        # Check paddle collision
        collisionManager.check_ball_paddle(self.ball, self.paddle)
        
        # Check block collisions
        self.level_manager.blocks, score_increase = collisionManager.check_ball_blocks(
            self.ball, self.level_manager.blocks
        )
        self.score += score_increase
        
        # Check level completion
        if len(self.level_manager.blocks) == 0:
            self.game_state = GameState.LEVEL_COMPLETE

    #
    # Bottom (life loss)
    #
    def handle_life_loss(self) -> None:
        self.lives -= 1
        if self.lives <= 0:
            self.game_state = GameState.GAME_OVER
            return
            
        self.ball_launched = False
        self.ball.x = self.paddle.x
        self.ball.y = self.paddle.y - self.paddle.height / 2 - self.ball.radius - 2
        self.ball.vx = 0.0
        self.ball.vy = -1.0

    def render(self) -> None:
        self.screen.fill((0, 0, 0))

        #
        # Draw blocks
        #
        for block in self.level_manager.blocks:
            r = block.rect()
            color = hex_to_rgb(block.color)
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
        level_info = self.level_manager.get_level_info()
        self.ui.draw_hud(self.screen, self.score, self.lives, level_info["number"])

    def process_actions(self, action: str) -> None:
        if action == "next_level":
            self.next_level()

        elif action == "restart_level":
            self.reset_level_state()
            self.game_state = GameState.PLAYING

        elif action == "restart_game":
            self.level_manager.load_level(1)
            self.score = 0
            self.reset_game_state()
            self.game_state = GameState.PLAYING

        elif action == "retry_level":
            self.reset_level_state()
            self.game_state = GameState.PLAYING

    def run(self, max_frames: int = None) -> None:
        frames = 0
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            
            # Get events
            events = pygame.event.get()
            
            # Handle input and state transitions
            self.game_state, self.running, action = inputManager.handle_state_transitions(
                events, self.game_state, self.running
            )
            
            # Process actions
            if action:
                self.process_actions(action)
            
            # Handle game input (paddle movement)
            inputManager.handle_game_input(events, self.game_state, self.paddle, dt)
            
            # Update and render based on game state
            if self.game_state == GameState.MENU:
                self.ui.draw_menu(self.screen)
                pygame.display.flip()
                
            elif self.game_state == GameState.PLAYING:
                self.update(dt)
                self.render()
                if not self.ball_launched:
                    self.ui.draw_launch_hint(self.screen)
                pygame.display.flip()
                
            elif self.game_state == GameState.PAUSED:
                self.render()
                self.ui.draw_pause_screen(self.screen)
                pygame.display.flip()
                
            elif self.game_state == GameState.LEVEL_COMPLETE:
                level_info = self.level_manager.get_level_info()
                self.ui.draw_next_level(self.screen, level_info["number"], self.score)
                pygame.display.flip()
                
            elif self.game_state == GameState.GAME_OVER:
                level_info = self.level_manager.get_level_info()
                self.ui.draw_game_over(self.screen, self.lives, self.score)
                pygame.display.flip()

            frames += 1
            if max_frames is not None and frames >= max_frames:
                break

        pygame.quit()

def main(argv=None):
    argv = argv or sys.argv[1:]
    
    # Check for level parameter
    start_level = 1
    for arg in argv:
        if arg.startswith("--level="):
            try:
                start_level = int(arg.split("=")[1])
            except ValueError:
                print(f"Invalid level number: {arg}")
                return
    
    # headless test mode
    headless = "--headless" in argv
    if headless:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy") # set dummy video driver
    
    game = Game(initial_level=start_level)
    if headless:
        game.run(max_frames=10)  # run a short headless smoke test
    else:
        game.run()  # run interactive loop


if __name__ == "__main__":
    main()
