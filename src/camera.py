def world_to_screen(rect, camera_x, camera_y):
    return rect.move(-camera_x, -camera_y)


def clamp_camera(x, y, width, height, world_width, world_height):
    x = max(0, min(x, world_width - width))
    y = max(0, min(y, world_height - height))
    return x, y
