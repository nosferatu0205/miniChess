import pygame as p
from MiniChess import ChessEngine

HEIGHT = 384
WIDTH = 320
DIMENSION_VERTICAL = 6
DIMENSION_HORIZONTAL = 5
SQ_SIZE = 64
MAX_FPS = 60
IMAGES = {}


def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"../images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    for i in range(len(validMoves)):
        print(validMoves[i].getChessNotation())

    moveMade = False
    load_images()
    # print(gs.board)
    running = True
    sqSelected = ()
    playerClicks = []

    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    else:
                        playerClicks.clear()
                    sqSelected = ()
                    playerClicks = []

        if moveMade:
            validMoves = gs.getValidMoves()
            for move in validMoves:
                print(move.getChessNotation())
            print("----")
            moveMade = False
        # print("working")
        draw_game_state(screen, gs)
        # print("working2")
        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquare(screen, gs, validMoves, sqSelected):
    if len(sqSelected) != 0:
        row, col = sqSelected[0]
        print(sqSelected[0])
        # a piece that can be moved
        if GAME_STATE.board[row][col][0] == ('w' if GAME_STATE.whiteToMove else 'b'):

            # hightlight square
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            # transparency value (0 - transparent, 255 - solid)
            surface.set_alpha(100)
            surface.fill(pygame.Color('blue'))
            WINDOW.blit(surface, (col*SQ_SIZE, row*SQ_SIZE))

            # highlight moves
            # TODO: if it's checkmate then the king should be colored as red
            surface.fill(pygame.Color('yellow'))

            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    WINDOW.blit(
                        surface, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color('white'), p.Color('darkolivegreen3')]
    for r in range(DIMENSION_VERTICAL):
        for c in range(DIMENSION_HORIZONTAL):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION_VERTICAL):
        for c in range(DIMENSION_HORIZONTAL):
            piece = board[r][c]
            if piece != "--":  # Ignore empty squares
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
