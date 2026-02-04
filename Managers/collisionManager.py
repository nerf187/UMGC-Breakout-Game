import math
from typing import List, Tuple, Optional
from Core import config
from Objects.block import Block
from Objects.ball import Ball
from Objects.paddle import Paddle

class collisionManager:
    @staticmethod
    #
    # Wall collisions
    #
    def check_ball_walls(ball: Ball) -> None:
        # Left wall
        if ball.x - ball.radius <= 0:
            ball.x = ball.radius
            ball.vx = abs(ball.vx)
        
        # Right wall
        if ball.x + ball.radius >= config.SCREEN_WIDTH:
            ball.x = config.SCREEN_WIDTH - ball.radius
            ball.vx = -abs(ball.vx)
        
        # Top wall
        if ball.y - ball.radius <= 0:
            ball.y = ball.radius
            ball.vy = abs(ball.vy)
    
    @staticmethod
    def check_ball_paddle(ball: Ball, paddle: Paddle) -> bool:
        px, py, pw, ph = paddle.rect()
        bx, by, bw, bh = ball.rect()
        
        if (bx < px + pw and bx + bw > px and by < py + ph and by + bh > py):
            if ball.vy > 0:  # Only bounce if ball is moving downward
                ball.bounce_from_paddle(paddle.x, paddle.width)
                # Position ball above paddle to prevent sticking
                ball.y = py - ball.radius - 1
                return True
        return False
    
    @staticmethod
    def check_ball_blocks(ball: Ball, blocks: List[Block]) -> Tuple[List[Block], int]:
        remaining = []
        score_increase = 0
        
        for block in blocks:
            bx, by, bw, bh = block.rect()
            
            # Find closest point on block to ball
            closest_x = max(bx, min(ball.x, bx + bw))
            closest_y = max(by, min(ball.y, by + bh))
            
            # Calculate distance from closest point
            distance_x = ball.x - closest_x
            distance_y = ball.y - closest_y
            distance_squared = distance_x**2 + distance_y**2
            
            # Check collision
            if distance_squared <= ball.radius**2:
                destroyed = block.hit()
                
                # Determine bounce direction based on hit location
                if abs(distance_x) > abs(distance_y):
                    # Hit from left/right
                    ball.vx *= -1
                else:
                    # Hit from top/bottom
                    ball.vy *= -1
                
                if destroyed:
                    score_increase += block.score
                else:
                    remaining.append(block)
            else:
                remaining.append(block)
        
        return remaining, score_increase
    
    @staticmethod
    def check_ball_bottom(ball: Ball) -> bool:
        return ball.y - ball.radius > config.SCREEN_HEIGHT