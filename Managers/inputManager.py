from typing import Tuple
import pygame
from Managers.game_state import GameState

class inputManager:
    @staticmethod
    def handle_game_input(events, game_state: GameState, paddle, dt: float) -> None:
        keys = pygame.key.get_pressed()
        dir = 0.0
        
        if game_state == GameState.PLAYING:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dir -= 1.0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dir += 1.0
        
        # Only move paddle if we're playing
        if game_state == GameState.PLAYING:
            paddle.move(dir, dt)
    
    @staticmethod
    def check_launch_ball(keys, ball_launched: bool) -> bool:
        if not ball_launched and keys[pygame.K_SPACE]:
            return True
        return False
    
    @staticmethod
    def handle_state_transitions(events, game_state: GameState, running: bool) -> Tuple[GameState, bool, str]:
        action = ""
        
        for event in events:
            if event.type == pygame.QUIT:
                return game_state, False, "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return game_state, False, "quit"
                
                # Game state transitions
                if game_state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        return GameState.LEVEL_SELECT, running, "open_level_select"
                
                elif game_state == GameState.LEVEL_SELECT:
                    if event.key == pygame.K_UP:
                        return game_state, running, "select_prev_level"
                    elif event.key == pygame.K_DOWN:
                        return game_state, running, "select_next_level"
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return GameState.PLAYING, running, "start_selected_level"
                
                elif game_state == GameState.PLAYING:
                    if event.key == pygame.K_p:
                        return GameState.PAUSED, running, "pause"
                
                elif game_state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        return GameState.PLAYING, running, "resume"
                
                elif game_state == GameState.LEVEL_COMPLETE:
                    if event.key == pygame.K_SPACE:
                        return game_state, running, "next_level"
                    elif event.key == pygame.K_r:
                        return game_state, running, "restart_level"
                
                elif game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        return game_state, running, "restart_game"
        
        return game_state, running, action