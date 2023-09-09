import random

piece_score = {"K": 100, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 3

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2],
                 [0.1, 0.3, 0.5, 0.5, 0.5],
                 [0.2, 0.5, 0.6, 0.65, 0.65],
                 [0.2, 0.55, 0.65, 0.7, 0.7],
                 [0.2, 0.5, 0.65, 0.7, 0.7],
                 [0.2, 0.55, 0.6, 0.65, 0.65]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2],
                 [0.2, 0.4, 0.4, 0.4, 0.4],
                 [0.2, 0.4, 0.5, 0.6, 0.6],
                 [0.2, 0.5, 0.5, 0.6, 0.6],
                 [0.2, 0.4, 0.6, 0.6, 0.6],
                 [0.2, 0.6, 0.6, 0.6, 0.6]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75],
               [0.0, 0.25, 0.25, 0.25, 0.25],
               [0.0, 0.25, 0.25, 0.25, 0.25],
               [0.0, 0.25, 0.25, 0.25, 0.25],
               [0.0, 0.25, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3],
                [0.2, 0.4, 0.4, 0.4, 0.4],
                [0.2, 0.4, 0.5, 0.5, 0.5],
                [0.3, 0.4, 0.5, 0.5, 0.5],
                [0.4, 0.4, 0.5, 0.5, 0.5],
                [0.2, 0.5, 0.5, 0.5, 0.5]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5],
               [0.25, 0.25, 0.3, 0.45, 0.45],
               [0.2, 0.2, 0.2, 0.4, 0.4],
               [0.25, 0.15, 0.1, 0.2, 0.2]]

'''
#manual input
knight_scores = [[0.0, 0.1, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.5, 0.2],
                 [0.2, 0.5, 0.6, 0.5, 0.2],
                 [0.1, 0.3, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.45, 0.65, 0.45, 0.2],
                 [0.2, 0.4, 0.6, 0.4, 0.2],
                 [0.2, 0.5, 0.45, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.5, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.3, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.4, 0.3],
                [0.3, 0.4, 0.5, 0.4, 0.3],
                [0.2, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.3, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5],
               [0.25, 0.25, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.0, 0.0, 0.2],
               [0.2, 0.2, 0.2, 0.2, 0.2]]

'''

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}


def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveMiniMaxPruning(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove


def findMoveMiniMaxPruning(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0 or gs.checkMate or gs.staleMate:
        return turnMultiplier * scoreBoard(gs)

    # Capture Moves First, MVV-LVA Ordering
    capture_moves = [move for move in validMoves if move.is_capture()]
    non_capture_moves = [move for move in validMoves if not move.is_capture()]

    # Order capture_moves based on MVV-LVA heuristic
    capture_moves.sort(key=lambda move: capture_heuristic(gs, move))

    # Combine the ordered lists
    ordered_moves = capture_moves + non_capture_moves

    maxScore = -CHECKMATE
    for move in ordered_moves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveMiniMaxPruning(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)

        # Include current score calculation
        current_score = turnMultiplier * scoreBoard(gs)

        score += current_score  # Add current score to the move's score

        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:  # pruning
            break

    return maxScore


def capture_heuristic(gs, move):
    victim_piece = gs.board[move.endRow, move.endCol]
    attacker_piece = gs.board[move.startRow, move.startCol]

    # Check if the piece is not an empty square
    if victim_piece != '--':
        victim_value = piece_score[victim_piece[1]]
    else:
        victim_value = 0  # Set value to 0 for empty squares

    attacker_value = piece_score[attacker_piece[1]]

    if gs.whiteToMove:
        return victim_value - attacker_value
    else:
        return attacker_value - victim_value


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE

    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(6):
        for col in range(5):
            piece = gs.board[row, col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score
                # print(piece_position_score)
    return score

