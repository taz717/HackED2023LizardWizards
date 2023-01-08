import numpy as np

COLS = "ABCDEFGH"
SQUARESIZE = 1.5 # inches

def moveToPath(move, displace=None):
    # Find initial position
    # Find final position
    # Create a path of movement and execute
    # Expected Output: "X<int>\r\nY<int>\r\n..."

    # Get initial number of squares
    initialSquares = np.array([COLS.find(move[0][0]), int(move[0][1])])
    print(initialSquares)

    # Get final number of squares
    finalSquares = np.array([COLS.find(move[1][0]), int(move[1][1])])
    print(finalSquares)

    # Find difference of squares
    diffSquares = finalSquares - initialSquares
    print(diffSquares)

    # Move the magnet
    travel(initialSquares)

    paths = []
    # Move out of the square
    paths.append(np.ones(2)*SQUARESIZE/2)
    paths.append(np.array([diffSquares[0]*SQUARESIZE,0]))
    paths.append(np.array([0,diffSquares[1]*SQUARESIZE]))
    paths.append(-paths[0])
    slide(paths)

# Move the magnet in a straight line to 'absPosition' while magnet disabled (format: [x_pos,y_pos])
def travel(absPosition):
    sendCommand("M03") # turn off magnet
    travelCommand = "G91 X"+str(absPosition[0])+" Y"+str(absPosition[1]) # G91 means absolute coords
    sendCommand(travelCommand)

# Move the magnet along a set of 'paths' while dragging a piece (format: [[x1_dist,y1_dist],[x2_dist,y2_dist],...]])
def slide(paths):
    sendCommand("M04")
    for path in paths:
        moveCommand = "G92 X"+str(path[0])+" Y"+str(path[1]) # G92 means relative coords
        sendCommand(moveCommand)

def sendCommand(command):
    # TODO send through serialControl.py
    print(">",command)

moveToPath(['E1','B5'])