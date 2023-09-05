import numpy as np


class GameState():
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK"],
            ["bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK"],
        ])

        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(6):
            print(30)
            for c in range(5):
                print(32)
                turn = self.board[r][c][0]
                print(turn)
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == "p":
                        # print("Line 35 o kaj kore na")
                        self.getPawnMoves(r,c,moves)

        print(moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        directions = [-1, 1] if self.whiteToMove else [1, -1]
        enemy_color = 'b' if self.whiteToMove else 'w'

        for dr in directions:
            if 0 <= r + dr < 6:
                # Single square pawn advance
                if self.board[r + dr][c] == "--":
                    moves.append(Move((r, c), (r + dr, c), self.board))

                # Pawn captures
                for dc in [-1, 1]:
                    new_r, new_c = r + dr, c + dc
                    if 0 <= new_r < 6 and 0 <= new_c < 5 and self.board[new_r][new_c][0] == enemy_color:
                        moves.append(Move((r, c), (new_r, new_c), self.board))


class Move():
    ranksToRows = {"1": 5, "2": 4, "3": 3, "4": 2, "5": 1, "6": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveId == other.moveId
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
