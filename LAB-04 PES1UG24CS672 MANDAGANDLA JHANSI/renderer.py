"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (140, 200, 230)
COLOR_HELI = (60, 60, 70)
COLOR_OBSTACLE = (70, 150, 80)
COLOR_TEXT = (20, 20, 20)

COLOR_SHIELD = (40, 120, 255)


def draw_scene(surface, helicopter, obstacles, shield_active=False):
    surface.fill(COLOR_BG)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(
            surface,
            COLOR_OBSTACLE,
            obstacle.get_top_rect()
        )

        pygame.draw.rect(
            surface,
            COLOR_OBSTACLE,
            obstacle.get_bottom_rect()
        )

    # Draw shield behind/around helicopter
    if shield_active:
        helicopter_rect = helicopter.get_rect()

        center = helicopter_rect.center

        pygame.draw.circle(
            surface,
            COLOR_SHIELD,
            center,
            max(helicopter_rect.width, helicopter_rect.height) // 2 + 10,
            4,
        )

    # Draw helicopter
    pygame.draw.rect(
        surface,
        COLOR_HELI,
        helicopter.get_rect(),
        border_radius=4
    )


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(
        font.render(text, True, color),
        pos
    )


def draw_banner(surface, font, text):
    surf = font.render(
        text,
        True,
        (180, 40, 40)
    )

    rect = surf.get_rect(
        center=(
            surface.get_width() // 2,
            surface.get_height() // 2
        )
    )

    surface.blit(surf, rect)


def draw_game_over(surface, font, distance):
    game_over_surf = font.render(
        "GAME OVER",
        True,
        (180, 40, 40)
    )

    distance_surf = font.render(
        f"Final Distance: {distance}",
        True,
        COLOR_TEXT
    )

    restart_surf = font.render(
        "Press R to Restart",
        True,
        COLOR_TEXT
    )

    center_x = surface.get_width() // 2
    center_y = surface.get_height() // 2

    game_over_rect = game_over_surf.get_rect(
        center=(center_x, center_y - 45)
    )

    distance_rect = distance_surf.get_rect(
        center=(center_x, center_y)
    )

    restart_rect = restart_surf.get_rect(
        center=(center_x, center_y + 45)
    )

    surface.blit(game_over_surf, game_over_rect)
    surface.blit(distance_surf, distance_rect)
    surface.blit(restart_surf, restart_rect)