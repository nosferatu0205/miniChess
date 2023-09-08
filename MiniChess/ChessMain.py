import pygame as p
from MiniChess import ChessEngine
import sys
import ai

HEIGHT = 520
WIDTH = 320
DIMENSION_VERTICAL = 6
DIMENSION_HORIZONTAL = 5
SQ_SIZE = 64
MAX_FPS = 60
IMAGES = {}


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))

    # human is true
    playerOne = True
    #we can put a button jeitay choose kora jayhuman vs human na human vs ai
    playerTwo = False

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()

    restart_button_rect = p.Rect(200, 410, 100, 40)
    moveMade = False
    load_images()
    # print(gs.board)
    running = True
    sqSelected = ()
    playerClicks = []

    while running:
        humanPlayer = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                if humanPlayer:
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
                       # print(move.getChessNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                        else:
                            playerClicks.clear()
                        sqSelected = ()
                        playerClicks = []
                if e.type == p.MOUSEBUTTONDOWN and restart_button_rect.collidepoint(e.pos):
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    running= True
                    moveMade = False

        # print("working")
        if not humanPlayer:
            aiMove = ai.findBestMove(gs, validMoves)
            gs.makeMove(aiMove)
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
          #  for move in validMoves:
               # print(move.getChessNotation())

          #  print("----")
            moveMade = False

        draw_game_state(screen, gs, validMoves, sqSelected)
        # print("working2")
        clock.tick(MAX_FPS)
        p.display.flip()


def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"../images/{piece}.png"), (SQ_SIZE, SQ_SIZE))




def draw_game_state(screen, gs, validMoves, sqSelected):
    draw_board(screen)
    draw_pieces(screen, gs.board)
    draw_buttons(screen)
    draw_turn_indicator(screen, gs)


def draw_board(screen):
    colors = [p.Color('white'), p.Color('darkolivegreen3')]
    for r in range(DIMENSION_VERTICAL):
        for c in range(DIMENSION_HORIZONTAL):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


            #chess notation
            rank = 6 - r
            if c == 0:
                surface = p.font.SysFont('Arial', 15).render(str(rank), True, 'black')
                screen.blit(surface, (5, r * SQ_SIZE))

            if r == DIMENSION_VERTICAL - 1:

                surface = p.font.SysFont('Arial', 15).render(chr(ord('a') + c), True, 'black')
                screen.blit(surface, (c * SQ_SIZE + 5,  (DIMENSION_VERTICAL) * SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION_VERTICAL):
        for c in range(DIMENSION_HORIZONTAL):
            piece = board[r][c]
            if piece != "--":  # Ignore empty squares
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_buttons(screen):

    # Draw "Restart" button
    restart_button_rect = p.Rect(200, 410, 100, 40)  # position, width, height
    p.draw.rect(screen, "darkgreen", restart_button_rect)

    restart_text = p.font.SysFont('Arial', 20, bold=True).render("Restart", True, "white")  # font, color, text
    restart_text_rect = restart_text.get_rect(
        center=restart_button_rect.center)
    screen.blit(restart_text, restart_text_rect)

def draw_turn_indicator(screen, gs):
    # Draw a rectangle to indicate the current player's turn
    turn_rect = p.Rect(10, 410, 100, 40)
    turn_color = "white"
    p.draw.rect(screen, turn_color, turn_rect)

    # Draw a border around the turn indicator box
    border_rect = p.Rect(10, 410, 100, 40)
    border_color = "gray"  # Choose a color for the border
    p.draw.rect(screen, border_color, border_rect, 3)  # The last argument (3) is the border width

    # Draw text to indicate the current player's turn
    font = p.font.SysFont('Arial', 20, bold=True)
    turn_text = font.render(f"Turn: {'White' if gs.whiteToMove else 'Black'}", True, "black")
    turn_text_rect = turn_text.get_rect(center=turn_rect.center)
    screen.blit(turn_text, turn_text_rect)


if __name__ == "__main__":
    main()
