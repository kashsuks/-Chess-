import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE, BLACK = (240, 217, 181), (181, 136, 99)
LIGHT_HIGHLIGHT = (255, 255, 255, 128)  # Translucent white
DARK_HIGHLIGHT = (0, 0, 0, 128)  # Translucent black
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

class GameState:
    def __init__(self):
        self.board = [row[:] for row in START_POSITION]
        self.whiteTurn = True
        self.whiteKingMoved = False
        self.blackKingMoved = False
        self.whiteRookKingsideMoved = False
        self.whiteRookQueensideMoved = False
        self.blackRookKingsideMoved = False
        self.blackRookQueensideMoved = False
        self.enPassantSquare = None

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

def findCurrentSquare(board, mousePosition):
    x, y = mousePosition
    col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None

def isValidCastle(gameState, start, end):
    """Check if castling move is valid."""
    startRow, startCol = start
    endRow, endCol = end
    board = gameState.board
    piece = board[startRow][startCol]

    # Is it a kingside or queenside castle?
    isKingsideCastle = endCol > startCol
    isWhite = piece.isupper()

    # Check the status of the king and rook
    if isWhite:
        if gameState.whiteKingMoved:
            return False
        if isKingsideCastle and gameState.whiteRookKingsideMoved:
            return False
        if not isKingsideCastle and gameState.whiteRookQueensideMoved:
            return False
    else:
        if gameState.blackKingMoved:
            return False
        if isKingsideCastle and gameState.blackRookKingsideMoved:
            return False
        if not isKingsideCastle and gameState.blackRookQueensideMoved:
            return False

    # Check if the path between king and rook is clear
    colRange = range(startCol + 1, 7) if isKingsideCastle else range(1, startCol)
    for col in colRange:
        if board[startRow][col] != ".":
            return False

    return True

def getLegalMoves(gameState, position, piece, whiteTurn):
    if (whiteTurn and piece.islower()) or (not whiteTurn and piece.isupper()):
        return []

    row, col = position
    board = gameState.board
    moves = []

    if piece.lower() == "p":  # Pawn moves
        direction = -1 if piece.isupper() else 1
        if 0 <= row + direction < ROWS and board[row + direction][col] == ".":
            moves.append((row + direction, col))

        # Initial two-square move
        if piece.isupper() and row == 6:  # White pawn (2nd rank)
            if board[row + direction][col] == "." and board[row + 2 * direction][col] == ".":
                moves.append((row + 2 * direction, col))
        elif piece.islower() and row == 1:  # Black pawn (7th rank)
            if board[row + direction][col] == "." and board[row + 2 * direction][col] == ".":
                moves.append((row + 2 * direction, col))

        # Capture moves
        captureCols = [col - 1, col + 1]
        for captureCol in captureCols:
            if 0 <= captureCol < COLS and 0 <= row + direction < ROWS:
                # Normal capture
                if board[row + direction][captureCol] != "." and board[row + direction][captureCol].islower() != piece.islower():
                    moves.append((row + direction, captureCol))
                
                # En Passant
                if gameState.enPassantSquare == (row + direction, captureCol):
                    moves.append((row + direction, captureCol))

        # Rook moves
    elif piece.lower() == "r":
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
        knightMoves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        for dr, dc in knightMoves:
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

        # Castling moves
        if (whiteTurn and not gameState.whiteKingMoved) or (not whiteTurn and not gameState.blackKingMoved):
            # Kingside castle
            if isValidCastle(gameState, (row, col), (row, col + 2)):
                moves.append((row, col + 2))
            # Queenside castle
            if isValidCastle(gameState, (row, col), (row, col - 2)):
                moves.append((row, col - 2))

    return moves

def performCastle(gameState, start, end):
    startRow, startCol = start
    endRow, endCol = end
    board = gameState.board

    # Kingside castle
    if endCol > startCol:
        board[startRow][startCol + 1] = board[startRow][7]
        board[startRow][7] = "."
    # Queenside castle
    else:
        board[startRow][startCol - 1] = board[startRow][0]
        board[startRow][0] = "."

def enPassant(gameState, start, end):
    startRow, startCol = start
    endRow, endCol = end
    board = gameState.board
    board[startRow][endCol] = "."

def highlightLegalMoves(win, moves):
    for move in moves:
        row, col = move
        centerX = col * SQUARE_SIZE + SQUARE_SIZE // 2
        centerY = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(win, (0, 255, 0), (centerX, centerY), SQUARE_SIZE // 8)

def drawTurnIndicator(win, whiteTurn):
    indicatorColor = (255, 255, 255) if whiteTurn else (0, 0, 0)
    pygame.draw.circle(win, indicatorColor, (WIDTH - 50, HEIGHT - 50), 20)
    
def findKingPosition(board, isWhite):
    king = "K" if isWhite else "k"
    for row in range[ROWS]:
        for col in range[COLS]:
            if board[row][col] == king:
                return (row, col)
    return None

def isSquareUnderAttack(gameState, position, isWhite):
    row, col = position
    opponentMoves = []
    for r in range(ROWS):
        for c in range(COLS):
            piece = gameState.board[r][c]
            if (piece.isupper() and not isWhite) or (piece.islower() and isWhite):
                opponentMoves.extend(getLegalMoves(gameState, (r, c), piece, not isWhite))
    return position in opponentMoves

def isCheckmate(gameState, isWhite):
    kingPosition = findKingPosition(gameState.board, isWhite)
    
    if not kingPosition:
        return False

    if not isSquareUnderAttack(gameState, kingPosition, isWhite):
        return False

    for row in range(ROWS):
        for col in range(COLS):
            piece = gameState.board[row][col]
            if (piece.isupper() and isWhite) or (piece.islower() and not isWhite):
                moves = getLegalMoves(gameState, (row, col), piece, isWhite)
                for move in moves:
                    oldPiece = gameState.board[move[0]][move[1]]
                    gameState.board[move[0]][move[1]] = piece
                    gameState.board[row][col] = "."

                    kingSafe = not isSquareUnderAttack(gameState, findKingPosition(gameState.board, isWhite), isWhite)

                    gameState.board[row][col] = piece
                    gameState.board[move[0]][move[1]] = oldPiece

                    if kingSafe:
                        return False
    return True

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("?Chess?")
    clock = pygame.time.Clock()
    images = loadPieceAssets()

    gameState = GameState()
    board = gameState.board

    selectedPiece = None
    selectedPosition = None
    legalMoves = []

    # Highlight burst timing variables
    highlight_start_time = None
    highlight_duration = 300  # milliseconds

    running = True
    while running:
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
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
                        legalMoves = getLegalMoves(gameState, selectedPosition, selectedPiece, gameState.whiteTurn)

            if event.type == pygame.MOUSEBUTTONUP:
                mousePosition = pygame.mouse.get_pos()
                square = findCurrentSquare(board, mousePosition)
                if square and selectedPiece:
                    newRow, newCol = square

                    if (newRow, newCol) in legalMoves:
                        oldRow, oldCol = selectedPosition

                        # Handle en passant
                        if (selectedPiece.lower() == "p" and gameState.enPassantSquare == (newRow, newCol)):
                            enPassant(gameState, selectedPosition, (newRow, newCol))

                        # Handle castling
                        if selectedPiece.lower() == "k" and abs(newCol - oldCol) == 2:
                            performCastle(gameState, (oldRow, oldCol), (newRow, newCol))

                        # Move the piece
                        board[oldRow][oldCol] = "."
                        board[newRow][newCol] = selectedPiece

                        # Update movement flags for king and rook
                        if selectedPiece == "K":
                            gameState.whiteKingMoved = True
                        elif selectedPiece == "k":
                            gameState.blackKingMoved = True
                        
                        if selectedPiece == "R" and oldCol == 0:
                            gameState.whiteRookQueensideMoved = True
                        elif selectedPiece == "R" and oldCol == 7:
                            gameState.whiteRookKingsideMoved = True
                        elif selectedPiece == "r" and oldCol == 0:
                            gameState.blackRookQueensideMoved = True
                        elif selectedPiece == "r" and oldCol == 7:
                            gameState.blackRookKingsideMoved = True

                        # Set up en passant possibility for two-square pawn moves
                        if selectedPiece.lower() == "p" and abs(newRow - oldRow) == 2:
                            gameState.enPassantSquare = ((oldRow + newRow) // 2, oldCol)
                        else:
                            gameState.enPassantSquare = None

                        # Switch turns and trigger highlight burst
                        gameState.whiteTurn = not gameState.whiteTurn
                        highlight_start_time = current_time

                    selectedPiece = None
                    selectedPosition = None
                    legalMoves = []

        # Drawing the game components
        win.fill(BACKGROUND_GRAY)
        drawBoard(win)

        drawPieces(win, board, images)

        if selectedPosition:
            row, col = selectedPosition
            pygame.draw.rect(win, (255, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            highlightLegalMoves(win, legalMoves)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()