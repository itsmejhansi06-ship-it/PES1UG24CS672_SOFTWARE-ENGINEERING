"""
GameEngine: owns the helicopter and all obstacles.

Handles movement, collisions, distance scoring, shield mechanics,
start countdown, and restarting after Game Over.
"""

import random
import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3

COUNTDOWN_SECONDS = 4


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0
        self.shield_active = False

        self.countdown_active = True
        self.countdown_start_time = pygame.time.get_ticks()

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(
            margin + GAP_HEIGHT // 2,
            HEIGHT - margin - GAP_HEIGHT // 2
        )

        self.obstacles.append(
            Obstacle(
                x=WIDTH,
                gap_y=gap_y,
                gap_height=GAP_HEIGHT,
                wall_width=WALL_WIDTH,
                screen_height=HEIGHT,
                speed=SCROLL_SPEED,
            )
        )

    def handle_input(self, keys_pressed):
        if self.countdown_active or self.game_over:
            return

        self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        # Restart after Game Over
        if self.game_over:
            if key == pygame.K_r:
                self._restart()
            return

        # Activate shield during normal gameplay
        if not self.countdown_active:
            if key == pygame.K_s:
                self.shield_active = True

    def _restart(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0
        self.shield_active = False

        self.countdown_active = True
        self.countdown_start_time = pygame.time.get_ticks()

    def _update_countdown(self):
        elapsed = (
            pygame.time.get_ticks() - self.countdown_start_time
        ) / 1000

        if elapsed >= COUNTDOWN_SECONDS:
            self.countdown_active = False

    def get_countdown_text(self):
        if not self.countdown_active:
            return None

        elapsed = (
            pygame.time.get_ticks() - self.countdown_start_time
        ) / 1000

        if elapsed < 1:
            return "3"
        elif elapsed < 2:
            return "2"
        elif elapsed < 3:
            return "1"
        else:
            return "START!"

    def update(self):
        # Countdown freezes the entire game
        if self.countdown_active:
            self._update_countdown()
            return

        # Game Over freezes the game
        if self.game_over:
            return

        self.helicopter.update(HEIGHT)

        self.distance += SCROLL_SPEED

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()

        self.obstacles = [
            o for o in self.obstacles
            if not o.is_off_screen()
        ]

        helicopter_rect = self.helicopter.get_rect()

        # Check collisions
        for obstacle in self.obstacles:
            collision = (
                helicopter_rect.colliderect(obstacle.get_top_rect())
                or helicopter_rect.colliderect(obstacle.get_bottom_rect())
            )

            if collision:
                if self.shield_active:
                    # Shield absorbs the collision
                    self.shield_active = False

                    # Remove the obstacle that was hit.
                    # This prevents an immediate second collision
                    # on the following frame.
                    self.obstacles.remove(obstacle)

                else:
                    # No shield -> Game Over
                    self.game_over = True

                break

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.helicopter,
            self.obstacles,
            self.shield_active,
        )

        if self.countdown_active:
            renderer.draw_banner(
                surface,
                font,
                self.get_countdown_text(),
            )
            return

        renderer.draw_text(
            surface,
            font,
            f"Distance: {self.distance}",
            (10, 10),
        )

        if self.shield_active:
            renderer.draw_text(
                surface,
                font,
                "SHIELD ACTIVE [S]",
                (10, 45),
            )

        if self.game_over:
            renderer.draw_game_over(
                surface,
                font,
                self.distance,
            )