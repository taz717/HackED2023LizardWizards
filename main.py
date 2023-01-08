from lib import kingGizzard as kg
import chess as ch


class Main:
    def __init__(self, board=ch.Board):
        self.arduinoData = serial.Serial('com6', 115200)

        self.board = board

    ## play opponent move
    def playOpponentMove(self):
        try:
            print(list(self.board.legal_moves))
            print("""To undo your last move, type "undo".""")
            ## get user input
            play = input("your move: ")
            if play == "undo":
                self.board.pop()
                self.board.pop()
                self.playOpponentMove()
                return
            
            self.board.push(self.board.parse_uci(play))
            #write acknoledgement back to arduino that it was a valid move
        except:
            print("INVALID MOVE... Return piece to previous position")
            
            # check from Arduino if piece is returned
            # for now set to dummy variable and skip loop
            returned = True
            while (not returned):
                pass
            self.playOpponentMove()

    ## play king gizzard move
    def playEngineMove(self, maxDepth, color):
        engine = kg.kingGizzard(self.board, maxDepth, color)
        self.board.push(engine.getBestMove())

    def translateBoards(self, previousTurn):
        print(previousTurn == self.board)

    def startGame(self):
        ## get opponent color
        color = None
        while color not in ["w", "b"]:
            color = input("choose color (w/b): ")
        maxDepth = None
        while isinstance(maxDepth, int) == False:
            maxDepth = int(input("choose max depth: "))
        if color == "b":
            while self.board.is_checkmate() == False:
                print("King Gizzard is thinking...")
                temp = self.board
                self.playEngineMove(maxDepth, ch.WHITE)
                self.translateBoards(temp)
                print(self.board)
                self.playOpponentMove()
            print(self.board)
            print(self.board.outcome())
        elif color == "w":
            while self.board.is_checkmate() == False:
                print(self.board)
                self.playOpponentMove()
                print(self.board)
                print("King Gizzard is thinking...")
                self.playEngineMove(maxDepth, ch.BLACK)
            print(self.board)
            print(self.board.outcome())

            ## reset the board
            self.board.reset
            ## start new game
            self.startGame()


newBoard = ch.Board()
game = Main(newBoard)
game.startGame()
