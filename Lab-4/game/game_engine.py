"""
GameEngine: owns the puck, both paddles, and the computer AI, and runs
one frame's worth of game logic.

Starter version: the puck bounces around and paddles can hit it, but
there is no scoring, no match timer, and the reset that happens after
a goal is incomplete. That's what Tasks 2-4 fix/add.
"""

import random
import math

from game.puck import Puck
from game.paddle import Paddle
from game.ai import ComputerAI
from game.collisions import handle_paddle_collision
from game.renderer import WIDTH, HEIGHT, MARGIN, GOAL_TOP, GOAL_BOTTOM

PLAYER_SPEED = 6
PUCK_RADIUS = 12
PADDLE_RADIUS = 28
INITIAL_PUCK_SPEED = 4.5
MATCH_DURATION_SECONDS = 30.0


class GameEngine:
    def __init__(self):
        self.puck = Puck(WIDTH / 2, HEIGHT / 2, PUCK_RADIUS)
        self._launch_puck()

        self.player = Paddle(
            x=WIDTH * 0.15, y=HEIGHT / 2, radius=PADDLE_RADIUS,
            min_x=MARGIN + PADDLE_RADIUS, max_x=WIDTH / 2 - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS, max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )
        self.computer = Paddle(
            x=WIDTH * 0.85, y=HEIGHT / 2, radius=PADDLE_RADIUS,
            min_x=WIDTH / 2 + PADDLE_RADIUS, max_x=WIDTH - MARGIN - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS, max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )
        self.ai = ComputerAI()
        self.player_score = 0
        self.computer_score = 0
        self.remaining_time = MATCH_DURATION_SECONDS
        self.match_over = False

    def _launch_puck(self):
        angle_choices = [0.3, 0.6, -0.3, -0.6]
        direction = random.choice([-1, 1])
        vy_factor = random.choice(angle_choices)
        self.puck.vx = INITIAL_PUCK_SPEED * direction
        self.puck.vy = INITIAL_PUCK_SPEED * vy_factor

    def handle_input(self, keys_pressed):
        if self.match_over:
            return

        import pygame
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= PLAYER_SPEED
        if keys_pressed[pygame.K_DOWN]:
            dy += PLAYER_SPEED
        if keys_pressed[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys_pressed[pygame.K_RIGHT]:
            dx += PLAYER_SPEED
        self.player.move_by(dx, dy)

    def update(self, delta_time=1 / 60):
        if self.match_over:
            return

        self.remaining_time = max(0.0, self.remaining_time - delta_time)
        if self.remaining_time == 0:
            self.match_over = True
            return

        self.ai.update(self.computer, self.puck)

        previous_x, previous_y = self.puck.x, self.puck.y
        self.puck.move()

        handle_paddle_collision(self.puck, self.player, previous_x, previous_y)
        handle_paddle_collision(self.puck, self.computer, previous_x, previous_y)

        self.puck.bounce_off_walls(HEIGHT, MARGIN)

        self._handle_goals()

    def _handle_goals(self):
        if self.match_over:
            return

        fits_goal = (
            GOAL_TOP + self.puck.radius < self.puck.y
            < GOAL_BOTTOM - self.puck.radius
        )
        if self.puck.x + self.puck.radius < MARGIN and fits_goal:
            self.computer_score += 1
            self._reset_puck()
        elif self.puck.x - self.puck.radius < MARGIN and not fits_goal:
            self.puck.x = MARGIN + self.puck.radius
            self.puck.vx = -self.puck.vx
        elif self.puck.x - self.puck.radius > WIDTH - MARGIN and fits_goal:
            self.player_score += 1
            self._reset_puck()
        elif self.puck.x + self.puck.radius > WIDTH - MARGIN and not fits_goal:
            self.puck.x = WIDTH - MARGIN - self.puck.radius
            self.puck.vx = -self.puck.vx

    def get_winner(self):
        if self.player_score > self.computer_score:
            return "Player"
        if self.computer_score > self.player_score:
            return "Computer"
        return "Draw"

    def _reset_puck(self):
        self.puck.x, self.puck.y = WIDTH / 2, HEIGHT / 2
        self._launch_puck()

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_table(surface)
        renderer.draw_paddle(surface, self.player, renderer.COLOR_PLAYER)
        renderer.draw_paddle(surface, self.computer, renderer.COLOR_COMPUTER)
        renderer.draw_puck(surface, self.puck)
        renderer.draw_text(
            surface, font, f"Player: {self.player_score}",
            (MARGIN + 12, MARGIN + 8), renderer.COLOR_PLAYER,
        )
        renderer.draw_text(
            surface, font, f"Computer: {self.computer_score}",
            (WIDTH - MARGIN - 180, MARGIN + 8), renderer.COLOR_COMPUTER,
        )
        renderer.draw_text(
            surface, font, f"Time: {math.ceil(self.remaining_time):02d}s",
            (WIDTH // 2 - 50, MARGIN + 8),
        )
        if self.match_over:
            renderer.draw_banner(surface, font, self.get_winner())
