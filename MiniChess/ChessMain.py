import pygame as p
import ChessEngine
import sys
import ai

HEIGHT = 520
WIDTH = 320
DIMENSION_VERTICAL = 6
DIMENSION_HORIZONTAL = 5
SQ_SIZE = 64
MAX_FPS = 60
IMAGES = {}
p.init()
COLORS = {'white': p.Color('white'), 'darkolivegreen3': p.Color('darkolivegreen3'), 'grey': p.Color('beige')}
colors = [COLORS['white'], COLORS['darkolivegreen3']]
font = p.font.SysFont('Arial', 15, bold=True)
restart_button_rect = p.Rect(200, 410, 100, 40)



def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(COLORS['grey'])

    # human is true
    playerOne = True
    # we can put a button jeitay choose kora jayhuman vs human na human vs ai
    playerTwo = False

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()

    restart_button_rect = p.Rect(200, 410, 100, 40)
    moveMade = False
    load_images()
    # print(gs.board)
    running = True
    sqSelected = []
    playerClicks = 0
    message = ""

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
                        sqSelected = []
                        playerClicks = 0
                    else:
                        sqSelected.append((row, col))
                        playerClicks += 1

                    if playerClicks == 2:
                        if sqSelected[0][0] < 6 and sqSelected[1][0] < 6:
                            move = ChessEngine.Move(sqSelected[0], sqSelected[1], gs.board)
                            if move in validMoves:
                                gs.makeMove(move)
                                moveMade = True
                                sqSelected = []
                                playerClicks = 0

                            else:
                                playerClicks = 1
                                sqSelected.remove(sqSelected[0])
                        else:
                            sqSelected = []
                            playerClicks = 0

                if e.type == p.MOUSEBUTTONDOWN and restart_button_rect.collidepoint(e.pos):
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = []
                    playerClicks = 0
                    running = True
                    moveMade = False

        # print("working")
        if not humanPlayer:
            aiMove = ai.findBestMove(gs, validMoves)

            if aiMove:
                # print(aiMove.getChessNotation())
                gs.makeMove(aiMove)
                moveMade = True
            else:
                # print("Player Won")
                message = "You Won :)"

        if moveMade:
            validMoves = gs.getValidMoves()
            if not validMoves:
                # print("Player lost")
                message = "You Lost :("
            moveMade = False


        draw_game_state(screen, gs, validMoves, sqSelected, message)
        # print("working2")
        p.display.flip()


def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"../images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, gs, validMoves, sqSelected, message):
    draw_board(screen)
    draw_pieces(screen, gs.board)
    draw_buttons(screen)
    draw_turn_indicator(screen, gs, message)


def draw_board(screen):
    for r in range(DIMENSION_VERTICAL):
        for c in range(DIMENSION_HORIZONTAL):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            # chess notation
            rank = 6 - r
            if c == 0:
                text = font.render(str(rank), True, 'black')
                screen.blit(text, (5, r * SQ_SIZE))

            if r == DIMENSION_VERTICAL - 1:
                text = font.render(chr(ord('a') + c), True, 'black')
                screen.blit(text, (c * SQ_SIZE + 5, DIMENSION_VERTICAL * SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION_VERTICAL):
        for c in range(DIMENSION_HORIZONTAL):
            piece = board[r][c]
            if piece != "--":  # Ignore empty squares
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_buttons(screen):
    p.draw.rect(screen, "darkgreen", restart_button_rect)
    restart_text = font.render("Restart", True, "white")
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_text, restart_text_rect)


def draw_turn_indicator(screen, gs, message):
    indicator_size = 40  # Size of the square indicator
    text_padding = 10  # Padding between text and the square indicator
    turn_rect = p.Rect(10, 410, indicator_size + text_padding + indicator_size, indicator_size)

    font1 = p.font.SysFont('Arial', 18, bold=False)
    text_surface = font1.render("Turn: ", True, "black")
    text_rect = text_surface.get_rect(topleft=(turn_rect.left, turn_rect.centery - text_surface.get_height() // 2))
    screen.blit(text_surface, text_rect)

    indicator_color = "white" if gs.whiteToMove else "black"
    indicator_rect = p.Rect(text_rect.right + text_padding, turn_rect.top, indicator_size, indicator_size)
    p.draw.rect(screen, indicator_color, indicator_rect)
    p.draw.rect(screen, "red", indicator_rect, 1)

    message_box_rect = p.Rect(10, turn_rect.bottom + 10, WIDTH - 20, 50)
    p.draw.rect(screen, "black", message_box_rect)
    p.draw.rect(screen, "red", message_box_rect, 1)
    
    # Draw the message text in the message box
    if message:
        font2 = p.font.SysFont('Arial', 16, bold=False)  # Choose an appropriate font and size for messages
        message_surface = font2.render(message, True, "green")
        message_rect = message_surface.get_rect(center=message_box_rect.center)
        screen.blit(message_surface, message_rect)

    p.display.update([turn_rect, message_box_rect])


if __name__ == "__main__":
    main()
