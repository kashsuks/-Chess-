import pygame

pygame.init()

SIDE_BAR_WIDTH = 110
WIDTH, HEIGHT = 950, 840
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // (COLS + 1)

WHITE, BLACK = (240, 217, 181), (181, 136, 99)
LIGHT_INDICATOR = (255, 255, 255)
DARK_INDICATOR = (50, 50, 50)
BACKGROUND_GRAY = (200, 200, 200)

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
            pygame.draw.rect(win, color, ((col * SQUARE_SIZE), row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(win, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != ".":
                win.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def findCurrentSquare(board, mousePosition):
    x, y = mousePosition
    if x >= WIDTH - SIDE_BAR_WIDTH:
        return None
    col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None

def drawSideBar(win, whiteTurn):
    pygame.draw.rect(win, BACKGROUND_GRAY, (WIDTH - SIDE_BAR_WIDTH, 0, SIDE_BAR_WIDTH, HEIGHT))
    turnRectHeight = HEIGHT // 2
    
    white_color = LIGHT_INDICATOR if whiteTurn else (150, 150, 150)
    pygame.draw.rect(win, white_color, (WIDTH - SIDE_BAR_WIDTH, 0, SIDE_BAR_WIDTH, turnRectHeight))
    
    black_color = DARK_INDICATOR if not whiteTurn else (100, 100, 100)
    pygame.draw.rect(win, black_color, (WIDTH - SIDE_BAR_WIDTH, turnRectHeight, SIDE_BAR_WIDTH, turnRectHeight))
    
    font = pygame.font.Font(None, 36)
    whiteText = font.render("", True, (0, 0, 0) if whiteTurn else (100, 100, 100))
    blackText = font.render("", True, (255, 255, 255) if not whiteTurn else (150, 150, 150))
    
    win.blit(whiteText, (WIDTH - SIDE_BAR_WIDTH + (SIDE_BAR_WIDTH - whiteText.get_width()) // 2, turnRectHeight // 2 - whiteText.get_height() // 2))
    win.blit(blackText, (WIDTH - SIDE_BAR_WIDTH + (SIDE_BAR_WIDTH - blackText.get_width()) // 2, turnRectHeight + turnRectHeight // 2 - blackText.get_height() // 2))
    

def getLegalMoves(board, position, piece, whiteTurn):
    if (whiteTurn and piece.islower()) or (not whiteTurn and piece.isupper()):
        return []

    row, col = position
    moves = []

    if piece.lower() == "p":  # Pawn moves
        direction = -1 if piece.isupper() else 1
        if 0 <= row + direction < ROWS and board[row + direction][col] == ".":
            moves.append((row + direction, col))

        if piece.isupper() and row == 6:  # White pawn (2nd rank)
            if board[row + direction][col] == "." and board[row + 2 * direction][col] == ".":
                moves.append((row + 2 * direction, col))
        elif piece.islower() and row == 1:  # Black pawn (7th rank)
            if board[row + direction][col] == "." and board[row + 2 * direction][col] == ".":
                moves.append((row + 2 * direction, col))

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

    elif piece.lower() == "n":  # Knight moves
        knight_moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        for dr, dc in knight_moves:
            newRow, newCol = row + dr, col + dc
            if 0 <= newRow < ROWS and 0 <= newCol < COLS and (board[newRow][newCol] == "." or board[newRow][newCol].islower() != piece.islower()):
                moves.append((newRow, newCol))

    elif piece.lower() == "b":  # Bishop moves
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for i in range(1, ROWS):
                newRow, newCol = row + i * dr, col + i * dc
                if 0 <= newRow < ROWS and 0 <= newCol < COLS:
                    if board[newRow][newCol] == ".":
                        moves.append((newRow, newCol))
                    elif board[newRow][newCol].islower() != piece.islower():
                        moves.append((newRow, newCol))
                        break
                    else:
                        break
                else:
                    break

    elif piece.lower() == "q":  # Queen moves
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for i in range(1, ROWS):
                newRow, newCol = row + i * dr, col + i * dc
                if 0 <= newRow < ROWS and 0 <= newCol < COLS:
                    if board[newRow][newCol] == ".":
                        moves.append((newRow, newCol))
                    elif board[newRow][newCol].islower() != piece.islower():
                        moves.append((newRow, newCol))
                        break
                    else:
                        break
                else:
                    break

    elif piece.lower() == "k":  # King moves
        kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in kingMoves:
            newRow, newCol = row + dr, col + dc
            if 0 <= newRow < ROWS and 0 <= newCol < COLS and (board[newRow][newCol] == "." or board[newRow][newCol].islower() != piece.islower()):
                moves.append((newRow, newCol))

    return moves

def highlightLegalMoves(win, moves):
    for move in moves:
        row, col = move
        centerX = col * SQUARE_SIZE + SQUARE_SIZE // 2
        centerY = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(win, (0, 255, 0), (centerX, centerY), SQUARE_SIZE // 8)

def drawTurnIndicator(win, whiteTurn):
    indicatorColor = (255, 255, 255) if whiteTurn else (0, 0, 0)
    pygame.draw.circle(win, indicatorColor, (WIDTH - 50, HEIGHT - 50), 20)

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MagnusAI")
    clock = pygame.time.Clock()
    images = loadPieceAssets()

    board = [row[:] for row in START_POSITION]

    whiteTurn = True
    selectedPiece = None
    selectedPosition = None
    legalMoves = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                square = findCurrentSquare(board, mousePosition)
                if square:
                    row, col = square
                    if board[row][col] != ".":
                        selectedPiece = board[row][col]
                        selectedPosition = (row, col)
                        legalMoves = getLegalMoves(board, selectedPosition, selectedPiece, whiteTurn)

            if event.type == pygame.MOUSEBUTTONUP:
                mousePosition = pygame.mouse.get_pos()
                square = findCurrentSquare(board, mousePosition)
                if square and selectedPiece:
                    newRow, newCol = square

                    if (newRow, newCol) in legalMoves:
                        oldRow, oldCol = selectedPosition
                        board[oldRow][oldCol] = "."
                        board[newRow][newCol] = selectedPiece
                        whiteTurn = not whiteTurn

                    selectedPiece = None
                    selectedPosition = None
                    legalMoves = []

        win.fill(BACKGROUND_GRAY)

        drawBoard(win)
        drawPieces(win, board, images)
        
        drawSideBar(win, whiteTurn)

        if selectedPosition:
            row, col = selectedPosition
            pygame.draw.rect(win, (255, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            highlightLegalMoves(win, legalMoves)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    
if __name__ == "__main__":
    main()