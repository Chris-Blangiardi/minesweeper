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
        self.win = False  # enables the win screen

        self.visited = []  # tracks which tiles have been searched for mines
        self.flagged = []  # tracks which tiles have been flagged by user
        self.time = 0  # track playtime

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
                if event.type == pygame.QUIT:  # checks for user quitting application
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

                if self.check_win(tile_count, mine_count):
                    self.game_over = True
                    self.win = True
                    print("You won")

                if left_clicked and self.game_over is False:  # check to see if tile is a mine, empty, or near mine
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

                if right_clicked and self.game_over is False:  # user can flag tile to track predicted mine locations
                    x = (mouse[0] - self.border_width) // tile_size
                    y = (mouse[1] - 110) // tile_size
                    if -1 < x < tile_count and -1 < y < tile_count:
                        if (x, y) in self.flagged:
                            self.flagged.remove((x, y))
                            x_border, y_border = self.x_border, self.y_border
                            visual.draw_flag(screen, x_border, y_border, self.border_width, x, y, tile_size, "gray")
                        else:
                            self.flagged.append((x, y))
                            x_border, y_border = self.x_border, self.y_border
                            visual.draw_flag(screen, x_border, y_border, self.border_width, x, y, tile_size, "white")

            self.time += 1
            visual.draw_time(screen, self.time)

            clock.tick(60)
            pygame.display.flip()

    def scan_adjacent(self, screen, x, y, tile_size, tile_count, must_visit):
        """
        check tiles surrounding a visited tile if there is no mine near it
        - runs recursively until it has found all tiles that have a mine near the selected tile

        :param screen: pygame window
        :param x: coordinate of where to start drawing
        :param y: coordinate of where to start drawing
        :param tile_size: varies with mode selection
        :param tile_count: number of tiles in x and y direction
        :param must_visit: list of tiles to visit
        :return: None
        """
        potential_visit = []  # stores 8 tiles around a given tile

        self.visited.append((x, y))  # mark current tile as visited

        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:  # pass over the current x, y coordinate
                    continue
                if 0 <= x + dx < tile_count and 0 <= y + dy < tile_count:  # verify tile is on the board
                    if self.board[y + dy][x + dx] == -1:  # increase mine count otherwise potentially check in future
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
        :return: None
        """
        self.board = [[0 for _ in range(dimensions)] for _ in range(dimensions)]  # 2-dimensional array of zeros

    def generate_mines(self, dimensions, mine_count):
        """
        update empty board to have mines in it
        - bombs are placed randomly each time
        - bombs are indicated by the value -1

        :param dimensions: size of the playing board (based on difficulty)
        :param mine_count: number of mines to generate (based on difficulty)
        :return: None
        """
        width = dimensions
        height = dimensions
        while mine_count > 0:
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)  # random spot to place mine
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mine_count -= 1

        """
        used for testing purposes (remove at the end)
        """
        for row in self.board:
            print(row)

    def check_win(self, dimensions, mine_count):
        """
        check to see if all tiles have been discovered that aren't bombs

        :param dimensions: size of the playing board (based on difficulty)
        :param mine_count: number of mines to generate (based on difficulty)
        :return: True or False
        """
        if len(self.visited) == dimensions * dimensions - mine_count:
            return True
        else:
            return False

    def play(self):
        """
        pygame setup, brings user to the start screen

        :return: None
        """
        pygame.init()  # initialize pygame
        screen = pygame.display.set_mode((self.width, self.height))  # create a game window with set dimensions
        pygame.display.set_caption("Minesweeper")  # title for the game window
        clock = pygame.time.Clock()  # used to keep track of time

        self.start_screen(screen, clock)

        pygame.quit()
