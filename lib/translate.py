import numpy as np

COLS = "ABCDEFGH"
SQUARE_SIZE = 1.5 # inches
HOME_POSITION = np.zeros(2)

def moveToPath(move, displace=None):
    """
    Take an input array "move" as gcode outputs for the motor
    """
    # Find initial position
    # Find final position
    # Create a path of movement and execute
    # Expected Output: "X<int>\r\nY<int>\r\n..."

    # Get initial number of squares
    initialSquares = np.array([COLS.find(move[0][0]), int(move[0][1])])
    # print(initialSquares)

    # Get final number of squares
    finalSquares = np.array([COLS.find(move[1][0]), int(move[1][1])])
    # print(finalSquares)

    # Find difference of squares
    diffSquares = finalSquares - initialSquares
    # print(diffSquares)

    # Move the magnet
    travel(initialSquares*SQUARE_SIZE+HOME_POSITION)

    paths = []
    # Move out of the square
    paths.append(np.ones(2)*SQUARE_SIZE/2)
    paths.append(np.array([diffSquares[0]*SQUARE_SIZE,0]))
    paths.append(np.array([0,diffSquares[1]*SQUARE_SIZE]))
    paths.append(-paths[0])
    slide(paths)

def travel(absPosition):
    """ 
    Move the magnet in a straight line to 'absPosition' while magnet disabled 
    (format: absPosition=[x_pos,y_pos])
     """
    sendCommand("M03") # turn off magnet
    sendCommand("G91") # absolute coords
    travelCommand = "G0 X"+str(absPosition[0])+" Y"+str(absPosition[1]) 
    sendCommand(travelCommand)

# 
def slide(paths):
    """
    Move the magnet along a set of 'paths' while dragging a piece 
    (format: paths=[array([x1_dist,y1_dist]),array([x2_dist,y2_dist]),...]])
    """
    sendCommand("M04") # turn on magnet
    sendCommand("G92") # relative coords
    for path in paths:
        moveCommand = "G0 X"+str(path[0])+" Y"+str(path[1])
        sendCommand(moveCommand)

def sendCommand(command):
    # TODO send through serialControl.py
    print(">",command)

moveToPath(['E1','B5'])