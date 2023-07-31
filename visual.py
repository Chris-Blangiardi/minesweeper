import pygame


def draw_border(screen, x, y, offset, resolution):
    """
    draws a border to place the tiles within

    :param screen: pygame window
    :param x: coordinate of where to start drawing
    :param y: coordinate of where to start drawing
    :param offset: border width
    :param resolution: 600x600
    :return: None
    """
    pygame.draw.rect(screen, "black", (
        x - offset, y, resolution[0] + 2 * offset, resolution[0] + 2 * offset), offset)


def draw_tiles(screen, x, y, offset, tile_size, tile_count):
    """
    draws the tiles for the game within the border

    :param screen: pygame window
    :param x: coordinate of where to start drawing
    :param y: coordinate of where to start drawing
    :param offset: border width
    :param tile_size: varies with mode selection
    :param tile_count: number of tiles in x and y direction
    :return: None
    """
    for row in range(tile_count):
        for col in range(tile_count):
            pygame.draw.rect(screen, "gray",
                             (col * tile_size + x, row * tile_size + y + offset, tile_size, tile_size))
            pygame.draw.rect(screen, "black",
                             (col * tile_size + x, row * tile_size + y + offset, tile_size, tile_size), 1)


def draw_bomb_count(screen, x_border, y_border, offset, x, y, tile_size, count):
    """
    draws the number of bombs near a selected tile

    :param screen: pygame window
    :param x_border: coordinate of where to start drawing
    :param y_border: coordinate of where to start drawing
    :param offset: border width
    :param x: x coordinate of mouse
    :param y: y coordinate of mouse
    :param tile_size: varies with mode selection
    :param count: number of bombs detected
    :return: None
    """
    count_text = pygame.font.Font("freesansbold.ttf", 50)
    text_surface = count_text.render(f'{count}', True, "black")
    text_rect = text_surface.get_rect()
    text_rect.center = (x_border + tile_size * (x + 0.5), y_border + tile_size * (y + 0.5) + offset)
    screen.blit(text_surface, text_rect)


def draw_visited_tiles(screen, x_border, y_border, offset, x, y, tile_size):
    """
    shows all tiles that aren't near mines from selected location

    :param screen: pygame window
    :param x_border: coordinate of where to start drawing
    :param y_border: coordinate of where to start drawing
    :param offset: border width
    :param x: x coordinate of mouse
    :param y: y coordinate of mouse
    :param tile_size: varies with mode selection
    :return: None
    """
    color = (212, 212, 212)
    location = (x * tile_size + x_border, y * tile_size + y_border + offset, tile_size, tile_size)
    pygame.draw.rect(screen, color, location)
    pygame.draw.rect(screen, "black", location, 1)


def draw_explosion(screen, x_border, y_border, offset, x, y, tile_size):
    """
        draws an explosion on a mine tile

        :param screen: pygame window
        :param x_border: coordinate of where to start drawing
        :param y_border: coordinate of where to start drawing
        :param offset: border width
        :param x: x coordinate of mouse
        :param y: y coordinate of mouse
        :param tile_size: varies with mode selection
        :return: None
        """
    location = (x * tile_size + x_border, y * tile_size + y_border + offset, tile_size, tile_size)
    pygame.draw.rect(screen, "red", location)
    pygame.draw.rect(screen, "black", location, 1)


def draw_flag(screen, x_border, y_border, offset, x, y, tile_size, color):
    """
        draws a flag on selected tile

        :param screen: pygame window
        :param x_border: coordinate of where to start drawing
        :param y_border: coordinate of where to start drawing
        :param offset: border width
        :param x: x coordinate of mouse
        :param y: y coordinate of mouse
        :param tile_size: varies with mode selection
        :param color: switches the color of tile (depends on flagged or not)
        :return: None
    """
    location = (x * tile_size + x_border, y * tile_size + y_border + offset, tile_size, tile_size)
    pygame.draw.rect(screen, color, location)
    pygame.draw.rect(screen, "black", location, 1)
