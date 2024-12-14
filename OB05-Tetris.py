
# Пример реализации игры Тетрис:


import pygame
import random

# Константы
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Цвета
COLORS = [
    (0, 0, 0),  # Черный (фон)
    (255, 0, 0),  # Красный
    (0, 255, 0),  # Зеленый
    (0, 0, 255),  # Синий
    (255, 255, 0),  # Желтый
    (255, 165, 0),  # Оранжевый
    (128, 0, 128),  # Пурпурный
    (0, 255, 255)   # Голубой
]

# Классы фигур
class Tetrimino:
    shapes = [
        [[1, 1, 1, 1]],  # I
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 0], [0, 1, 1]],  # Z
        [[0, 1, 1], [1, 1, 0]],  # S
        [[1, 1], [1, 1]],  # O
        [[1, 1, 1], [1, 0, 0]],  # L
        [[1, 1, 1], [0, 0, 1]]   # J
    ]

    def __init__(self):
        self.shape = random.choice(self.shapes)
        self.color = random.randint(1, len(COLORS) - 1)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def clear_rows(self):
        cleared_rows = 0
        for i in range(len(self.grid) - 1, -1, -1):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                cleared_rows += 1
        return cleared_rows

    def add_tetrimino(self, tetrimino):
        for i, row in enumerate(tetrimino.shape):
            for j, value in enumerate(row):
                if value:
                    self.grid[tetrimino.y + i][tetrimino.x + j] = tetrimino.color

    def is_valid_position(self, tetrimino):
        for i, row in enumerate(tetrimino.shape):
            for j, value in enumerate(row):
                if value:
                    if (tetrimino.x + j < 0 or tetrimino.x + j >= GRID_WIDTH or
                        tetrimino.y + i >= GRID_HEIGHT or
                        self.grid[tetrimino.y + i][tetrimino.x + j] != 0):
                        return False
        return True

class TetrisGame:
    def __init__(self):
        self.grid = Grid()
        self.current_tetrimino = Tetrimino()
        self.score = 0
        self.game_over = False

    def drop_tetrimino(self):
        if not self.game_over:
            self.current_tetrimino.y += 1
            if not self.grid.is_valid_position(self.current_tetrimino):
                self.current_tetrimino.y -= 1
                self.grid.add_tetrimino(self.current_tetrimino)
                self.score += self.grid.clear_rows()
                self.current_tetrimino = Tetrimino()
                if not self.grid.is_valid_position(self.current_tetrimino):
                    self.game_over = True

    def draw(self, screen):
        for i, row in enumerate(self.grid.grid):
            for j, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, COLORS[value], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for i, row in enumerate(self.current_tetrimino.shape):
            for j, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, COLORS[self.current_tetrimino.color], ((self.current_tetrimino.x + j) * BLOCK_SIZE, (self.current_tetrimino.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = TetrisGame()
    fall_time = 0
    fall_speed = 500  # миллисекунды

    while True:
        fall_time += clock.get_time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.current_tetrimino.x -= 1
                    if not game.grid.is_valid_position(game.current_tetrimino):
                        game.current_tetrimino.x += 1
                elif event.key == pygame.K_RIGHT:
                    game.current_tetrimino.x += 1
                    if not game.grid.is_valid_position(game.current_tetrimino):
                        game.current_tetrimino.x -= 1
                elif event.key == pygame.K_DOWN:
                    game.drop_tetrimino()
                elif event.key == pygame.K_UP:
                    game.current_tetrimino.rotate()
                    if not game.grid.is_valid_position(game.current_tetrimino):
                        game.current_tetrimino.rotate()  # Возврат назад если не подходит

        if fall_time >= fall_speed:
            game.drop_tetrimino()
            fall_time = 0

        screen.fill(COLORS[0])
        game.draw(screen)

        if game.game_over:
            font = pygame.font.SysFont('Arial', 30)
            text = font.render('Game Over', True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()


### Объяснение кода:

# 1. **Константы и цвета**: Определяются размеры экрана, размеры блоков, цветовые схемы.
#
# 2. **Класс `Tetrimino`**: Описывает фигуры Тетриса, их вращение и начальные координаты.
#
# 3. **Класс `Grid`**: Управляет состоянием игрового поля, добавляет и проверяет позиции фигур, очищает заполненные ряды.
#
# 4. **Класс `TetrisGame`**: Основной класс игры, который объединяет логику управления фигурами, их падение и рисование на экране.
#
# 5. **Основная функция `main`**: Инициализация Pygame, игровой цикл, обрабатывающий события и обновляющий экран.
#
# ### Заключение:
# Этот код представляет собой базовую версию игры Тетрис. Вы можете расширить его, добавив больше функций, таких как уровни сложности, различные режимы игры, звуковые эффекты и т.д.