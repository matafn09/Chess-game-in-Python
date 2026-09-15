import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}

knightScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

bishopScores = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4],
]

queenScores = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 1, 2, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1],
]

rookScores = [
    [4, 3, 4, 4, 4, 4, 3, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 2, 2, 2, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 3, 4, 4, 4, 4, 3, 4],
]

whitePawnScores = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

blackPawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
]

piecePositionScores = {
    "N": knightScores,
    "Q": queenScores,
    "B": bishopScores,
    "R": rookScores,
    "bP": blackPawnScores,
    "wP": whitePawnScores,
}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


"""
Helper method to make first recursive call
"""


def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(
        gs,
        validMoves,
        DEPTH,
        -CHECKMATE,
        CHECKMATE,
        1 if gs.whiteToMove else -1,
    )
    print(f"Nodes evaluated: {counter}")
    return nextMove


def findMoveNegaMaxAlphaBeta(gs, ValidMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # move ordering - implement later
    maxScore = -CHECKMATE
    for move in ValidMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(
            gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier
        )
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()

        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


"""
A positive Score is good for white, a negative score is good for black
"""


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]

            if square != "--":
                # score it positionally
                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == "P":  # for pawns
                        piecePositionScore = piecePositionScores[square][row][
                            col
                        ]
                    else:  # for other pieces
                        piecePositionScore = piecePositionScores[square[1]][
                            row
                        ][col]

                if square[0] == "w":
                    score += pieceScore[square[1]] + piecePositionScore * 0.1
                elif square[0] == "b":
                    score -= pieceScore[square[1]] + piecePositionScore * 0.1
    return score


"""
Find the board based on the material.
"""


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]
    return score


