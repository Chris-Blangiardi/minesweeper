import pygame

class Minesweeper:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.start = True
        self.easy = False
        self.medium = False
        self.hard = False

    def start_screen(self, screen, clock):
        screen.fill("white")
        title = pygame.font.Font("freesansbold.ttf", 100)
        text_surface = title.render("Minesweeper", True, "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width/2, self.height/8)
        screen.blit(text_surface, text_rect)

        button_width = 215
        button_height = 75

        pygame.draw.rect(screen, "gray", (
            self.width/2 - button_width/2, self.height/2 - button_height/2 + 100, button_width, button_height))

        medium_text = pygame.font.Font("freesansbold.ttf", 50)
        text_surface = medium_text.render("Medium", True, "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width/2, self.height/2 + 100)
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, "gray", (
            self.width/2 - button_width/2, self.height/2 - button_height/2 + 200, button_width, button_height))

        hard_text = pygame.font.Font("freesansbold.ttf", 50)
        text_surface = hard_text.render("Hard", True, "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width/2, self.height/2 + 200)
        screen.blit(text_surface, text_rect)

        while self.start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = False

            mouse = pygame.mouse.get_pos()
            print(mouse)

            """
            Button Control
            """
            if self.width/2 - button_width/2 < mouse[0] < self.width/2 + button_width/2 and \
                    self.height/2 - button_height/2 < mouse[1] < self.height/2 + button_height/2:
                pygame.draw.rect(screen, "black", (
                    self.width/2 - button_width/2, self.height/2 - button_height/2, button_width, button_height), True)
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
        pass

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper")
        clock = pygame.time.Clock()

        self.start_screen(screen, clock)

        pygame.quit()
