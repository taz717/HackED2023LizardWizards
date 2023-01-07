import chess as ch


class kingGizzard:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def engine(self, candidate, depth):
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evaluate()

        else:
            ## list of legal moves for the current board
            moveList = list(self.board.legal_moves)

            ##  init candidate
            newCandidate = None

            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")

            for i in moveList:
                ## play i
                self.board.push(i)

                ## recursive call
                ## get value
                value = self.engine(newCandidate, depth + 1)

                ## minmax without pruning
                ## basic

                ## if maxim (engine turn)
                if value > newCandidate and depth % 2 != 0:
                    newCandidate = value
                    if depth == 1:
                        move = i

                ## if minim (opponent turn)
                elif value < newCandidate and depth % 2 == 0:
                    newCandidate = value

                ## alpha-beta pruning
                ## if previous candidate is better than new candidate
