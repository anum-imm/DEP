import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# RGB
RED = (255, 0, 0)
BG_COLOR = (5, 5, 5)
LINE_COLOR = (255, 255,255)
CIRCLE_COLOR = (255, 0, 0)
CROSS_COLOR = (239, 231, 200)
# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Pygame Clock
clock = pygame.time.Clock()

def draw_lines():
    # 1st horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    # 2nd horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

    # 1st vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 2nd vertical
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)  
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_win(player):
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # asc diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True

    # desc diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    return False

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None
    return 'X'
def minimax(board, depth, is_maximizing):
    if check_win('O'):
        return -10
    elif check_win('X'):
        return 10
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float('inf')
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        mark_square(best_move[0], best_move[1], 'O')

player = 'X'
game_over = False
draw_lines()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y
            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                    font = pygame.font.Font(None, 40)
                    text = font.render("You win! Press 'R' to restart.", True, RED)
                    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
                    pygame.display.update()
                elif is_board_full():
                    game_over = True
                    font = pygame.font.Font(None, 40)
                    text = font.render("Draw! Press 'R' to restart.", True, RED)
                    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
                    pygame.display.update()
                else:
                    player = 'O'
                    ai_move()
                    if check_win('O'):
                        game_over = True
                        font = pygame.font.Font(None, 40)
                        text = font.render("AI wins! Press 'R' to restart.", True, RED)
                        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
                        pygame.display.update()
                    elif is_board_full():
                        game_over = True
                        font = pygame.font.Font(None, 40)
                        text = font.render("Draw! Press 'R' to restart.", True, RED)
                        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
                        pygame.display.update()
                    player = 'X'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 'X'
                game_over = False

    draw_figures()
    pygame.display.update()
    clock.tick(60)
