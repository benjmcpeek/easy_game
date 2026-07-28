import math
import pygame
from settings import (
    BACKGROUND,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    FPS,
    GAME_FONT_SIZE,
    GOAL_COLOR,
    GOAL_HEIGHT,
    GOAL_WIDTH,
    GRAVITY,
    HEIGHT,
    JUMP_POWER,
    PLAYER_COLOR,
    PLAYER_SPEED,
    PLATFORM_COLOR,
    SPIKE_COLOR,
    SPIKE_SIZE,
    WALL_COLOR,
    WIDTH,
    WORLD_HEIGHT,
    WORLD_WIDTH,
    SMALL_FONT_SIZE,
    WALL_THICKNESS,
)
from camera import clamp_camera, world_to_screen
from level import LEVELS
from player import create_player, reset_player
from ui import draw_button, draw_instructions_popup, draw_multiline_text


SPIKE_IMAGE = pygame.image.load("assets/spike.png")
SPIKE_IMAGE = pygame.transform.scale(SPIKE_IMAGE, (SPIKE_SIZE, SPIKE_SIZE))

SHOW_WHOLE_LEVEL = True
OVERVIEW_SCALE = 0.65


def initialize_walls():
    return [
        pygame.Rect(0, 0, WORLD_WIDTH, WALL_THICKNESS),
        pygame.Rect(0, WORLD_HEIGHT - WALL_THICKNESS, WORLD_WIDTH, WALL_THICKNESS),
        pygame.Rect(0, 0, WALL_THICKNESS, WORLD_HEIGHT),
        pygame.Rect(WORLD_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, WORLD_HEIGHT),
    ]


def initialize_level(level):
    if "original_goal" not in level:
        level["original_goal"] = level["goal"].copy()
        level["original_spikes"] = [spike.copy() for spike in level["spikes"]]
        level["original_platforms"] = [platform.copy() for platform in level.get("platforms", [])]
        level["original_floor_removal_rect"] = (
            level.get("floor_removal_rect").copy() if level.get("floor_removal_rect") else None
        )
    else:
        level["goal"] = level["original_goal"].copy()
        level["spikes"] = [spike.copy() for spike in level["original_spikes"]]
        level["platforms"] = [platform.copy() for platform in level["original_platforms"]]
        level["floor_removal_rect"] = (
            level["original_floor_removal_rect"].copy() if level["original_floor_removal_rect"] else None
        )

    level["goal_moved"] = False
    level["goal_returned"] = False
    level["moved_goal_position"] = None
    level["floor_removed"] = False


def load_level(level_index, player):
    level = LEVELS[level_index]
    initialize_level(level)
    spawn_x, spawn_y = level["spawn"]
    reset_player(player, spawn_x, spawn_y)
    return level


def update_first_level_floor(level, player):
    if level.get("floor_removed", False):
        return

    floor_rect = level.get("floor_removal_rect")
    if floor_rect is None:
        return

    trigger_x = level.get("floor_remove_trigger_x", level["goal"].left - 120)
    if player.centerx >= trigger_x:
        level["platforms"] = [
            platform
            for platform in level["platforms"]
            if not (
                platform.x == floor_rect.x
                and platform.y == floor_rect.y
                and platform.width == floor_rect.width
                and platform.height == floor_rect.height
            )
        ]
        level["floor_removed"] = True


def update_first_level_goal(level, player):

    if level.get("goal_moved", False):
        return

    trigger_distance = level.get("goal_trigger_distance", 80)

    if abs(player.centerx - level["goal"].centerx) <= trigger_distance:
        level["goal"].topleft = level["goal_move_to"]
        level["goal_moved"] = True


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Easy Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, GAME_FONT_SIZE)
    small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

    player = create_player()
    walls = initialize_walls()
    play_button = pygame.Rect(WIDTH // 2 - 150, 330, 300, 70)
    instructions_button = pygame.Rect(WIDTH // 2 - 150, 430, 300, 70)

    current_level = 0
    level = load_level(current_level, player)
    velocity_y = 0
    on_ground = False
    death_count = 0
    game_state = "menu"
    previous_state = None
    running = True

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "menu":
                    if play_button.collidepoint(event.pos):
                        current_level = 0
                        death_count = 0
                        level = load_level(current_level, player)
                        game_state = "playing"
                    elif instructions_button.collidepoint(event.pos):
                        previous_state = "menu"
                        game_state = "instructions"

                elif game_state == "instructions":
                    popup_rect = pygame.Rect(150, 120, 1100, 510)
                    close_button = pygame.Rect(
                        popup_rect.right - 220,
                        popup_rect.bottom - 90,
                        180,
                        50,
                    )
                    if close_button.collidepoint(event.pos):
                        game_state = previous_state or "menu"
                        previous_state = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and game_state != "instructions":
                    previous_state = game_state
                    game_state = "instructions"

                elif event.key == pygame.K_ESCAPE:
                    if game_state == "playing":
                        game_state = "menu"
                    elif game_state == "instructions":
                        game_state = previous_state or "menu"
                        previous_state = None

                elif event.key == pygame.K_RETURN and game_state == "win":
                    game_state = "menu"

        screen.fill(BACKGROUND)

        if game_state == "menu":
            title = font.render("Easy Game", True, BUTTON_TEXT_COLOR)
            play_text = small_font.render("Play", True, BUTTON_TEXT_COLOR)
            instructions_text = small_font.render("Instructions", True, BUTTON_TEXT_COLOR)
            draw_button(screen, play_button, play_text, play_button.collidepoint(mouse_pos))
            draw_button(
                screen,
                instructions_button,
                instructions_text,
                instructions_button.collidepoint(mouse_pos),
            )
            screen.blit(
                title,
                (
                    WIDTH // 2 - title.get_width() // 2,
                    220,
                ),
            )

        elif game_state == "playing":
            solid_objects = walls + level["platforms"] + level["obstacles"]

            if current_level == 0:
                update_first_level_floor(level, player)
                update_first_level_goal(level, player)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED

            for solid in solid_objects:
                if player.colliderect(solid):
                    if keys[pygame.K_LEFT]:
                        player.left = solid.right
                    if keys[pygame.K_RIGHT]:
                        player.right = solid.left

            if keys[pygame.K_SPACE] and on_ground:
                velocity_y = JUMP_POWER
                on_ground = False

            velocity_y += GRAVITY
            player.y += velocity_y
            on_ground = False

            for solid in solid_objects:
                if player.colliderect(solid):
                    if velocity_y > 0:
                        player.bottom = solid.top
                        velocity_y = 0
                        on_ground = True
                    elif velocity_y < 0:
                        player.top = solid.bottom
                        velocity_y = 0

            for spike in level["spikes"]:
                if player.colliderect(spike):
                    death_count += 1
                    velocity_y = 0
                    on_ground = False
                    initialize_level(level)
                    reset_player(player, *level["spawn"])
                    break

            if player.colliderect(level["goal"]):
                current_level += 1
                if current_level >= len(LEVELS):
                    game_state = "win"
                else:
                    level = load_level(current_level, player)

            if SHOW_WHOLE_LEVEL:
                camera_x = 0
                camera_y = 0
            else:
                camera_x = player.centerx - WIDTH // 2
                camera_y = player.centery - HEIGHT // 2
                camera_x, camera_y = clamp_camera(
                    camera_x,
                    camera_y,
                    WIDTH,
                    HEIGHT,
                    WORLD_WIDTH,
                    WORLD_HEIGHT,
                )

            def draw_scaled_rect(color, rect):
                screen_rect = world_to_screen(rect, camera_x, camera_y)
                scaled_rect = pygame.Rect(
                    int(screen_rect.x * OVERVIEW_SCALE),
                    int(screen_rect.y * OVERVIEW_SCALE),
                    max(1, int(screen_rect.width * OVERVIEW_SCALE)),
                    max(1, int(screen_rect.height * OVERVIEW_SCALE)),
                )
                pygame.draw.rect(screen, color, scaled_rect)

            if SHOW_WHOLE_LEVEL:
                for wall in walls:
                    draw_scaled_rect(WALL_COLOR, wall)
                for platform in level["platforms"]:
                    draw_scaled_rect(PLATFORM_COLOR, platform)
                for obstacle in level["obstacles"]:
                    draw_scaled_rect(WALL_COLOR, obstacle)
                for spike in level["spikes"]:
                    screen_pos = world_to_screen(spike, camera_x, camera_y)
                    scaled_pos = (int(screen_pos.x * OVERVIEW_SCALE), int(screen_pos.y * OVERVIEW_SCALE))
                    scaled_spike = pygame.transform.scale(
                        SPIKE_IMAGE,
                        (
                            max(1, int(SPIKE_SIZE * OVERVIEW_SCALE)),
                            max(1, int(SPIKE_SIZE * OVERVIEW_SCALE)),
                        ),
                    )
                    screen.blit(scaled_spike, scaled_pos)
                goal_rect = world_to_screen(level["goal"], camera_x, camera_y)
                pygame.draw.rect(
                    screen,
                    GOAL_COLOR,
                    pygame.Rect(
                        int(goal_rect.x * OVERVIEW_SCALE),
                        int(goal_rect.y * OVERVIEW_SCALE),
                        max(1, int(goal_rect.width * OVERVIEW_SCALE)),
                        max(1, int(goal_rect.height * OVERVIEW_SCALE)),
                    ),
                )
                player_rect = world_to_screen(player, camera_x, camera_y)
                pygame.draw.rect(
                    screen,
                    PLAYER_COLOR,
                    pygame.Rect(
                        int(player_rect.x * OVERVIEW_SCALE),
                        int(player_rect.y * OVERVIEW_SCALE),
                        max(1, int(player_rect.width * OVERVIEW_SCALE)),
                        max(1, int(player_rect.height * OVERVIEW_SCALE)),
                    ),
                )
            else:
                for wall in walls:
                    pygame.draw.rect(screen, WALL_COLOR, world_to_screen(wall, camera_x, camera_y))
                for platform in level["platforms"]:
                    pygame.draw.rect(screen, PLATFORM_COLOR, world_to_screen(platform, camera_x, camera_y))
                for obstacle in level["obstacles"]:
                    pygame.draw.rect(screen, WALL_COLOR, world_to_screen(obstacle, camera_x, camera_y))
                for spike in level["spikes"]:
                    screen_pos = world_to_screen(spike, camera_x, camera_y)
                    screen.blit(SPIKE_IMAGE, screen_pos)
                pygame.draw.rect(screen, GOAL_COLOR, world_to_screen(level["goal"], camera_x, camera_y))
                pygame.draw.rect(screen, PLAYER_COLOR, world_to_screen(player, camera_x, camera_y))

            level_text = small_font.render(f"Level {current_level + 1}", True, BUTTON_TEXT_COLOR)
            death_text = small_font.render(f"Deaths: {death_count}", True, BUTTON_TEXT_COLOR)
            screen.blit(level_text, (20, 20))
            screen.blit(death_text, (WIDTH - death_text.get_width() - 20, 20))

        elif game_state == "instructions":
            draw_instructions_popup(screen, font, small_font, mouse_pos)

        elif game_state == "win":
            win_text = font.render("Congratulations!", True, BUTTON_TEXT_COLOR)
            restart_text = small_font.render("Press Enter for Menu", True, BUTTON_TEXT_COLOR)
            attempts_text = small_font.render(
                f"Completed all {len(LEVELS)} levels in {death_count} attempt(s)",
                True,
                BUTTON_TEXT_COLOR,
            )

            screen.blit(
                win_text,
                (WIDTH // 2 - win_text.get_width() // 2, 300),
            )
            screen.blit(
                attempts_text,
                (WIDTH // 2 - attempts_text.get_width() // 2, 370),
            )
            screen.blit(
                restart_text,
                (WIDTH // 2 - restart_text.get_width() // 2, 430),
            )

        pygame.display.flip()

    pygame.quit()
