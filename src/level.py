
import pygame


WIDTH, HEIGHT = 1250, 750
WALL_THICKNESS = 40

CURRENT_LEVEL = 0

LEVELS = [
    {
        "spawn": (100, 650),
        "platforms": [
            pygame.Rect(180, 620, 180, 25),
            pygame.Rect(430, 550, 160, 25),
        ],
        "obstacles": [
            pygame.Rect(360, HEIGHT - WALL_THICKNESS - 120, 40, 120),
        ],
        "spikes": [
            pygame.Rect(500, HEIGHT - WALL_THICKNESS - 30, 30, 30),
        ],
        "goal": pygame.Rect(1140, HEIGHT - WALL_THICKNESS - 60, 40, 60)
    },

    {
        "spawn": (100, 650),
        "platforms": [
            pygame.Rect(250, 600, 160, 25),
            pygame.Rect(520, 500, 160, 25),
        ],
        "obstacles": [
            pygame.Rect(700, HEIGHT - WALL_THICKNESS - 160, 40, 160),
        ],
        "spikes": [
            pygame.Rect(450, HEIGHT - WALL_THICKNESS - 30, 30, 30),
            pygame.Rect(850, HEIGHT - WALL_THICKNESS - 30, 30, 30),
        ],
        "goal": pygame.Rect(1140, HEIGHT - WALL_THICKNESS - 60, 40, 60)
    },

    {
        "spawn": (100, 650),
        "platforms": [
            pygame.Rect(200, 620, 140, 25),
            pygame.Rect(440, 520, 140, 25),
            pygame.Rect(680, 420, 140, 25),
        ],
        "obstacles": [
            pygame.Rect(900, HEIGHT - WALL_THICKNESS - 220, 40, 220),
        ],
        "spikes": [
            pygame.Rect(400, HEIGHT - WALL_THICKNESS - 30, 30, 30),
            pygame.Rect(700, HEIGHT - WALL_THICKNESS - 30, 30, 30),
            pygame.Rect(1000, HEIGHT - WALL_THICKNESS - 30, 30, 30),
        ],
        "goal": pygame.Rect(1140, HEIGHT - WALL_THICKNESS - 60, 40, 60)
    }
]