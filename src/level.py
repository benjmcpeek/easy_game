import pygame

WORLD_WIDTH, WORLD_HEIGHT = 1800, 900
WALL_THICKNESS = 24
SPIKE_SIZE = 20
GOAL_WIDTH = 30
GOAL_HEIGHT = 50
PLATFORM_HEIGHT = 20

CURRENT_LEVEL = 0

LEVELS = [
    {
        "spawn": (100, WORLD_HEIGHT - 100),
        "platforms": [
            pygame.Rect(220, WORLD_HEIGHT - 160, 220, PLATFORM_HEIGHT),
            pygame.Rect(560, WORLD_HEIGHT - 310, 240, PLATFORM_HEIGHT),
            pygame.Rect(940, WORLD_HEIGHT - 430, 200, PLATFORM_HEIGHT),
        ],
        "obstacles": [
            pygame.Rect(440, WORLD_HEIGHT - 240, WALL_THICKNESS, 140),
            pygame.Rect(1180, WORLD_HEIGHT - 220, WALL_THICKNESS, 120),
        ],
        "spikes": [
            pygame.Rect(720, WORLD_HEIGHT - WALL_THICKNESS - SPIKE_SIZE, SPIKE_SIZE, SPIKE_SIZE),
        ],
        "goal": pygame.Rect(1700, WORLD_HEIGHT - WALL_THICKNESS - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT),
    },

    {
        "spawn": (100, WORLD_HEIGHT - 100),
        "platforms": [
            pygame.Rect(260, WORLD_HEIGHT - 210, 200, PLATFORM_HEIGHT),
            pygame.Rect(620, WORLD_HEIGHT - 350, 220, PLATFORM_HEIGHT),
            pygame.Rect(1040, WORLD_HEIGHT - 470, 200, PLATFORM_HEIGHT),
        ],
        "obstacles": [
            pygame.Rect(780, WORLD_HEIGHT - 250, WALL_THICKNESS, 150),
            pygame.Rect(1260, WORLD_HEIGHT - 280, WALL_THICKNESS, 170),
        ],
        "spikes": [
            pygame.Rect(480, WORLD_HEIGHT - WALL_THICKNESS - SPIKE_SIZE, SPIKE_SIZE, SPIKE_SIZE),
            pygame.Rect(900, WORLD_HEIGHT - WALL_THICKNESS - SPIKE_SIZE, SPIKE_SIZE, SPIKE_SIZE),
        ],
        "goal": pygame.Rect(1700, WORLD_HEIGHT - WALL_THICKNESS - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT),
    },

    {
        "spawn": (100, WORLD_HEIGHT - 100),
        "platforms": [
            pygame.Rect(220, WORLD_HEIGHT - 160, 160, PLATFORM_HEIGHT),
            pygame.Rect(520, WORLD_HEIGHT - 280, 200, PLATFORM_HEIGHT),
            pygame.Rect(860, WORLD_HEIGHT - 410, 220, PLATFORM_HEIGHT),
            pygame.Rect(1220, WORLD_HEIGHT - 530, 180, PLATFORM_HEIGHT),
        ],
        "obstacles": [
            pygame.Rect(1060, WORLD_HEIGHT - 260, WALL_THICKNESS, 140),
            pygame.Rect(1500, WORLD_HEIGHT - 320, WALL_THICKNESS, 200),
        ],
        "spikes": [
            pygame.Rect(460, WORLD_HEIGHT - WALL_THICKNESS - SPIKE_SIZE, SPIKE_SIZE, SPIKE_SIZE),
            pygame.Rect(820, WORLD_HEIGHT - WALL_THICKNESS - SPIKE_SIZE, SPIKE_SIZE, SPIKE_SIZE),
            pygame.Rect(1180, WORLD_HEIGHT - WALL_THICKNESS - SPIKE_SIZE, SPIKE_SIZE, SPIKE_SIZE),
        ],
        "goal": pygame.Rect(1700, WORLD_HEIGHT - WALL_THICKNESS - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT),
    }
]