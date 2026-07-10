import pygame
from settings import PLAYER_SIZE


def create_player():
    return pygame.Rect(100, 850, PLAYER_SIZE, PLAYER_SIZE)


def reset_player(player, spawn_x, spawn_y):
    player.x = spawn_x
    player.y = spawn_y
    return player
