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

def load_piece_images():
    images = {}
    for piece, img_file in PIECE_IMAGES.items():
        images[piece] = pygame.transform.scale(
            pygame.image.load(img_file), (SQUARE_SIZE, SQUARE_SIZE)
        )
    return images

def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != ".":
                win.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Main loop
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Board")
    clock = pygame.time.Clock()
    images = load_piece_images()

    board = START_POSITION

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(win)
        draw_pieces(win, board, images)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
