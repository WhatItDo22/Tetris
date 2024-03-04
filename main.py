import pygame
import random

# Pygame setup
pygame.init()
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors and Shapes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(0, 255, 255), (255, 165, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0), (128, 0, 128)]
tetromino_shapes = [
    [[1, 1, 1, 1]],  # I
    [[2, 2], [2, 2]],  # O
    [[0, 3, 3], [3, 3, 0]],  # S
    [[4, 4, 0], [0, 4, 4]],  # Z
    [[5, 0, 0], [5, 5, 5]],  # J
    [[0, 0, 6], [6, 6, 6]],  # L
    [[0, 7, 0], [7, 7, 7]]  # T
]

# Game variables
block_size = 30
board_width = 10
board_height = 20
board = [[0 for _ in range(board_width)] for _ in range(board_height)]
current_piece = None
current_position = [0, 0]
score = 0


def create_piece():
    global current_piece, current_position
    current_piece = random.choice(tetromino_shapes)
    current_position = [0, board_width // 2 - len(current_piece[0]) // 2]
    # Game over condition
    if not valid_space(current_piece, current_position):
        return False
    return True


def rotate_piece(piece):
    return [list(row) for row in zip(*piece[::-1])]


def valid_space(piece, position):
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                if y + position[0] >= board_height or x + position[1] < 0 or x + position[1] >= board_width or \
                        board[y + position[0]][x + position[1]]:
                    return False
    return True


def integrate_piece_into_board(piece, position):
    global score
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                board[y + position[0]][x + position[1]] = cell
    clear_rows()


def clear_rows():
    global score
    to_clear = [i for i, row in enumerate(board) if 0 not in row]
    for i in reversed(to_clear):
        del board[i]
        board.insert(0, [0 for _ in range(board_width)])
        score += 100  # Simple scoring, 100 points per cleared row


def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            color = COLORS[cell - 1] if cell else BLACK
            pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size), 0)


def game_loop():
    global current_piece, current_position
    running = True
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.3  # Standard fall speed
    current_fall_speed = fall_speed  # Current fall speed, which can be modified

    if not create_piece():
        print("Game Over! Final Score:", score)
        return  # End game if a new piece cannot be placed

    while running:
        screen.fill(BLACK)
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and valid_space(current_piece,
                                                              [current_position[0], current_position[1] - 1]):
                    current_position[1] -= 1
                if event.key == pygame.K_RIGHT and valid_space(current_piece,
                                                               [current_position[0], current_position[1] + 1]):
                    current_position[1] += 1
                if event.key == pygame.K_UP:
                    rotated_piece = rotate_piece(current_piece)
                    if valid_space(rotated_piece, current_position):
                        current_piece = rotated_piece
                if event.key == pygame.K_DOWN:
                    current_fall_speed = 0.05  # Increase fall speed when down key is pressed

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= current_fall_speed:
            fall_time = 0
            if valid_space(current_piece, [current_position[0] + 1, current_position[1]]):
                current_position[0] += 1
            else:
                integrate_piece_into_board(current_piece, current_position)
                if not create_piece():
                    print("Game Over! Final Score:", score)
                    running = False  # End game if a new piece cannot be placed
                current_fall_speed = fall_speed  # Reset fall speed for the new piece

        draw_board()
        for i, row in enumerate(current_piece):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[cell - 1], (current_position[1] * block_size + j * block_size,
                                                                current_position[0] * block_size + i * block_size,
                                                                block_size, block_size))

        pygame.display.update()


game_loop()
pygame.quit()
