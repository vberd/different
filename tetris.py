import pygame
from random import choice, randint


class Field:
    def __init__(self, start_y, hi_score=0):
        self.field = [[0] * (width + 2) for i in range(height + 2)]
        self.score = self.score_plus = self.score_up = 0
        self.hiscore = hi_score
        self.k = self.lines = 0
        self.start_x, self.start_y = cell_size, start_y
        self.game = False
        self.figure_last_x = self.figure_last_y = 0

    def draw(self):
        for i in range(2, height + 2):
            for j in range(1, width + 1):
                if self.field[i][j]:
                    GameWindow.draw_cell('red', self.start_y, 0, 0, i, j)

    def add_figure(self, figure):
        for i in range(len(figure.figure)):
            for j in range(len(figure.figure[i])):
                if figure.figure[i][j]:
                    self.field[i + figure.x][j + figure.y] = 1

    def check_line(self):
        self.score_up = 0
        self.k = 0
        for i in range(2, height + 2):
            if 0 not in self.field[i]:
                self.field.pop(i)
                self.field.insert(2, ([1] + [0] * width + [1]))
                self.k += 1
                self.lines += 1
                self.figure_last_x = i
                self.score_plus = 100 * (self.k ** 2 - (self.k - 1) ** 2) + 25 * (height - i + 1)
                self.score_up += self.score_plus
                self.score += self.score_plus
                self.hiscore = max(self.hiscore, self.score)

    def restart(self):
        self.game = True
        self.field = [[1] * (width // 2 - 1) + [0] * 4 + [1] * (width // 2 - 1 + width % 2)] * 2 + \
                     [([1] + [0] * width + [1]) for i in range(height)] + \
                     [[1] * (width + 2)]
        self.lines = self.score = 0


class Figure:
    def __init__(self, start_y, field):
        self.x = 0
        self.y = width // 2 - 1
        self.press_down = False
        self.start_x, self.start_y = cell_size, start_y
        self.figure = ''
        self.next_figure = self.new_figure()
        self.field = field
        self.auto_down_speed = 1000

    def draw(self):
        for i in range(len(self.figure)):
            for j in range(len(self.figure[i])):
                if self.figure[i][j] and (((self.x + i - 1) * cell_size) > 0):
                    GameWindow.draw_cell('black', self.start_y, self.x, self.y, i, j)

    def can_move(self, side):
        new_x = self.x
        new_y = self.y
        if side == "d":
            new_x += 1
        elif side == "l":
            new_y -= 1
        elif side == "r":
            new_y += 1
        for i in range(len(self.figure)):
            for j in range(len(self.figure[i])):
                if self.figure[i][j] and self.field.field[new_x + i][new_y + j]:
                    return False
        return True

    def move_down(self):
        self.x += 1

    def move_left(self):
        self.y -= 1

    def move_right(self):
        self.y += 1

    def rotate(self, n=1):
        for i in range(n):
            self.figure = list(zip(*reversed(self.figure)))

    def can_rotate(self):
        new_form = list(zip(*reversed(self.figure)))
        for i in range(len(new_form)):
            for j in range(len(new_form[i])):
                if new_form[i][j] and self.field.field[self.x + i][self.y + j]:
                    return False
        return True

    def new_figure(self):
        self.next_figure = choice(list(figures.values()))
        for i in range(randint(1, 4)):
            self.next_figure = list(zip(*reversed(self.next_figure)))
        return self.next_figure

    def move_figure(self, game):
        if not game.pressed_button:
            self.auto_down_speed = int(0.66 ** (self.field.score // div) * 1000)
            pygame.time.set_timer(game.AUTODOWN, self.auto_down_speed)
        if self.can_move("d"):
            self.move_down()
        else:
            self.field.figure_last_y = self.y
            self.field.add_figure(self)
            self.field.check_line()
            self.figure = self.next_figure
            self.x = 0
            self.y = width // 2 - 1
            self.new_figure()
            self.game_over()

    def game_over(self):
        global PAUSE, n_t
        for i in range(len(self.figure)):
            for j in range(len(self.figure[i])):
                if self.figure[i][j] and self.field.field[self.x + i][self.y + j]:
                    self.field.game = False
                    PAUSE = True
                    n_t = 0

    def restart(self):
        self.auto_down_speed = 1000
        self.x = 0
        self.y = width // 2 - 1
        self.figure = self.new_figure()


class GameWindow:
    def __init__(self, field, figure, autodown):
        self.field = field
        self.menu_left_line = int((width + 2.5) * cell_size + field.start_y)
        self.score_sum = pygame.font.SysFont(font, cell_size, 1).render('0' * 6, 1, colors['green'])
        self.speed = 1
        self.AUTODOWN = autodown
        self.figure = figure
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.bind_key_up_c = self.bind_key_down_c = self.bind_key_left_c = self.bind_key_right_c = colors['keybind_inactive']
        self.bind_key_up = self.bind_key_down = self.bind_key_left = self.bind_key_right = False
        self.pressed_button = False
        self.blink_start = 150
        self.blink_step = 2
        self.frames = 0

    def draw_window(self):
        self.speed = 1 + self.field.score // div
        pygame.draw.rect(screen, (0, 200, 100), (self.field.start_y, self.field.start_x, width * cell_size, height * cell_size))
        for i in range(height):
            screen.blit(pygame.font.SysFont(font, int(cell_size * 0.7), True)
                        .render((str((height - i))), 1, (200, 100, 100)),
                        (3 + self.field.start_y - cell_size, cell_size * (i + 1)))
            screen.blit(pygame.font.SysFont(font, int(cell_size * 0.7), True)
                        .render(("+" + str((height - i - 1) * 25)), 1, (200, 100, 100)),
                        ((width + 1) * cell_size + 3 + self.field.start_y - cell_size, cell_size * (i + 1)))
        if height > 14:
            font_size = int(cell_size * 1)
            screen.blit(pygame.font.SysFont(font, font_size, True).
                        render("next figure", 1, colors['green']), (self.menu_left_line, int(cell_size * (5 - 0.25))))
            labels = ['hi-score:', 'level:']
            numbers = [0, 2, 3, 4, 5.9, 9.75, 3, 0, 10.75, 3]
        else:
            font_size = int(cell_size * 0.66)
            labels = ['hiscore:', 'lv:']
            numbers = [2.25, 1, 1.5, 1.5, 2, 6, 2, 2.75, 6, 3.75]
        self.score_sum = pygame.font.SysFont(font, font_size, 1).\
            render('{:06d}'.format(self.field.score), 1, colors['green'])
        hiscore = pygame.font.SysFont(font, font_size, 1).\
            render('{:06d}'.format(self.field.hiscore), 1, colors['green'])
        screen.blit(pygame.font.SysFont(font, font_size, True).render("score:", 1, colors['green']),
                    (self.menu_left_line, int(cell_size * (1 - 0.25))))
        screen.blit(self.score_sum, (self.menu_left_line + int(cell_size * numbers[0]),
                                     int(cell_size * (numbers[1] - 0.25))))
        screen.blit(pygame.font.SysFont(font, font_size, True).render(labels[0], 1, colors['green']),
                    (self.menu_left_line, int(cell_size * (numbers[2] - 0.25))))
        screen.blit(hiscore, (self.menu_left_line + int(cell_size * numbers[0]),
                              int(cell_size * (numbers[3] - 0.25))))
        pygame.draw.rect(screen, (0, 200, 100), (self.menu_left_line, int(cell_size * numbers[4]),
                                                 cell_size * 4, cell_size * 4))
        screen.blit(pygame.font.SysFont(font, font_size, True).render("lines:", 1, colors['green']),
                    (self.menu_left_line, int(cell_size * numbers[5])))
        screen.blit(pygame.font.SysFont(font, font_size, True).render(str(self.field.lines), 1, colors['green']),
                    (self.menu_left_line + int(cell_size * numbers[6]), int(cell_size * numbers[5])))
        screen.blit(pygame.font.SysFont(font, font_size, True).render(labels[1], 1, colors['green']),
                    (self.menu_left_line + int(cell_size * numbers[7]), int(cell_size * numbers[8])))
        screen.blit(pygame.font.SysFont(font, font_size, True).render(str(self.speed), 1, colors['green']),
                    (self.menu_left_line + int(cell_size * numbers[9]), int(cell_size * numbers[8])))

    def button_color(self, button, mouse):
        if button.collidepoint(mouse[0], mouse[1]):
            return colors['menu_active']
        return colors['menu_inactive']

    def draw_menu(self, mouse, click):
        global PAUSE, done

        b0x1 = (cell_size * 2 + self.field.start_y) if width > 7 else self.field.start_y
        b0x2 = (cell_size * (width - 4)) if width > 7 else (width * cell_size)
        b0y1 = (cell_size * 3) if height > 9 else cell_size
        b1y1 = (cell_size * 6) if height > 9 else (cell_size * 3)
        b2y1 = (cell_size * 9) if height > 9 else (cell_size * 5)
        b0y2 = cell_size * 2

        button_0 = pygame.Rect(b0x1, b0y1, b0x2, b0y2)
        button_1 = pygame.Rect(b0x1, b1y1, b0x2, b0y2)
        button_2 = pygame.Rect(b0x1, b2y1, b0x2, b0y2)

        if PAUSE and self.field.game:
            pygame.draw.rect(screen, self.button_color(button_0, mouse), button_0)
            screen.blit(pygame.font.SysFont(font, cell_size, True).render("Continue", 1, (0, 0, 100)),
                        (int(self.field.start_y + width / 2 * cell_size - cell_size * 1.75), int(b0y1 + cell_size / 2)))
            if button_0.collidepoint(mouse[0], mouse[1]) and click[0]:
                PAUSE = False
                pygame.time.set_timer(self.AUTODOWN, self.figure.auto_down_speed)
                self.pressed_button = False

        pygame.draw.rect(screen, self.button_color(button_1, mouse), button_1)
        screen.blit(pygame.font.SysFont(font, cell_size, True).render(" Start " if not self.field.game else "Restart", 1, (0, 0, 100)),
                    (int(self.field.start_y + width / 2 * cell_size - cell_size * 1.25), int(b1y1 + cell_size / 2)))

        pygame.draw.rect(screen, self.button_color(button_2, mouse), button_2)
        screen.blit(pygame.font.SysFont(font, cell_size, True).render("EXIT", 1, (0, 0, 100)),
                    (int(self.field.start_y + width / 2 * cell_size - cell_size * 0.9), int(b2y1 + cell_size / 2)))

        if button_1.collidepoint(mouse[0], mouse[1]) and click[0]:
            if not self.field.game:
                PAUSE = False
            self.field.restart()
            self.figure.restart()
            pygame.time.set_timer(self.AUTODOWN, self.figure.auto_down_speed)
        elif button_2.collidepoint(mouse[0], mouse[1]) and click[0]:
            done = True

    @staticmethod
    def draw_cell(color, start_y, x, y, i, j):
        pygame.draw.rect(screen, colors[color],
                         [int((y + j - 0.65) * cell_size) + start_y,
                          int((x + i - 0.65) * cell_size),
                          int(cell_size * 0.3), int(cell_size * 0.3)])
        pygame.draw.lines(screen, colors[color], 1,
                          [((y + j - 1) * cell_size + cell_size_1 + start_y,
                           (x + i - 1) * cell_size + cell_size_1),
                           ((y + j + 0) * cell_size - cell_size_3 + start_y,
                           (x + i - 1) * cell_size + cell_size_1),
                           ((y + j + 0) * cell_size - cell_size_3 + start_y,
                           (x + i) * cell_size - cell_size_3),
                           ((y + j - 1) * cell_size + cell_size_1 + start_y,
                           (x + i) * cell_size - cell_size_3)],
                          int(cell_size / 5))

    def draw_next_figure(self):
        for i in range(len(self.figure.next_figure)):
            for j in range(len(self.figure.next_figure[i])):
                if self.figure.next_figure[i][j]:
                    if height > 14:
                        start_x = 6.9

                    else:
                        start_x = 3
                    GameWindow.draw_cell('white', self.field.start_y, start_x, (width + 2.5) +
                                         self.field.start_x / cell_size, i, j)

    def key_press(self):
        global done

        for event in event_list:
            if event.type == pygame.QUIT:
                done = True
            elif not PAUSE and event.type == pygame.KEYDOWN:
                if event.key == self.down:
                    if self.figure.auto_down_speed > 100:
                        pygame.time.set_timer(self.AUTODOWN, 50)
                        self.pressed_button = True
                    self.figure.move_figure(self)
                elif event.key == self.left and self.figure.can_move("l"):
                    self.figure.move_left()
                elif event.key == self.right and self.figure.can_move("r"):
                    self.figure.move_right()
                elif event.key == self.up and self.figure.can_rotate():
                    self.figure.rotate()
            elif PAUSE:
                pass
            elif event.type == pygame.KEYUP:
                if event.key == self.down:
                    pygame.time.set_timer(self.AUTODOWN, self.figure.auto_down_speed)
                    self.pressed_button = False
            elif event.type == self.AUTODOWN:
                self.figure.move_figure(self)

    def notification(self, notification_times):
        global n_t
        if height > 14:
            not_y_pos = cell_size * 9
            not_times = notification_times

            if n_t < not_times:
                not_field = pygame.Rect(int(self.field.start_y + (width - 3) * cell_size - 2),
                                        int(not_y_pos + cell_size * 3 + 2), cell_size * 5, cell_size * 3)
                if self.blink_start > 200 or self.blink_start < 100:
                    self.blink_step *= -1
                    n_t += 1
                self.blink_start += self.blink_step
                not_blink_color = pygame.Color(100, self.blink_start, 100)

                pygame.draw.rect(screen, (0, 100, 100), not_field)
                screen.blit(pygame.font.SysFont(font, cell_size, True).render("You can", 1, not_blink_color),
                            (int(self.field.start_y + (width - 3) * cell_size), int(not_y_pos + cell_size * 3)))
                screen.blit(pygame.font.SysFont(font, cell_size, True).render("change   =>", 1, not_blink_color),
                            (int(self.field.start_y + (width - 3) * cell_size), int(not_y_pos + cell_size * 4)))
                screen.blit(pygame.font.SysFont(font, cell_size, True).render("the controls", 1, not_blink_color),
                            (int(self.field.start_y + (width - 3) * cell_size), int(not_y_pos + cell_size * 5)))
        else:
            pass

    def key_bind(self):
        global done

        if height > 14:
            numbers = [2, 12, 1, 0, 2, 0, 3]
        else:
            numbers = [1.25, 6.75, 0.75, 1.25, 0.5, 2.5, 0.5]

        b3x1 = int(cell_size * (width + 2.5) + self.field.start_y)
        b3x2 = int(cell_size * numbers[0])
        b3y1 = int(cell_size * numbers[1])
        b3y2 = int(cell_size * numbers[2])
        up_field = pygame.Rect(b3x1 + int(cell_size * numbers[3]), b3y1, b3x2, b3y2)
        down_field = pygame.Rect(b3x1 + int(cell_size * numbers[3]), b3y1 + cell_size, b3x2, b3y2)
        left_field = pygame.Rect(b3x1, b3y1 + int(cell_size * numbers[4]), b3x2, b3y2)
        right_field = pygame.Rect(b3x1 + int(cell_size * numbers[5]), b3y1 + int(cell_size * numbers[6]), b3x2, b3y2)

        if PAUSE:
            for event in event_list:
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if up_field.collidepoint(event.pos):
                        self.bind_key_up = not self.bind_key_up
                        self.bind_key_down = self.bind_key_left = self.bind_key_right = False
                    elif down_field.collidepoint(event.pos):
                        self.bind_key_up = self.bind_key_left = self.bind_key_right = False
                        self.bind_key_down = not self.bind_key_down
                    elif left_field.collidepoint(event.pos):
                        self.bind_key_up = self.bind_key_down = self.bind_key_right = False
                        self.bind_key_left = not self.bind_key_left
                    elif right_field.collidepoint(event.pos):
                        self.bind_key_up = self.bind_key_down = self.bind_key_left = False
                        self.bind_key_right = not self.bind_key_right
                    else:
                        self.bind_key_up = self.bind_key_down = self.bind_key_left = self.bind_key_right = False
                    self.bind_key_up_c = colors['keybind_active'] if self.bind_key_up else colors['keybind_inactive']
                    self.bind_key_down_c = colors['keybind_active'] if self.bind_key_down else colors['keybind_inactive']
                    self.bind_key_left_c = colors['keybind_active'] if self.bind_key_left else colors['keybind_inactive']
                    self.bind_key_right_c = colors['keybind_active'] if self.bind_key_right else colors['keybind_inactive']
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.bind_key_up = self.bind_key_down = self.bind_key_left = self.bind_key_right = False
                        self.bind_key_up_c = self.bind_key_down_c = self.bind_key_left_c = self.bind_key_right_c = colors['keybind_inactive']
                    if self.bind_key_up:
                        self.up = event.key
                    elif self.bind_key_down:
                        self.down = event.key
                    elif self.bind_key_left:
                        self.left = event.key
                    elif self.bind_key_right:
                        self.right = event.key

        pygame.draw.rect(screen, self.bind_key_up_c, up_field, 2)
        pygame.draw.rect(screen, self.bind_key_down_c, down_field, 2)
        pygame.draw.rect(screen, self.bind_key_left_c, left_field, 2)
        pygame.draw.rect(screen, self.bind_key_right_c, right_field, 2)

        if height > 14:
            screen.blit(pygame.font.SysFont(font, int(cell_size * 0.75), True).render("Up", 1, self.bind_key_up_c),
                        (b3x1 + int(2.5 * cell_size), b3y1))
            screen.blit(pygame.font.SysFont(font, int(cell_size * 0.75), True).render("Down", 1, self.bind_key_down_c),
                        (b3x1 + int(2.5 * cell_size), b3y1 + cell_size))
            screen.blit(pygame.font.SysFont(font, int(cell_size * 0.75), True).render("Left", 1, self.bind_key_left_c),
                        (b3x1 + int(2.5 * cell_size), b3y1 + cell_size * 2))
            screen.blit(pygame.font.SysFont(font, int(cell_size * 0.75), True).render("Right", 1, self.bind_key_right_c),
                        (b3x1 + int(2.5 * cell_size), b3y1 + cell_size * 3))
            numbers = [0.75, 0.1, 0.1, 2, 0.1, 3]
        else:
            numbers = [0.6, 1.4, 0.15, 0.5, 2.65, 0.5]
        screen.blit(pygame.font.SysFont(font, int(cell_size * numbers[0]), True).
                    render('{:.4}'.format(pygame.key.name(self.up)), 1, self.bind_key_up_c),
                    (b3x1 + int(cell_size * numbers[1]), b3y1))
        screen.blit(pygame.font.SysFont(font, int(cell_size * numbers[0]), True).
                    render('{:.4}'.format(pygame.key.name(self.down)), 1, self.bind_key_down_c),
                    (b3x1 + int(cell_size * numbers[1]), b3y1 + cell_size))
        screen.blit(pygame.font.SysFont(font, int(cell_size * numbers[0]), True).
                    render('{:.4}'.format(pygame.key.name(self.left)), 1, self.bind_key_left_c),
                    (b3x1 + int(cell_size * numbers[2]), b3y1 + int(cell_size * numbers[3])))
        screen.blit(pygame.font.SysFont(font, int(cell_size * numbers[0]), True).
                    render('{:.4}'.format(pygame.key.name(self.right)), 1, self.bind_key_right_c),
                    (b3x1 + int(cell_size * numbers[4]), b3y1 + int(cell_size * numbers[5])))

    def fly_points(self):
        if self.field.k and self.frames < 80 and self.field.score_up:
            score_plus_fly = pygame.font.SysFont(font, int(cell_size * (1 + 1 / 4 * self.field.k))) \
                .render(("+" + str(self.field.score_up)), 0, (100, 100, 100, 10))
            score_plus_fly.set_alpha(160 - self.frames * 2)
            screen.blit(score_plus_fly, ((self.field.figure_last_y * cell_size + self.figure.start_y),
                                         ((self.field.figure_last_x - 2) * cell_size - self.frames / 2)))
            self.frames += 1
        else:
            self.frames = self.field.k = self.field.score_up = 0


def main(players=1, width_field=10, height_field=15, cell_size_pixels=20, divider=300):
    global PAUSE, done, screen
    global event_list
    global colors, figures, font
    global width, height
    global cell_size, cell_size_1, cell_size_3, div
    global n_t

    PAUSE = True
    done = False
    width, height = width_field, height_field
    cell_size = cell_size_pixels
    cell_size_3 = int(cell_size / 8)
    cell_size_1 = int(cell_size / 16)
    div = divider
    n_t = 0
    font = "Arial"

    colors = {'black': pygame.Color(0, 0, 0),
              'white': pygame.Color(255, 255, 255),
              'green': pygame.Color(100, 100, 100),
              'red': pygame.Color(255, 100, 0),
              'keybind_inactive': pygame.Color(100, 100, 0),
              'keybind_active': pygame.Color(200, 0, 0),
              'menu_inactive': pygame.Color(0, 100, 200),
              'menu_active': pygame.Color(0, 200, 200)}

    figures = {'O': [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
               'L': [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
               'J': [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
               'T': [[0, 1, 0], [1, 1, 0], [0, 1, 0]],
               'I': [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
               'Z': [[1, 0], [1, 1], [0, 1]],
               'S': [[0, 1], [1, 1], [1, 0]]}

    pygame.init()

    size = (cell_size * (width + 9) * players, cell_size * (height + 2))
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    players_dic = {}
    for player in range(players):
        players_dic[player] = {'field': Field(cell_size + cell_size * (width + 9) * player),
                               'figure': '',
                               'game': ''}
        players_dic[player]['figure'] = Figure((cell_size + cell_size * (width + 9) * player),
                                               players_dic[player]['field'])
        players_dic[player]['game'] = GameWindow(players_dic[player]['field'],
                                                 players_dic[player]['figure'],
                                                 (pygame.USEREVENT + player))

    while not done:
        screen.fill((0, 255, 0))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        event_list = pygame.event.get()

        for player_number in range(players):
            players_dic[player_number]['game'].draw_window()
            players_dic[player_number]['game'].key_bind()

            players_dic[player_number]['field'].draw()
            if players_dic[player_number]['field'].game:
                players_dic[player_number]['figure'].draw()
                players_dic[player_number]['game'].fly_points()
                players_dic[player_number]['game'].draw_next_figure()
                players_dic[player_number]['game'].key_press()

            if not players_dic[player_number]['field'].game or PAUSE:
                players_dic[player_number]['game'].draw_menu(mouse, click)
                players_dic[player_number]['game'].notification(4)

        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if PAUSE:
                    PAUSE = False
                    for player_number in range(players):
                        pygame.time.set_timer(players_dic[player_number]['game'].AUTODOWN,
                                              players_dic[player_number]['figure'].auto_down_speed)
                        players_dic[player_number]['game'].pressed_button = False
                else:
                    PAUSE = True
                    n_t = 0

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


main(3, 10, 15, 20, 1000)
