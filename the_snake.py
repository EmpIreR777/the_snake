from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

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

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 7

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    '''Базовый класс. Cодержит общие атрибуты и метод отрисовки игровых объектов.'''

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    '''Класс, описывающий яблоко и действия с ним.'''

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()
                
        # Устанавливаем случайную позицию яблока.
    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )
        return self.position

        # Задаём цвет яблока.
    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 2, 4)


class Snake(GameObject):
    '''Тут описывается логика змейки,движение на игровом поле и отрисовка'''

    # Атрибуты змейки.
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Обновляет направление движения змейки.
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Обновляет позицию змейки и логика прохождения змейки через стены.
    def move(self):
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

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

    # Метод draw класса Snake
    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, 3, 5)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    # Возвращает позицию головы змейки.
    def get_head_position(self):
        return self.positions[0]
    
    # Сбрасывает змейку в начальное состояние после столкновения.
    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)

# Логика подключения клавиатуры.
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

# Отрисовка яблока.
def draw_apple():
    apple = Apple()
    apple.draw(screen)
    return apple

# Основная логика игры Змейка.
def main():

    apple = draw_apple()

    snake = Snake()
    snake.draw(screen)
    global SPEED
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if apple.position == snake.get_head_position():
            snake.length += 1
            SPEED += 0.5
            print(SPEED)
            apple = draw_apple()

        if snake.get_head_position() in snake.positions[1:]:
            SPEED = 7
            snake.reset()
            apple = draw_apple()
        snake.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()