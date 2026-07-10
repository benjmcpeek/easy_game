import pygame
from level import CURRENT_LEVEL, LEVELS 

pygame.init()

WIDTH, HEIGHT = 1250, 750
FPS = 60

# Colors
BACKGROUND = (30, 30, 40)
PLAYER_COLOR = (255, 255, 255)
WALL_COLOR = (90, 90, 90)
SPIKE_COLOR = (255, 60, 60)
GOAL_COLOR = (60, 255, 100)
PLATFORM_COLOR = (120, 120, 120)

# Screen / clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Easy Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

# Player
player = pygame.Rect(100, 650, 32, 32)
spawn_x = 100
spawn_y = 650

player_speed = 5
velocity_y = 0
gravity = 0.6
jump_power = -12
on_ground = False

# Level objects
WALL_THICKNESS = 40

walls = [
    pygame.Rect(0, 0, WIDTH, WALL_THICKNESS),
    pygame.Rect(0, HEIGHT - WALL_THICKNESS, WIDTH, WALL_THICKNESS),
    pygame.Rect(0, 0, WALL_THICKNESS, HEIGHT),
    pygame.Rect(WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT),
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
    reset_player()


game_state = "menu"
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_RETURN:
                    CURRENT_LEVEL = 0
                    load_level(CURRENT_LEVEL)
                    game_state = "playing"

            elif game_state == "playing":
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "win":
                if event.key == pygame.K_RETURN:
                    game_state = "menu"

    screen.fill(BACKGROUND)

    if game_state == "menu":
        title = font.render("Easy Game", True, (255, 255, 255))
        start = small_font.render("Press Enter to Start", True, (255, 255, 255))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 260))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 340))

    elif game_state == "playing":
        level = LEVELS[CURRENT_LEVEL]

        platforms = level["platforms"]
        obstacles = level["obstacles"]
        spikes = level["spikes"]
        goal = level["goal"]

        solid_objects = walls + platforms + obstacles

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
                reset_player()

        # Goal collision
        if player.colliderect(goal):
            CURRENT_LEVEL += 1

            if CURRENT_LEVEL >= len(LEVELS):
                game_state = "win"
            else:
                load_level(CURRENT_LEVEL)

        # Draw objects
        for wall in walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)

        for platform in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)

        for obstacle in obstacles:
            pygame.draw.rect(screen, WALL_COLOR, obstacle)

        for spike in spikes:
            pygame.draw.rect(screen, SPIKE_COLOR, spike)

        pygame.draw.rect(screen, GOAL_COLOR, goal)
        pygame.draw.rect(screen, PLAYER_COLOR, player)

        level_text = small_font.render(
            f"Level {CURRENT_LEVEL + 1}", True, (255, 255, 255)
        )
        screen.blit(level_text, (20, 20))

    elif game_state == "win":
        win_text = font.render("Congratulations!", True, (255, 255, 255))
        restart_text = small_font.render("Press Enter for Menu", True, (255, 255, 255))

        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 300))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 370))

    pygame.display.flip()

pygame.quit()