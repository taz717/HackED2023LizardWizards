import numpy as np
COLS = "ABCDEFGH"


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



moveToPath(['E1','B5'])