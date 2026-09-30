"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4
MAX_VERTICAL_SPEED = 5.0


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        # Move upward
        if keys_pressed[pygame.K_UP]:
            if self.vy > 0:
                self.vy = -THRUST
            else:
                self.vy -= THRUST

            self.vy = max(self.vy, -MAX_VERTICAL_SPEED)

        # Move downward
        if keys_pressed[pygame.K_DOWN]:
            if self.vy < 0:
                self.vy = THRUST
            else:
                self.vy += THRUST

            self.vy = min(self.vy, MAX_VERTICAL_SPEED)

    def update(self, height_bound):
        self.y += self.vy

        # Top boundary
        top_limit = self.height / 2

        if self.y < top_limit:
            self.y = top_limit
            self.vy = 0

        # Bottom boundary
        bottom_limit = height_bound - self.height / 2

        if self.y > bottom_limit:
            self.y = bottom_limit
            self.vy = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )