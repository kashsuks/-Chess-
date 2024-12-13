def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MagnusAI")
    clock = pygame.time.Clock()
    images = loadPieceAssets()

    board = [row[:] for row in START_POSITION]

    selected_piece = None
    selected_position = None
    legalMoves = []

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
                        legalMoves = getLegalMoves(board, selected_position, selected_piece)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                square = findCurrentSquare(board, mouse_pos)
                if square and selected_piece:
                    newRow, newCol = square

                    if (newRow, newCol) in legalMoves:
                        old_row, old_col = selected_position
                        board[old_row][old_col] = "."
                        board[newRow][newCol] = selected_piece

                    selected_piece = None
                    selected_position = None
                    legalMoves = []

        drawBoard(win)
        drawPieces(win, board, images)

        if selected_position:
            row, col = selected_position
            pygame.draw.rect(win, (255, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            highlightLegalMoves(win, legalMoves)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()