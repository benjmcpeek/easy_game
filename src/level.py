import pygame

WORLD_WIDTH, WORLD_HEIGHT = 1800, 900
WALL_THICKNESS = 20
SPIKE_SIZE = 20
GOAL_WIDTH = 30
GOAL_HEIGHT = 50
PLATFORM_HEIGHT = 20
RAISED_FLOOR_Y = WORLD_HEIGHT // 2

CURRENT_LEVEL = 0


def create_spike_row(start_x, end_x, y):
    return [pygame.Rect(x, y, SPIKE_SIZE, SPIKE_SIZE) for x in range(start_x, end_x, SPIKE_SIZE)]


LEVELS = [
    {
        "spawn": (100, RAISED_FLOOR_Y - 24),
        "platforms": [
            pygame.Rect(20, RAISED_FLOOR_Y, 1400, PLATFORM_HEIGHT),
            pygame.Rect(1420, RAISED_FLOOR_Y, 360, PLATFORM_HEIGHT),
        ],
        "floor_removal_rect": pygame.Rect(1420, RAISED_FLOOR_Y, 360, PLATFORM_HEIGHT),
        "floor_remove_trigger_x": 1500,
        "obstacles": [

        ],
        "solo_spikes": [
            pygame.Rect(500, RAISED_FLOOR_Y - SPIKE_SIZE, SPIKE_SIZE, SPIKE_SIZE),
            pygame.Rect(900, RAISED_FLOOR_Y - SPIKE_SIZE, SPIKE_SIZE, SPIKE_SIZE),
        ],
        "spikes": create_spike_row(20, 1770, WORLD_HEIGHT - SPIKE_SIZE - WALL_THICKNESS - 4),
        "goal": pygame.Rect(1700, RAISED_FLOOR_Y - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT),
        "goal_move_to": (300, WORLD_HEIGHT - WALL_THICKNESS - GOAL_HEIGHT,),
        "goal_trigger_distance": 80,
    },

    {
        "spawn": (100, RAISED_FLOOR_Y - 24),
        "platforms": [
            pygame.Rect(20, RAISED_FLOOR_Y, 1400, PLATFORM_HEIGHT),
            pygame.Rect(1420, RAISED_FLOOR_Y, 360, PLATFORM_HEIGHT),
        ],
        "floor_removal_rect": pygame.Rect(1420, RAISED_FLOOR_Y, 360, PLATFORM_HEIGHT),
        "floor_remove_trigger_x": 1500,
        "obstacles": [

        ],
        "spikes": create_spike_row(20, 1770, WORLD_HEIGHT - SPIKE_SIZE - WALL_THICKNESS - 4),
        "goal": pygame.Rect(1700, RAISED_FLOOR_Y - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)
    },

    {
        "spawn": (100, RAISED_FLOOR_Y - 24),
        "platforms": [
            pygame.Rect(20, RAISED_FLOOR_Y, 1400, PLATFORM_HEIGHT),
            pygame.Rect(1420, RAISED_FLOOR_Y, 360, PLATFORM_HEIGHT),
        ],
        "floor_removal_rect": pygame.Rect(1420, RAISED_FLOOR_Y, 360, PLATFORM_HEIGHT),
        "floor_remove_trigger_x": 1500,
        "obstacles": [

        ],
        "spikes": create_spike_row(20, 1770, WORLD_HEIGHT - SPIKE_SIZE - WALL_THICKNESS - 4),
        "goal": pygame.Rect(1700, RAISED_FLOOR_Y - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)
    }
]