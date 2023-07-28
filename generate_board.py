import random
import time

import pygame


class Minesweeper:
    def __init__(self):
        self.width = 620  # width of game window
        self.height = 720  # height of game window

        self.board = None  # stores the board for each game
        self.board_size = (600, 600)  # size of the board regardless of difficulty

        self.start = True  # enables start screen at program execution
        self.game_over = False  # enables game over screen on loss

        """
        different difficulties within the game
        - when set to true it will enable the game screen to update to chosen difficulty
        - all are set to False on program execution 
        """
        self.easy = False
        self.medium = False
        self.hard = False

    def start_screen(self, screen, clock):
        screen.fill("white")
        title = pygame.font.Font("freesansbold.ttf", 75)
        text_surface = title.render("Minesweeper", True, "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width / 2, self.height / 8)
        screen.blit(text_surface, text_rect)

        button_width = 215
        button_height = 75

        pygame.draw.rect(screen, "gray", (
            self.width / 2 - button_width / 2, self.height / 2 - button_height / 2 + 100, button_width, button_height))

        medium_text = pygame.font.Font("freesansbold.ttf", 50)
        text_surface = medium_text.render("Medium", True, "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width / 2, self.height / 2 + 100)
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, "gray", (
            self.width / 2 - button_width / 2, self.height / 2 - button_height / 2 + 200, button_width, button_height))

        hard_text = pygame.font.Font("freesansbold.ttf", 50)
        text_surface = hard_text.render("Hard", True, "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width / 2, self.height / 2 + 200)
        screen.blit(text_surface, text_rect)

        while self.start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = False

            mouse = pygame.mouse.get_pos()
            clicked = pygame.mouse.get_pressed()

            """
            Button Control
            """
            if self.width / 2 - button_width / 2 < mouse[0] < self.width / 2 + button_width / 2 and \
                    self.height / 2 - button_height / 2 < mouse[1] < self.height / 2 + button_height / 2:
                pygame.draw.rect(screen, "black", (
                    self.width / 2 - button_width / 2, self.height / 2 - button_height / 2, button_width,
                    button_height), True)
                if clicked[0]:
                    self.start = False
                    self.easy = True
                    self.easy_mode(screen, clock)

            else:
                pygame.draw.rect(screen, "gray", (
                    self.width / 2 - button_width / 2, self.height / 2 - button_height / 2, button_width,
                    button_height), False)
                easy_text = pygame.font.Font("freesansbold.ttf", 50)
                text_surface = easy_text.render("Easy", True, "black")
                text_rect = text_surface.get_rect()
                text_rect.center = (self.width / 2, self.height / 2)
                screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(60)

    def easy_mode(self, screen, clock):
        screen.fill("gray")  # screen background is gray
        board_dimension = (10, 10)  # number of tiles in x and y dimension
        mine_count = 10  # number of mines in easy mode
        tile_size = self.board_size[0] / board_dimension[0]  # the size of each tile to be drawn

        self.generate_board(board_dimension)  # generate a virtual board with the given dimensions
        self.generate_mines(board_dimension, mine_count)  # place mines in the generated board

        x = self.width / 2 - self.board_size[0] / 2  # controls the starting point of where most objects are drawn
        y = self.height / 2 - self.board_size[0] / 2

        offset = 10  # border width

        # border for tile area
        pygame.draw.rect(screen, "black", (x - 10, y + 40, self.board_size[0] + 20, self.board_size[0] + 20), 10)

        # create tiles
        for row in range(board_dimension[0]):
            for col in range(board_dimension[0]):
                pygame.draw.rect(screen, "gray", (col * tile_size + x, row * tile_size + y + 50, tile_size, tile_size))
                pygame.draw.rect(screen, "black", (col * tile_size + x, row * tile_size + y + 50, tile_size, tile_size),
                                 1)

        while self.easy:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.easy = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    left_clicked = True
                else:
                    left_clicked = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mouse = pygame.mouse.get_pos()
                    right_clicked = True
                else:
                    right_clicked = False

                if left_clicked:
                    x_mouse = int((mouse[0] - offset) // tile_size)
                    y_mouse = int((mouse[1] - 110) // tile_size)
                    if 10 > x_mouse > -1 != self.board[y_mouse][x_mouse] and -1 < y_mouse < 10:
                        pygame.draw.rect(screen, "black",
                                         (x + tile_size * x_mouse, y + tile_size * y_mouse + 50, tile_size, tile_size))
                        self.scan_adjacent(screen, x_mouse, y_mouse)
                    else:
                        self.game_over = True

                if right_clicked:
                    x_mouse = (mouse[0] - offset) // tile_size
                    y_mouse = (mouse[1] - 110) // tile_size
                    if -1 < x_mouse < 10 and -1 < y_mouse < 10:
                        pygame.draw.rect(screen, "gray",
                                         (x + tile_size * x_mouse, y + tile_size * y_mouse + 50, tile_size, tile_size))
                        pygame.draw.rect(screen, "black",
                                         (x + tile_size * x_mouse, y + tile_size * y_mouse + 50, tile_size, tile_size),
                                         1)

            pygame.display.flip()
            clock.tick(60)

    def scan_adjacent(self, screen, x, y):
        pass

    def generate_board(self, dimensions):
        self.board = [[0 for _ in range(dimensions[0])] for _ in range(dimensions[1])]

    def generate_mines(self, dimensions, mine_count):
        grid_width = dimensions[0]
        grid_height = dimensions[1]
        while mine_count > 0:
            x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mine_count -= 1

        for row in self.board:
            print(row)

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper")
        clock = pygame.time.Clock()

        self.start_screen(screen, clock)

        pygame.quit()
