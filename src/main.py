import math
import pygame
from level import CURRENT_LEVEL, LEVELS 

pygame.init()

WIDTH, HEIGHT = 1250, 750
WORLD_WIDTH, WORLD_HEIGHT = 1800, 900
FPS = 60
PLAYER_SIZE = 24
WALL_THICKNESS = 24
SPIKE_SIZE = 20
GOAL_WIDTH = 30
GOAL_HEIGHT = 50
PLATFORM_HEIGHT = 20

# Colors
BACKGROUND = (30, 30, 40)
PLAYER_COLOR = (255, 255, 255)
WALL_COLOR = (90, 90, 90)
SPIKE_COLOR = (255, 60, 60)
GOAL_COLOR = (60, 255, 100)
PLATFORM_COLOR = (120, 120, 120)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
BUTTON_TEXT_COLOR = (255, 255, 255)
POPUP_COLOR = (20, 20, 30)
POPUP_BORDER_COLOR = (200, 200, 200)

# Screen / clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Easy Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

# Game stats
death_count = 0

# Player
player = pygame.Rect(100, 850, PLAYER_SIZE, PLAYER_SIZE)
spawn_x = 100
spawn_y = 850

# Menu buttons
play_button = pygame.Rect(WIDTH // 2 - 150, 330, 300, 70)
instructions_button = pygame.Rect(WIDTH // 2 - 150, 430, 300, 70)

player_speed = 5
velocity_y = 0
gravity = 0.6
jump_power = -17
on_ground = False

walls = [
    pygame.Rect(0, 0, WORLD_WIDTH, WALL_THICKNESS),
    pygame.Rect(0, WORLD_HEIGHT - WALL_THICKNESS, WORLD_WIDTH, WALL_THICKNESS),
    pygame.Rect(0, 0, WALL_THICKNESS, WORLD_HEIGHT),
    pygame.Rect(WORLD_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, WORLD_HEIGHT),
]



def reset_player():
    global velocity_y, on_ground

    player.x = spawn_x
    player.y = spawn_y
    velocity_y = 0
    on_ground = False


def load_level(level_number):
    global spawn_x, spawn_y

    spawn_x, spawn_y = LEVELS[level_number]["spawn"]
    level = LEVELS[level_number]
    if "original_goal" not in level:
        level["original_goal"] = level["goal"].copy()
        level["original_spikes"] = [spike.copy() for spike in level["spikes"]]
    else:
        level["goal"] = level["original_goal"].copy()
        level["spikes"] = [spike.copy() for spike in level["original_spikes"]]
    level["goal_moved"] = False
    level["goal_returned"] = False
    level["moved_goal_position"] = None
    reset_player()


def draw_multiline_text(surface, text, font, color, x, y, line_height):
    for index, line in enumerate(text.splitlines()):
        surface.blit(font.render(line, True, color), (x, y + index * line_height))


def world_to_screen(rect, camera_x, camera_y):
    return rect.move(-camera_x, -camera_y)


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


game_state = "menu"
previous_state = None
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "menu":
                if play_button.collidepoint(event.pos):
                    CURRENT_LEVEL = 0
                    death_count = 0
                    load_level(CURRENT_LEVEL)
                    game_state = "playing"
                elif instructions_button.collidepoint(event.pos):
                    previous_state = "menu"
                    game_state = "instructions"
            elif game_state == "instructions":
                popup_rect = pygame.Rect(150, 120, WIDTH - 300, HEIGHT - 240)
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
            if game_state == "menu":
                if event.key == pygame.K_m:
                    previous_state = "menu"
                    game_state = "instructions"

            elif game_state == "playing":
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                elif event.key == pygame.K_m:
                    previous_state = "playing"
                    game_state = "instructions"

            elif game_state == "instructions":
                if event.key == pygame.K_ESCAPE:
                    game_state = previous_state or "menu"
                    previous_state = None

            elif game_state == "win":
                if event.key == pygame.K_RETURN:
                    game_state = "menu"

    screen.fill(BACKGROUND)

    if game_state == "menu":
        title = font.render("Easy Game", True, (255, 255, 255))
        play_text = small_font.render("Play", True, BUTTON_TEXT_COLOR)
        instructions_text = small_font.render("Instructions", True, BUTTON_TEXT_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        play_color = BUTTON_HOVER_COLOR if play_button.collidepoint(mouse_pos) else BUTTON_COLOR
        instructions_color = BUTTON_HOVER_COLOR if instructions_button.collidepoint(mouse_pos) else BUTTON_COLOR

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
        pygame.draw.rect(screen, play_color, play_button, border_radius=8)
        pygame.draw.rect(screen, instructions_color, instructions_button, border_radius=8)
        pygame.draw.rect(screen, POPUP_BORDER_COLOR, play_button, 3, border_radius=8)
        pygame.draw.rect(screen, POPUP_BORDER_COLOR, instructions_button, 3, border_radius=8)

        screen.blit(
            play_text,
            (
                play_button.centerx - play_text.get_width() // 2,
                play_button.centery - play_text.get_height() // 2,
            ),
        )
        screen.blit(
            instructions_text,
            (
                instructions_button.centerx - instructions_text.get_width() // 2,
                instructions_button.centery - instructions_text.get_height() // 2,
            ),
        )

    elif game_state == "playing":
        level = LEVELS[CURRENT_LEVEL]

        platforms = level["platforms"]
        obstacles = level["obstacles"]
        spikes = level["spikes"]
        goal = level["goal"]

        solid_objects = walls + platforms + obstacles

        if CURRENT_LEVEL == 0:
            distance_to_goal = math.hypot(
                player.centerx - goal.centerx,
                player.centery - goal.centery,
            )
            if not level.get("goal_moved", False):
                if distance_to_goal < 280:
                    move_goal_to_highest_platform(level)
            elif not level.get("goal_returned", False):
                if distance_to_goal < 150:
                    move_goal_back(level)

        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            player.x -= player_speed

        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        # Horizontal collision
        for solid in solid_objects:
            if player.colliderect(solid):
                if keys[pygame.K_LEFT]:
                    player.left = solid.right
                if keys[pygame.K_RIGHT]:
                    player.right = solid.left

        # Jump
        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = jump_power
            on_ground = False

        # Gravity
        velocity_y += gravity
        player.y += velocity_y

        # Vertical collision
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

        # Spike collision
        for spike in spikes:
            if player.colliderect(spike):
                death_count += 1
                reset_player()

        # Goal collision
        if player.colliderect(goal):
            CURRENT_LEVEL += 1

            if CURRENT_LEVEL >= len(LEVELS):
                game_state = "win"
            else:
                load_level(CURRENT_LEVEL)

        camera_x = player.centerx - WIDTH // 2
        camera_y = player.centery - HEIGHT // 2
        camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))
        camera_y = max(0, min(camera_y, WORLD_HEIGHT - HEIGHT))

        # Draw objects
        for wall in walls:
            pygame.draw.rect(screen, WALL_COLOR, world_to_screen(wall, camera_x, camera_y))

        for platform in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, world_to_screen(platform, camera_x, camera_y))

        for obstacle in obstacles:
            pygame.draw.rect(screen, WALL_COLOR, world_to_screen(obstacle, camera_x, camera_y))

        for spike in spikes:
            pygame.draw.rect(screen, SPIKE_COLOR, world_to_screen(spike, camera_x, camera_y))

        pygame.draw.rect(screen, GOAL_COLOR, world_to_screen(goal, camera_x, camera_y))
        pygame.draw.rect(screen, PLAYER_COLOR, world_to_screen(player, camera_x, camera_y))

        level_text = small_font.render(
            f"Level {CURRENT_LEVEL + 1}", True, (255, 255, 255)
        )
        death_text = small_font.render(
            f"Deaths: {death_count}", True, (255, 255, 255)
        )
        screen.blit(level_text, (20, 20))
        screen.blit(death_text, (WIDTH - death_text.get_width() - 20, 20))

    elif game_state == "instructions":
        popup_rect = pygame.Rect(150, 120, WIDTH - 300, HEIGHT - 240)
        title = font.render("Instructions", True, (255, 255, 255))
        instructions_text = (
            "1. Use Left and Right arrow keys to move\n"
            "2. Use Space to jump\n"
            "3. Avoid spikes and reach the goal\n"
            "4. Press 'M' to view this menu at any time\n"
            "5. Press Esc to return to the menu"
        )
        close_button = pygame.Rect(
            popup_rect.right - 220,
            popup_rect.bottom - 90,
            180,
            50,
        )
        close_text = small_font.render("Close", True, BUTTON_TEXT_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        close_color = BUTTON_HOVER_COLOR if close_button.collidepoint(mouse_pos) else BUTTON_COLOR

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, POPUP_COLOR, popup_rect)
        pygame.draw.rect(screen, POPUP_BORDER_COLOR, popup_rect, 3)
        screen.blit(
            title,
            (
                popup_rect.centerx - title.get_width() // 2,
                popup_rect.top + 30,
            ),
        )
        draw_multiline_text(
            screen,
            instructions_text,
            small_font,
            (255, 255, 255),
            popup_rect.left + 40,
            popup_rect.top + 110,
            40,
        )
        pygame.draw.rect(screen, close_color, close_button, border_radius=8)
        pygame.draw.rect(screen, POPUP_BORDER_COLOR, close_button, 3, border_radius=8)
        screen.blit(
            close_text,
            (
                close_button.centerx - close_text.get_width() // 2,
                close_button.centery - close_text.get_height() // 2,
            ),
        )

    elif game_state == "win":
        win_text = font.render("Congratulations!", True, (255, 255, 255))
        restart_text = small_font.render("Press Enter for Menu", True, (255, 255, 255))
        attempts_text = small_font.render(
            f"Completed all 3 levels in {death_count} attempt(s)",
            True,
            (255, 255, 255),
        )

        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 300))
        screen.blit(attempts_text, (WIDTH // 2 - attempts_text.get_width() // 2, 370))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 430))

    pygame.display.flip()

pygame.quit()