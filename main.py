from lib import kingGizzard as kg
import chess as ch
import serial
# import serial

numToLetterDict = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}


class Main:
    def __init__(self, board=ch.Board):
        ## TODO talk about in meeting
        # self.arduinoData = serial.Serial("com6", 115200)

        self.board = board

    def getUserMove(self):
        arduinoData = serial.Serial('com6', 115200)
        start = (0,0)
        end = (0,0)
        dataPacket = arduinoData.readline()
        dataPacket = str(dataPacket, 'utf-8')
        dataPacket = dataPacket.strip('\r\n')
        occupied = [int(x) for x in dataPacket.split(',')]
        pieceLifted = False
        oppPieceLifted = (-1,-1)
        userTurn = True
        while userTurn:
            if arduinoData.inWaiting() != 0:
                dataPacket = arduinoData.readline()
                dataPacket = str(dataPacket, 'utf-8')
                dataPacket = dataPacket.strip('\r\n')
                new_occupancy = [int(x) for x in dataPacket.split(',')]
                if new_occupancy != occupied and not pieceLifted :
                    pieceLifted = True
                    for i in range(len(occupied)):
                        if occupied[i] != new_occupancy[i]:
                            bit_string_old = '{0:b}'.format(occupied[i])
                            bit_string_new = '{0:b}'.format(new_occupancy[i])
                            for j in range(len(bit_string_new)):
                                # find what has flipped to 0
                                if bit_string_old[j]=='1' and bit_string_new[j]=='0':
                                    start = (i,j)
                                    break
                            break
                    occupied = new_occupancy
                if new_occupancy != occupied and pieceLifted :
                    for i in range(len(occupied)):
                        if occupied[i] != new_occupancy[i]:
                            bit_string_old = '{0:b}'.format(occupied[i])
                            bit_string_new = '{0:b}'.format(new_occupancy[i])
                            for j in range(len(bit_string_new)):
                                # find what has flipped to 0
                                if bit_string_old[j]=='0' and bit_string_new[j]=='1':
                                    end = (i,j) #user piece has taken empty position
                                    userTurn=False
                                    break
                                if bit_string_old[j]=='1' and bit_string_new[j]=='0':
                                    # lifting up opponent piece
                                    oppPieceLifted=(i,j)
                                    userTurn=False
                                    break
                            break
                    occupied = new_occupancy
                if new_occupancy != occupied and oppPieceLifted!=(-1,-1) and pieceLifted:
                    bit_string_old = '{0:b}'.format(occupied[oppPieceLifted[0]])
                    bit_string_new = '{0:b}'.format(new_occupancy[oppPieceLifted[0]])
                    if bit_string_old[oppPieceLifted[1]]=='0' and bit_string_new[oppPieceLifted[1]]=='1':
                        end = (i,j) #user piece has taken empty position
                        userTurn=False
                        break
                    occupied = new_occupancy
        return chr(start[0]+97)+str(start[1]+1)+chr(end[0]+97)+str(end[1]+1)

    ## play opponent move
    def playOpponentMove(self):
        try:
            ## Don't list this, it doesn't look as nice
            print(self.board.legal_moves)
            print("""To undo your last move, type "undo".""")
            ## get user input
            play = input("your move: ")
            
            if play == "undo":
                self.board.pop()
                self.board.pop()
                self.playOpponentMove()
                return

            self.board.push(self.board.parse_uci(play))
        except:
            print("INVALID MOVE... Return piece to previous position")

            # check from Arduino if piece is returned
            # for now set to dummy variable and skip loop
            returned = True
            while not returned:
                pass
            self.playOpponentMove()

    def makeMatrix(self, board):  # type(board) == chess.Board()
        ## https://stackoverflow.com/questions/55876336/is-there-a-way-to-convert-a-python-chess-board-into-a-list-of-integers

        ## returns 2d array with board

        pgn = board.epd()
        foo = []  # Final board
        pieces = pgn.split(" ", 1)[0]
        rows = pieces.split("/")
        for row in rows:
            foo2 = []  # This is the row I make
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append(".")
                else:
                    foo2.append(thing)
            foo.append(foo2)
        return foo

    def compareBoards(self, matrix1, matrix2):
        vals = []
        for i in range(len(matrix1)):
            for j in range(len(matrix1)):
                if matrix1[i][j] != matrix2[i][j]:
                    vals.append(numToLetterDict[j + 1] + str(i + 1))

        return vals

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

                previousBoard = self.makeMatrix(self.board)
                self.playEngineMove(maxDepth, ch.WHITE)
                print(self.board)
                vals = self.compareBoards(previousBoard, self.makeMatrix(self.board))
                ## TODO SEND VALS TO ARDUINO TO MOVE PIECES
                print(vals)

                self.playOpponentMove()

            print(self.board)
            print(self.board.outcome())
        elif color == "w":
            while self.board.is_checkmate() == False:
                print(self.board)
                self.playOpponentMove()
                print(self.board)

                print("King Gizzard is thinking...")
                previousBoard = self.makeMatrix(self.board)
                self.playEngineMove(maxDepth, ch.BLACK)
                vals = self.compareBoards(previousBoard, self.makeMatrix(self.board))
                ## TODO SEND VALS TO ARDUINO TO MOVE PIECES
                print(vals)

            print(self.board)
            print(self.board.outcome())

            ## reset the board
            self.board.reset
            ## start new game
            self.startGame()


if __name__ == "__main__":
    newBoard = ch.Board()
    game = Main(newBoard)
    game.startGame()
