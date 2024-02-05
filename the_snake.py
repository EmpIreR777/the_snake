import sys
from random import choice, randint

import pygame as pg


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Регулировка скорости:
SPEED_CONTROL = 7

# Скорость движения змейки:
SPEED = SPEED_CONTROL

# Центр поля:
CENTRE_POINT = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс. Cодержит общие атрибуты и метод отрисовки."""

    def __init__(self, body_color=None, position=CENTRE_POINT):
        self.position = position
        self.body_color = body_color

    def randomize_position(self, boom=[CENTRE_POINT]):
        """Устанавливаем случайную значение яблоку и стенке."""
        while self.position is None or self.position in boom:
            self.position = (
                (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE),
            )

    def draw(self, surface):
        """Метод для отрисовки объектов."""
        raise NotImplementedError(f'Определите draw в \
                                  {self.__class__.__name__}.')

    def rect(self, surface, position, border_color=BORDER_COLOR,
             border_width=1, frame_loading=1):
        """Задаём цвет камня и яблока."""
        rect = pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, border_color, rect, border_width, frame_loading)
        return rect


class Stone(GameObject):
    """Преграда на поле."""

    def __init__(self, boom=[CENTRE_POINT]):
        super().__init__(body_color=BORDER_COLOR, position=None)
        self.randomize_position(boom)

    def draw(self, surface):
        """Отрисовка Камня."""
        self.rect(surface, self.position, border_width=1)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, boom=[CENTRE_POINT]):
        super().__init__(body_color=APPLE_COLOR, position=None)
        self.randomize_position(boom)

    def draw(self, surface):
        """Отрисовка Яблока."""
        self.rect(surface, self.position, BORDER_COLOR, 2, 4)


class Snake(GameObject):
    """Тут описывается логика змейки,движение на игровом поле и отрисовка."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.positions = [self.position]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки и логика прохождения змейки через стены."""
        head_x, head_y = self.get_head_position()

        dx, dy = self.direction
        new_x = head_x + dx * GRID_SIZE
        new_y = head_y + dy * GRID_SIZE

        if new_x == SCREEN_WIDTH:
            new_x = -GRID_SIZE
        elif new_x == -GRID_SIZE:
            new_x = SCREEN_WIDTH - GRID_SIZE
        if new_y == SCREEN_HEIGHT:
            new_y = -GRID_SIZE
        elif new_y == -GRID_SIZE:
            new_y = SCREEN_HEIGHT - GRID_SIZE

        new_point = (new_x, new_y)

        self.positions.insert(0, new_point)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            self.rect(surface, position, BOARD_BACKGROUND_COLOR, 3)

        # Отрисовка головы змейки
        self.rect(surface, self.positions[0], BORDER_COLOR, 1, 1)

        # Затирание последнего сегмента
        if self.last:
            self.rect(surface, self.last, BOARD_BACKGROUND_COLOR, 10, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Логика подключения клавиатуры."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


snake = Snake()


def draw_apple(boom):
    """Отрисовка яблока."""
    apple = Apple(boom)
    apple.draw(screen)
    return apple


def draw_stone(boom):
    """Отрисовка стены."""
    stone = Stone(boom)
    stone.draw(screen)
    return stone


def main():
    """Основная логика игры Змейка."""
    pg.init()
    snake = Snake()
    snake.draw(screen)
    apple = draw_apple(snake.positions)
    stone = draw_stone(snake.positions + [apple.position])
    stones = [stone]

    global SPEED

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        for i in stones:
            if i.position == snake.get_head_position():
                SPEED = SPEED_CONTROL
                snake.reset()
                apple = draw_apple(snake.positions)
                stone = draw_stone(snake.positions + [apple.position])
                stones = [stone]

        stones_positions = []
        for i in stones:
            stones_positions.append(i.position)

        if apple.position == snake.get_head_position():
            snake.length += 1
            SPEED += 0.3
            apple = draw_apple(snake.positions + stones_positions)
            if randint(0, 3) == 1:
                stone = draw_stone(
                    snake.positions + [apple.position] + stones_positions
                )
                stones.append(stone)
                stones_positions.append(stone.position)

        if snake.get_head_position() in snake.positions[1:]:
            SPEED = SPEED_CONTROL
            snake.reset()
            apple = draw_apple(snake.positions)
            stone = draw_stone(snake.positions + [apple.position])
            stones = [stone]

        snake.draw(screen)

        pg.display.update()


if __name__ == '__main__':
    main()
