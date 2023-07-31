import random
import time

import pygame
import visual


class Minesweeper:
    def __init__(self):
        self.width = 620  # width of game window
        self.height = 720  # height of game window

        self.board = None  # stores the board for each game
        self.resolution = (600, 600)  # size of the board regardless of difficulty

        self.start = True  # enables start screen at program execution
        self.game_over = False  # enables game over screen on loss

        self.visited = []  # tracks which tiles have been searched for mines
        self.flagged = []  # tracks which tiles have been flagged by user

        self.x_border = self.width / 2 - self.resolution[0] / 2  # controls the starting point of most drawn objects
        self.y_border = self.height / 2 - self.resolution[0] / 2 + 40
        self.border_width = 10  # border width

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
        tile_count = 10  # number of tiles in x and y dimension
        mine_count = 10  # number of mines in easy mode
        tile_size = self.resolution[0] / tile_count  # the size of each tile to be drawn

        self.generate_board(tile_count)
        self.generate_mines(tile_count, mine_count)

        visual.draw_border(screen, self.x_border, self.y_border, self.border_width, self.resolution)
        visual.draw_tiles(screen, self.x_border, self.y_border, self.border_width, tile_size, tile_count)

        while self.easy:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.easy = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # tile selection with left-click
                    mouse = pygame.mouse.get_pos()
                    left_clicked = True
                else:
                    mouse = pygame.mouse.get_pos()
                    left_clicked = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # flag with right-click
                    mouse = pygame.mouse.get_pos()
                    right_clicked = True
                else:
                    right_clicked = False

                if left_clicked and self.game_over is False:
                    x = int((mouse[0] - self.border_width) // tile_size)
                    y = int((mouse[1] - 110) // tile_size)
                    if -1 < x < tile_count and -1 < y < tile_count:
                        if self.board[y][x] != -1:
                            self.scan_adjacent(screen, x, y, tile_size, tile_count, [])
                        else:
                            x_border, y_border = self.x_border, self.y_border
                            visual.draw_explosion(screen, x_border, y_border, self.border_width, x, y, tile_size)
                            self.game_over = True
                            print("Game Over")

                if right_clicked:
                    x = (mouse[0] - self.border_width) // tile_size
                    y = (mouse[1] - 110) // tile_size
                    if -1 < x < 10 and -1 < y < 10:
                        if (x, y) in self.flagged:
                            self.flagged.remove((x, y))
                            x_border, y_border = self.x_border, self.y_border
                            visual.draw_flag(screen, x_border, y_border, self.border_width, x, y, tile_size, "gray")
                        else:
                            self.flagged.append((x, y))
                            x_border, y_border = self.x_border, self.y_border
                            visual.draw_flag(screen, x_border, y_border, self.border_width, x, y, tile_size, "white")

            pygame.display.flip()
            clock.tick(60)

    def scan_adjacent(self, screen, x, y, tile_size, tile_count, to_visit):
        potential_visit = []
        must_visit = []

        self.visited.append((x, y))

        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if 0 <= x + dx < tile_count and 0 <= y + dy < tile_count:
                    if self.board[y + dy][x + dx] == -1:
                        count += 1
                    else:
                        potential_visit.append((x + dx, y + dy))

        if count > 0:
            visual.draw_bomb_count(screen, self.x_border, self.y_border, self.border_width, x, y, tile_size, count)
        else:
            visual.draw_visited_tiles(screen, self.x_border, self.y_border, self.border_width, x, y, tile_size)
            must_visit += potential_visit

        while must_visit:
            x, y = must_visit.pop(0)
            if (x, y) not in self.visited:
                self.scan_adjacent(screen, x, y, tile_size, tile_count, must_visit)

        return

    def generate_board(self, dimensions):
        """
        create and empty board

        :param dimensions: size of the playing board (based on difficulty)
        :return:
        """
        self.board = [[0 for _ in range(dimensions)] for _ in range(dimensions)]  # 2-dimensional array of zeros

    def generate_mines(self, dimensions, mine_count):
        """
        update empty board to have mines in it
        - bombs are placed randomly each time
        - bombs are indicated by the value -1

        :param dimensions: size of the playing board (based on difficulty)
        :param mine_count: number of mines to generate (based on difficulty)
        :return:
        """
        width = dimensions
        height = dimensions
        while mine_count > 0:
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mine_count -= 1

        """
        used for testing purposes (remove at the end)
        """
        for row in self.board:
            print(row)

    def play(self):
        pygame.init()

        screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Minesweeper")

        clock = pygame.time.Clock()

        self.start_screen(screen, clock)

        pygame.quit()
