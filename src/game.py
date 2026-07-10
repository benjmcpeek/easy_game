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
    else:
        level["goal"] = level["original_goal"].copy()
        level["spikes"] = [spike.copy() for spike in level["original_spikes"]]

    level["goal_moved"] = False
    level["goal_returned"] = False
    level["moved_goal_position"] = None


def load_level(level_index, player):
    level = LEVELS[level_index]
    initialize_level(level)
    spawn_x, spawn_y = level["spawn"]
    reset_player(player, spawn_x, spawn_y)
    return level


def move_goal_to_highest_platform(level):
    highest_platform = min(level["platforms"], key=lambda p: p.top)
    goal_rect = level["goal"]
    goal_rect.x = highest_platform.centerx - GOAL_WIDTH // 2
    goal_rect.y = highest_platform.top - GOAL_HEIGHT
    level["moved_goal_position"] = goal_rect.copy()
    level["goal_moved"] = True


def move_goal_back(level):
    moved_pos = level.get("moved_goal_position")
    if moved_pos is not None:
        spike_rect = pygame.Rect(
            moved_pos.centerx - SPIKE_SIZE // 2,
            moved_pos.bottom - SPIKE_SIZE,
            SPIKE_SIZE,
            SPIKE_SIZE,
        )
        level["spikes"].append(spike_rect)
    level["goal"] = level["original_goal"].copy()
    level["goal_returned"] = True


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
                distance_to_goal = math.hypot(
                    player.centerx - level["goal"].centerx,
                    player.centery - level["goal"].centery,
                )
                if not level.get("goal_moved", False) and distance_to_goal < 280:
                    move_goal_to_highest_platform(level)
                elif level.get("goal_moved", False) and not level.get("goal_returned", False) and distance_to_goal < 150:
                    move_goal_back(level)

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
                velocity_y = -17
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
                    reset_player(player, *level["spawn"])
                    break

            if player.colliderect(level["goal"]):
                current_level += 1
                if current_level >= len(LEVELS):
                    game_state = "win"
                else:
                    level = load_level(current_level, player)

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

            for wall in walls:
                pygame.draw.rect(screen, WALL_COLOR, world_to_screen(wall, camera_x, camera_y))
            for platform in level["platforms"]:
                pygame.draw.rect(screen, PLATFORM_COLOR, world_to_screen(platform, camera_x, camera_y))
            for obstacle in level["obstacles"]:
                pygame.draw.rect(screen, WALL_COLOR, world_to_screen(obstacle, camera_x, camera_y))
            for spike in level["spikes"]:
                pygame.draw.rect(screen, SPIKE_COLOR, world_to_screen(spike, camera_x, camera_y))
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
