import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (100, 100, 100)
RED = (255, 100, 0)

WIDTH = 10
HEIGHT = 15
cell_size = 20
AUTODOWN_1 = pygame.USEREVENT + 1
AUTODOWN_2 = pygame.USEREVENT + 2

PAUSE = True
divider = 300
font = "Arial"

O = [[1, 1], [1, 1]]
L = [[0, 0, 0], [1, 1, 1], [0, 0, 1]]
J = [[0, 0, 1], [1, 1, 1], [0, 0, 0]]
T = [[0, 1, 0], [0, 1, 1], [0, 1, 0]]
I = [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]
Z = [[1, 0], [1, 1], [0, 1]]
S = [[0, 1], [1, 1], [1, 0]]


class Field:
    def __init__(self, width, height, screen, start_x=cell_size, start_y=cell_size):
        self.width = width
        self.height = height
        self.field = [[1] * 4 + [0] * (self.width - 6) + [1] * 4] * 2 + \
                     [([1] + [0] * self.width + [1]) for i in range(self.height)] + [[1] * (self.width + 2)]
        self.score = 0
        self.k = self.lines = 0
        self.score_plus = self.score_up = 0
        self.start_x, self.start_y = start_x, start_y
        self.frames = 0
        self.game = False
        self.figure_last_x = 0
        self.figure_last_y = 0
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, (0, 200, 100), (self.start_x, self.start_y, WIDTH * cell_size, HEIGHT * cell_size))
        for i in range(2, self.height + 2):
            for j in range(1, self.width + 1):
                if self.field[i][j]:
                    pygame.draw.rect(self.screen, RED,
                                     [self.start_x + int((j - 0.65) * cell_size),
                                      self.start_y + int((i - 1.65) * cell_size),
                                      int(cell_size * 0.3), int(cell_size * 0.3)])
                    pygame.draw.lines(self.screen, RED, 1,
                                      [(self.start_x + (j - 1) * cell_size + 1, self.start_y + (i - 2) * cell_size + 1),
                                       (self.start_x + (j - 1) * cell_size + 1, self.start_y + (i - 1) * cell_size - 3),
                                       (self.start_x + j * cell_size - 3, self.start_y + (i - 1) * cell_size - 3),
                                       (self.start_x + j * cell_size - 3, self.start_y + (i - 2) * cell_size + 1)], 4)

    def add_figure(self, figure):
        for i in range(len(figure.figure)):
            for j in range(len(figure.figure[i])):
                if figure.figure[i][j]:
                    self.field[j + figure.y][i + figure.x] = 1

    def check_line(self):
        self.score_up = 0
        for i in range(HEIGHT + 2):
            if (0 not in self.field[i]) and (i != (HEIGHT + 2)):
                self.field.pop(i)
                self.field.insert(2, ([1] + [0] * self.width + [1]))
                self.k += 1
                self.lines += 1
                self.figure_last_y = i
                self.score_plus = 100 * (self.k ** 2 - (self.k - 1) ** 2) + 25 * (self.height - i + 1)
                self.score_up += self.score_plus
                self.score += self.score_plus

    def fly_points(self):
        if self.k > 0 and self.frames < 80:
            score_plus = pygame.font.SysFont(font, int(cell_size + cell_size / 4 * self.k)) \
                .render(("+" + str(self.score_up)), 0, (100, 100, 100, 10))
            score_plus.set_alpha(160 - self.frames * 2)
            self.screen.blit(score_plus, ((self.figure_last_x * cell_size - 10 + self.start_x - cell_size),
                                     (self.figure_last_y * cell_size - 50 - self.frames / 2)))
            self.frames += 1
        else:
            self.frames = 0
            self.k = 0

    def restart(self):
        self.game = True
        self.field = [[1] * 4 + [0] * (self.width - 6) + [1] * 4] * 2 + \
                     [([1] + [0] * self.width + [1]) for i in range(self.height)] + [[1] * (self.width + 2)]
        self.lines = 0
        self.score = 0


class Figure:
    def __init__(self, x, y, form, start_x=cell_size, start_y=cell_size):
        self.x = x
        self.y = y
        self.press_down = False
        self.start_x, self.start_y = start_x, start_y
        self.figure = form
        self.next_figure = self.new_figure()
        self.auto_down_speed = 1000

    def draw(self, screen, add):
        for i in range(len(self.figure)):
            for j in range(len(self.figure[i])):
                if self.figure[i][j] and (((self.y + j - 1) * cell_size) > 0):
                    pygame.draw.rect(screen,
                                     BLACK,
                                     [self.start_x + int((self.x + i - 0.65) * cell_size) + add,
                                      self.start_y + int((self.y + j - 1.65) * cell_size),
                                      cell_size - int(cell_size * 0.7),
                                      cell_size - int(cell_size * 0.7)])
                    pygame.draw.lines(screen, BLACK, 1, [(self.start_x + (self.x + i - 1) * cell_size + 1 + add,
                                                          self.start_y + (self.y + j - 2) * cell_size + 1),
                                                         (self.start_x + (self.x + i - 1) * cell_size + 1 + add,
                                                          self.start_y + (self.y + j - 1) * cell_size - 3),
                                                         (self.start_x + (self.x + i) * cell_size - 3 + add,
                                                          self.start_y + (self.y + j - 1) * cell_size - 3),
                                                         (self.start_x + (self.x + i) * cell_size - 3 + add,
                                                          self.start_y + (self.y + j - 2) * cell_size + 1)], 4)

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def can_move(self, field, side):
        new_x = self.x
        new_y = self.y
        self.auto_down_speed = int(0.66 ** (1 + field.score // divider) * 1515)
        if side == "d":
            new_y += 1
        elif side == "l":
            new_x -= 1
        elif side == "r":
            new_x += 1

        for i in range(len(self.figure)):
            for j in range(len(self.figure[i])):
                if self.figure[i][j] and field.field[new_y + j][new_x + i]:
                    return False
        return True

    def rotate(self, n=1):
        for i in range(n):
            self.figure = list(zip(*reversed(self.figure)))

    def can_rotate(self, field):
        new_form = list(zip(*reversed(self.figure)))
        for i in range(len(new_form)):
            for j in range(len(new_form[i])):
                if new_form[i][j] and field.field[self.y + j][self.x + i]:
                    return False
        return True

    def game_over(self, field):
        global PAUSE
        for i in range(len(self.figure)):
            for j in range(len(self.figure[i])):
                if self.figure[i][j] and field.field[self.y + j][self.x + i]:
                    field.game = False
                    PAUSE = True

    def new_figure(self):
        self.next_figure = random.choice([O, L, J, T, I, Z, S])
        for i in range(random.randint(1, 4)):
            self.next_figure = list(zip(*reversed(self.next_figure)))
        return self.next_figure

    def move_figure(self, field, figure):
        if self.can_move(field, "d"):
            self.move_down()
        else:
            field.figure_last_x = figure.x
            field.add_figure(figure)
            field.check_line()
            figure.figure = figure.next_figure
            figure.x = WIDTH // 2 - 1
            figure.y = 0
            figure.new_figure()
            figure.game_over(field)

    def restart(self):
        self.auto_down_speed = 1000
        self.x = 4
        self.y = 0
        self.figure = self.new_figure()


class GameWindow:
    def __init__(self, screen, cell_size, field, figure, AUTODOWN):
        self.screen = screen
        self.cell_size = cell_size
        self.field = field
        self.menu_left_line = (WIDTH + 4) * self.cell_size + field.start_x - self.cell_size
        self.score_print = '000000'
        self.score_sum = pygame.font.SysFont(font, self.cell_size, 1).render(self.score_print, 1, GREEN)
        self.speed = 1
        self.AUTODOWN = AUTODOWN
        self.figure = figure

    def draw_window(self):
        self.speed = 1 + self.field.score // divider
        self.score_print = ('{:6d}'.format(self.field.score))
        self.score_sum = pygame.font.SysFont(font, self.cell_size, 1).render(self.score_print, 1, GREEN)
        for i in range(HEIGHT):
            self.screen.blit(pygame.font.SysFont(font, int(self.cell_size * 0.7), True)
                        .render((str((HEIGHT - i))), 1, (200, 100, 100)),
                             (3 + self.field.start_x - self.cell_size, self.cell_size * (i + 1)))
            self.screen.blit(pygame.font.SysFont(font, int(self.cell_size * 0.7), True)
                        .render(("+" + str((HEIGHT - i - 1) * 25)), 1, (200, 100, 100)),
                             ((WIDTH + 1) * self.cell_size + 3 + self.field.start_x - self.cell_size, self.cell_size * (i + 1)))
        self.screen.blit(pygame.font.SysFont(font, self.cell_size, True)
                    .render("score:", 1, GREEN), (self.menu_left_line, self.cell_size))
        self.screen.blit(self.score_sum, (self.menu_left_line, self.cell_size * 2))
        self.screen.blit(pygame.font.SysFont(font, self.cell_size, True)
                    .render("next figure", 1, GREEN), (self.menu_left_line, self.cell_size * 3))
        self.screen.blit(pygame.font.SysFont(font, self.cell_size, True)
                    .render("lines:", 1, GREEN), (self.menu_left_line, self.cell_size * 9))
        self.screen.blit(pygame.font.SysFont(font, self.cell_size, True)
                    .render(str(self.field.lines), 1, GREEN), (self.menu_left_line, self.cell_size * 10))
        self.screen.blit(pygame.font.SysFont(font, self.cell_size, True)
                    .render("level:", 1, GREEN), (self.menu_left_line, self.cell_size * 11))
        self.screen.blit(pygame.font.SysFont(font, self.cell_size, True)
                    .render(str(self.speed), 1, GREEN), (self.menu_left_line, self.cell_size * 12))

    def draw_menu(self, mouse, click):
        global PAUSE
        global done

        b0x1 = cell_size * 3 + self.field.start_x - cell_size
        b0x2 = cell_size * (WIDTH - 4)
        b0y1 = cell_size * 3
        b0y2 = cell_size * 2
        if PAUSE and self.field.game:
            pygame.draw.rect(self.screen, (0, 100, 200), (b0x1, b0y1, b0x2, b0y2))
            self.screen.blit(pygame.font.SysFont(font, self.cell_size, True).render("Continue", 1, (0, 0, 100)),
                        (b0x1 + WIDTH / 8 * self.cell_size, b0y1 + self.cell_size / 2))
            if (b0x1 + b0x2) > mouse[0] > b0x1 and (b0y1 + b0y2) > mouse[1] > b0y1 and click[0]:
                PAUSE = False

        b1x1 = self.cell_size * 3 + self.field.start_x - cell_size
        b1x2 = self.cell_size * (WIDTH - 4)
        b1y1 = self.cell_size * 6
        b1y2 = self.cell_size * 2
        pygame.draw.rect(self.screen, (0, 100, 200), (b1x1, b1y1, b1x2, b1y2))
        self.screen.blit(pygame.font.SysFont(font, self.cell_size, True).render(
            "Start" if PAUSE and not self.field.game else "Restart", 1, (0, 0, 100)),
            (b1x1 + WIDTH / 6 * self.cell_size, b1y1 + self.cell_size / 2))
        b2x1 = self.cell_size * 3 + self.field.start_x - cell_size
        b2x2 = self.cell_size * (WIDTH - 4)
        b2y1 = self.cell_size * 9
        b2y2 = self.cell_size * 2
        pygame.draw.rect(self.screen, (0, 100, 200), (b2x1, b2y1, b2x2, b2y2))
        self.screen.blit(pygame.font.SysFont(font, self.cell_size, True).render("EXIT", 1, (0, 0, 100)),
                    (b2x1 + WIDTH / 5 * self.cell_size, b2y1 + self.cell_size / 2))

        if (b1x1 + b1x2) > mouse[0] > b1x1 and (b1y1 + b1y2) > mouse[1] > b1y1 and click[0]:
            PAUSE = False
            self.field.restart()
            self.figure.restart()
            pygame.time.set_timer(self.AUTODOWN, self.figure.auto_down_speed)

            print("Pause/Start works")
        elif (b2x1 + b2x2) > mouse[0] > b2x1 and (b2y1 + b2y2) > mouse[1] > b2y1 and click[0]:
            done = True

    def draw_next_figure(self):
        for i in range(len(self.figure.next_figure)):
            for j in range(len(self.figure.next_figure[i])):
                if self.figure.next_figure[i][j]:
                    pygame.draw.rect(self.screen, WHITE,
                                     [int(cell_size * (i + WIDTH + 4.35)) + self.field.start_x - cell_size,
                                      int((j + 4.85) * cell_size),
                                      int(cell_size * 0.3), int(cell_size * 0.3)])
                    pygame.draw.lines(self.screen, WHITE, 1,
                                      [(cell_size * (i + WIDTH + 4) + 1 + self.field.start_x - cell_size,
                                        (j + 4.5) * cell_size + 1),
                                       (cell_size * (i + WIDTH + 4) + 1 + self.field.start_x - cell_size,
                                        (j + 5.5) * cell_size - 3),
                                       (cell_size * (i + WIDTH + 5) - 3 + self.field.start_x - cell_size,
                                        (j + 5.5) * cell_size - 3),
                                       (cell_size * (i + WIDTH + 5) - 3 + self.field.start_x - cell_size,
                                        (j + 4.5) * cell_size + 1)], 4)

    def key_press(self, event_list, up, down, left, right):
        global PAUSE
        global done
        for event in event_list:
            if event.type == pygame.QUIT:
                done = True
            elif not PAUSE and event.type == pygame.KEYDOWN:
                if event.key == down:
                    if self.figure.auto_down_speed > 100:
                        pygame.time.set_timer(self.AUTODOWN, 50)
                    self.figure.move_figure(self.field, self.figure)
                elif event.key == left and self.figure.can_move(self.field, "l"):
                    self.figure.move_left()
                elif event.key == right and self.figure.can_move(self.field, "r"):
                    self.figure.move_right()
                elif event.key == up and self.figure.can_rotate(self.field):
                    self.figure.rotate()
            elif PAUSE:
                pass
            elif event.type == pygame.KEYUP:
                if event.key == down:
                    pygame.time.set_timer(self.AUTODOWN, self.figure.auto_down_speed)
            elif event.type == self.AUTODOWN:
                self.figure.move_figure(self.field, self.figure)


def main(cell_size):
    global PAUSE
    global done
    pygame.init()

    size = (800, 600)
    # size = (cell_size * (WIDTH + 9), cell_size * (HEIGHT + 2))
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    done = False

    field = Field(WIDTH, HEIGHT, screen, cell_size, cell_size)
    field_2 = Field(WIDTH, HEIGHT, screen, 400, cell_size)

    figure = Figure(WIDTH // 2 - 1, 0, random.choice([O, L, J, T, I, Z, S]), cell_size, cell_size)
    figure_2 = Figure(WIDTH // 2 - 1, 0, random.choice([O, L, J, T, I, Z, S]), 400, cell_size)

    game_1 = GameWindow(screen, cell_size, field, figure, AUTODOWN_1)
    game_2 = GameWindow(screen, cell_size, field_2, figure_2, AUTODOWN_2)

    clock = pygame.time.Clock()

    while not done:
        screen.fill((0, 255, 0))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        game_1.draw_window()
        game_2.draw_window()

        event_list = pygame.event.get()

        if field.game:
            field.draw()
            figure.draw(screen, 0)
            field.fly_points()
            game_1.draw_next_figure()
            game_1.key_press(event_list, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

        if field_2.game:
            field_2.draw()
            figure_2.draw(screen, 0)
            field_2.fly_points()
            game_2.draw_next_figure()
            game_2.key_press(event_list, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

        for event in event_list:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE) and (
                    field.game or field_2.game):
                if PAUSE:
                    PAUSE = False
                else:
                    PAUSE = True

        if PAUSE:
            game_1.draw_menu(mouse, click)
            game_2.draw_menu(mouse, click)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main(cell_size)
