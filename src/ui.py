import pygame
from settings import BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, POPUP_COLOR, POPUP_BORDER_COLOR


def draw_multiline_text(surface, text, font, color, x, y, line_height):
    for index, line in enumerate(text.splitlines()):
        surface.blit(font.render(line, True, color), (x, y + index * line_height))


def draw_button(surface, rect, text_surface, hover, border_radius=8):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)
    pygame.draw.rect(surface, POPUP_BORDER_COLOR, rect, 3, border_radius=border_radius)
    surface.blit(
        text_surface,
        (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2,
        ),
    )


def draw_instructions_popup(surface, font, small_font, mouse_pos):
    popup_rect = pygame.Rect(150, 120, 1100, 510)
    title = font.render("Instructions", True, (255, 255, 255))
    instructions_text = (
        "1. Use Left and Right arrow keys to move\n"
        "2. Use Space to jump\n"
        "3. Avoid spikes and reach the goal\n"
        "4. Press 'M' to view this menu at any time\n"
        "5. Press Esc or Close to return to the menu"
    )
    close_button = pygame.Rect(popup_rect.right - 220, popup_rect.bottom - 90, 180, 50)
    close_text = small_font.render("Close", True, BUTTON_TEXT_COLOR)
    close_hover = close_button.collidepoint(mouse_pos)

    surface.fill((0, 0, 0))
    pygame.draw.rect(surface, POPUP_COLOR, popup_rect)
    pygame.draw.rect(surface, POPUP_BORDER_COLOR, popup_rect, 3)
    surface.blit(
        title,
        (
            popup_rect.centerx - title.get_width() // 2,
            popup_rect.top + 30,
        ),
    )
    draw_multiline_text(
        surface,
        instructions_text,
        small_font,
        (255, 255, 255),
        popup_rect.left + 40,
        popup_rect.top + 110,
        40,
    )
    draw_button(surface, close_button, close_text, close_hover)
    return close_button
