#Пример кода, который реализует игру Тетрис:
#
#
import pygame
import random

# Константы
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Цвета
COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'orange': (255, 165, 0),
    'black': (0, 0, 0),
}

# Фигуры
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(list(COLORS.values()))
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.score = 0

    def new_piece(self):
        return Piece(random.choice(SHAPES))

    def valid_move(self, dx, dy):
        for y, row in enumerate(self.current_piece.shape):
            for x, block in enumerate(row):
                if block:
                    new_x = self.current_piece.x + x + dx
                    new_y = self.current_piece.y + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or self.board[new_y][new_x]:
                        return False
        return True

    def freeze_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, block in enumerate(row):
                if block:
                    self.board[self.current_piece.y + y][self.current_piece.x + x] = 1
        self.clear_lines()

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * GRID_WIDTH)
        self.score += len(lines_to_clear)

    def move_piece(self, dx, dy):
        if self.valid_move(dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
        else:
            if dy > 0:  # если вниз, то фиксируем
                self.freeze_piece()
                self.current_piece = self.new_piece()
                if not self.valid_move(0, 0):
                    print("Game Over")

    def drop_piece(self):
        self.move_piece(0, 1)

    def draw(self, screen):
        for y, row in enumerate(self.board):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(screen, COLORS['blue'], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for y, row in enumerate(self.current_piece.shape):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + x) * BLOCK_SIZE, (self.current_piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.tetris = Tetris()

    def run(self):
        while True:
            self.screen.fill(COLORS['black'])
            self.tetris.drop_piece()
            self.tetris.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.tetris.move_piece(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.tetris.move_piece(1, 0)
                    if event.key == pygame.K_DOWN:
                        self.tetris.move_piece(0, 1)
                    if event.key == pygame.K_UP:
                        self.tetris.current_piece.rotate()

            pygame.display.flip()
            self.clock.tick(10)

if __name__ == "__main__":
    game = Game()
    game.run()
#```

### Объяснение структуры

# 1. **Класс `Piece`**: Представляет текущую фигуру. Содержит методы для вращения фигуры.
#
# 2. **Класс `Tetris`**: Логика игры. Содержит игровое поле, текущее состояние, проверяет допустимость движений, фиксирует фигуры на поле и очищает линии.
#
# 3. **Класс `Game`**: Управляет основным игровым циклом, обрабатывает события и прорисовывает все на экране.
#
# ### Применение принципов SOLID
#
# - **Single Responsibility Principle (SRP)**: Каждый класс имеет одну ответственность. `Piece` отвечает за фигуры, `Tetris` — за игровую логику, а `Game` — за управление игровым циклом.
#
# - **Open/Closed Principle (OCP)**: Логика игры может быть расширена, например, добавлением новых фигур, без изменения основного кода.
#
# - **Liskov Substitution Principle (LSP)**: В данном примере не реализована иерархия классов, но можно создать подклассы для различных типов фигур, если это потребуется.
#
# - **Interface Segregation Principle (ISP)**: Интерфейсы не реализованы, но можно создать абстрактный класс или интерфейс для фигур.
#
# - **Dependency Inversion Principle (DIP)**: В данной реализации классы зависят от абстракций (например, можно создать интерфейс для управления фигурами), но в рамках простого проекта это не является критичным.
#
# ### Запуск игры
#
# Запустите код в Python, и у вас должна открыться игра Тетрис. Вы сможете управлять фигурами с помощью стрелок на клавиатуре.
#
# Это базовая реализация, и вы можете добавлять дополнительные функции, такие как счёт, уровень сложности, улучшенную графику и т.д.