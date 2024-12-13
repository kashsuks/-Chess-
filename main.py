import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE, BLACK = (240, 217, 181), (181, 136, 99)

PIECE_IMAGES = {
    "P": "pieces/wp.png", "p": "pieces/bp.png",  # Pawn
    "R": "pieces/wr.png", "r": "pieces/br.png",  # Rook
    "N": "pieces/wn.png", "n": "pieces/bn.png",  # Knight
    "B": "pieces/wb.png", "b": "pieces/bb.png",  # Bishop
    "Q": "pieces/wq.png", "q": "pieces/bq.png",  # Queen
    "K": "pieces/wk.png", "k": "pieces/bk.png",  # King
}

START_POSITION = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

def loadPieceAssets():
    images = {}
    for piece, imgFile in PIECE_IMAGES.items():
        images[piece] = pygame.transform.scale(
            pygame.image.load(imgFile), (SQUARE_SIZE, SQUARE_SIZE)
        )
    return images

def drawBoard(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(win, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != ".":
                win.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def findCurrentSquare(board, mouse_pos):
    x, y = mouse_pos
    col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None

def getLegalMoves(board, position, piece):
    row, col = position
    moves = []

    if piece.lower() == "p":  # Pawn moves
        direction = -1 if piece.isupper() else 1
        if 0 <= row + direction < ROWS and board[row + direction][col] == ".":
            moves.append((row + direction, col))
        if col - 1 >= 0 and 0 <= row + direction < ROWS and board[row + direction][col - 1] != "." and board[row + direction][col - 1].islower() != piece.islower():
            moves.append((row + direction, col - 1))
        if col + 1 < COLS and 0 <= row + direction < ROWS and board[row + direction][col + 1] != "." and board[row + direction][col + 1].islower() != piece.islower():
            moves.append((row + direction, col + 1))

    elif piece.lower() == "r":  # Rook moves
        for d in [-1, 1]:
            for i in range(1, ROWS):
                if 0 <= row + i * d < ROWS and board[row + i * d][col] == ".":
                    moves.append((row + i * d, col))
                elif 0 <= row + i * d < ROWS and board[row + i * d][col].islower() != piece.islower():
                    moves.append((row + i * d, col))
                    break
                else:
                    break
            for i in range(1, COLS):
                if 0 <= col + i * d < COLS and board[row][col + i * d] == ".":
                    moves.append((row, col + i * d))
                elif 0 <= col + i * d < COLS and board[row][col + i * d].islower() != piece.islower():
                    moves.append((row, col + i * d))
                    break
                else:
                    break

    # Add other pieces' logic (knight, bishop, queen, king)

    return moves

def highlightLegalMoves(win, moves):
    for move in moves:
        row, col = move
        pygame.draw.rect(win, (0, 255, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MagnusAI")
    clock = pygame.time.Clock()
    images = loadPieceAssets()

    board = [row[:] for row in START_POSITION]

    selected_piece = None
    selected_position = None
    legal_moves = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                square = findCurrentSquare(board, mouse_pos)
                if square:
                    row, col = square
                    if board[row][col] != ".":
                        selected_piece = board[row][col]
                        selected_position = (row, col)
                        legal_moves = getLegalMoves(board, selected_position, selected_piece)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                square = findCurrentSquare(board, mouse_pos)
                if square and selected_piece:
                    new_row, new_col = square

                    if (new_row, new_col) in legal_moves:
                        old_row, old_col = selected_position
                        board[old_row][old_col] = "."
                        board[new_row][new_col] = selected_piece

                    selected_piece = None
                    selected_position = None
                    legal_moves = []

        drawBoard(win)
        drawPieces(win, board, images)

        if selected_position:
            row, col = selected_position
            pygame.draw.rect(win, (255, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            highlightLegalMoves(win, legal_moves)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
