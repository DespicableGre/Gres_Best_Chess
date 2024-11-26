import re
class piece:
    def __init__(self, ICON, SIDE, VALUE):
        self.icon = ICON
        self.side = SIDE
        self.value = VALUE
    icon = str
    side = bool
    value = int

# For testing
def Index2Coord(row_column):
    if row_column[0] > 7 or row_column[0] < 0: return "Bruh, Index2Coord(*row_column), 0 ≤ row ≤ 7"
    if row_column[1] > 7 or row_column[1] < 0: return "Bruh2, Index2Coord(row_*column), 0 ≤ column ≤ 7"
    return f"{chr(row_column[0] + 97)}{row_column[1]+1}"

def Coord2Index(row_column):
    if len(row_column) != 2: return "Bruh, Coord2Index(*row_column*), must be 2 characters"
    r = ord(row_column[0]) - 97
    c = int(row_column[1]) - 1
    if r > 7 or r < 0: return "Bruh, Coord2Index(*row_column), first chara must be a-h only"
    if c > 7 or c < 0: return "Bruh, Coord2Index(row_*column), second chara must be 0 ≤ row ≤ 7"
    return r,c


piece_dictionary = {0   : piece(" ",None,None)  ,   # Empty
                    1   : piece("♟",True,1)    ,   # White Pawn
                    2   : piece("♞",True,3)    ,   # White Knight
                    3   : piece("♝",True,3)    ,   # White Bishop
                    4   : piece("♜",True,5)    ,   # White Rook
                    5   : piece("♛",True,9)    ,   # White Queen
                    6   : piece("♚",True,None) ,   # White King
                    7   : piece("♙",False,1)   ,   # Black Pawn
                    8   : piece("♘",False,3)   ,   # Black Knight
                    9   : piece("♗",False,3)   ,   # Black Bishop
                    10  : piece("♖",False,5)   ,   # Black Rook
                    11  : piece("♕",False,9)   ,   # Black Queen
                    12  : piece("♔",False,None),   # Black King
                    "P" : 1,
                    "N" : 2,
                    "B" : 3,
                    "R" : 4,
                    "Q" : 5,
                    "K" : 6
                    }

real_board = [
    [10,8,9,11,12,9,8,10],
    [7,7,7,7,7,7,7,7],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1],
    [4,2,3,5,6,3,2,4]
    ]

real_board.reverse()

def update_board():
    global real_board
    real_board.reverse() # cheeky. Also dont reverse maybe if multiplayering later idk
    updatedBoard = ""
    r = 0
    c = 0
    for row in real_board:
        updatedBoard += str(8 - r) + "  "
        for column in row:
            if r % 2 == 0:
                if c % 2 == 0:
                    if column != 0:
                        updatedBoard += f"|={piece_dictionary[column].icon} ="
                    else:
                        updatedBoard += f"|===="
                else:
                    updatedBoard += f"| {piece_dictionary[column].icon}  "
            if r % 2 == 1:
                if c % 2 == 1:
                    if column != 0:
                        updatedBoard += f"|={piece_dictionary[column].icon} ="
                    else:
                        updatedBoard += f"|===="
                else:
                    updatedBoard += f"| {piece_dictionary[column].icon}  "
            c += 1
        r += 1

        updatedBoard += "|\n\n"
    real_board.reverse() # cheeky2
    updatedBoard += "     a    b    c    d    e    f    g    h"
    print(updatedBoard)

move = 0 
move_history = []

# Parse
# Check
# Repeat
def interpreter(inp):
    global move
    
    # Information to pass:
    _piece = 1 # For potential checks
    _location = (None, None) # For specification cases
    _capture = False # Always required when capturing
    _destination = (None,None) # Always required

    if len(inp) < 2 or len(inp) > 6:
        print("Please make sure your input follows the algebraic notation rules.")
        return

    # Regex Matching    --------------------------------------------------------------------
    match = re.match(r'([NBRQK])?([a-h])?([1-8])?(x)?([a-h])([1-8])',inp)

    if match:
        # Destination   --------------------------------------------------------------------
        if match.group(5) == None or match.group(6) == None:
            print("Please include your destination coordinate!")
            return
        else:   _destination = (match.group(5), match.group(6))

        # Piece Name    --------------------------------------------------------------------
        if match.group(1) != None:
            _piece = piece_dictionary[match.group(1)]
        else:   _piece = 1

        # Location      --------------------------------------------------------------------
        _location = (match.group(2), match.group(3))

        # Capture       --------------------------------------------------------------------
        if match.group(4) != None:
            _capture = True
        else:   _capture = False
    # --------------------------------------------------------------------------------------

    # If you are black
    if move % 2 == 1:
        _piece += 6

    print(_piece, _location, _capture, _destination)


# All destinations should be input to the piece check def as tuples initially.

def check_Spot(destination, piece):
    global real_board
    if real_board[destination[0]][destination[1]] == piece:
        return True
    else:
        return False

def check_Pawn(destination, piece):
    global real_board

    # (Spot below, Two below)
    found = (None, None)

    if check_Spot(destination, piece) == False or real_board.index(real_board[destination[0]]) == 0:
        return found
    else:
        if check_Spot((destination[0]-1,destination[1]), piece):
            found = (destination[0]-1, destination[1])
        elif check_Spot((destination[0]-2,destination[1]), piece) and real_board.index(real_board[destination[0]]) >= 2:
            # Make sure we dont go out of bounds with that        and
            found = (destination[0]-2, destination[1])
    return found

def check_Rook(destination, piece):
    global real_board

    # None  -   No rooks in the same row/column
    # False -   No more than 1 rooks in the same row/column
    # True  -   More than 1 in the same row/column
    #       (Same row relative to dest, Same column relative to dest)
    found = (None, None)

    if check_Spot(destination, piece) == True:
        #return found
        print("Found", piece, "at", Index2Coord(destination))
    # else:
        # Loop to check possible rooks
    # Loop columns first
    for spots in range(7 - destination[1]):
        if check_Spot((destination[0],destination[1]+spots+1),piece):
            print("found on column:", chr(destination[1]+spots+98))
            if found == (found[0],False):
                found = (found[0],True)
                print(found)
                break
            else: 
                found = (found[0],False)
    # Then rows
    for spots in range(7 - destination[0]):
        if check_Spot((destination[0]+spots+1,destination[1]),piece):
            print("found on row:", destination[0]+spots+1)
            if found == (False,None):
                found = (True, None)
                print(found)
                break
            else: 
                found = (False, None)

check_Rook((0,0),4)

# These are useless for now

def checkColumn(piece, column, side_to_check = None):
    global real_board
    piece_to_check_for = piece
    # Just in case
    if side_to_check == None: # Check for current side's pieces
        piece_to_check_for = piece_dictionary[piece] + (move % 2 * 6)
    elif side_to_check == True: # Check for White pieces
        piece_to_check_for = piece_dictionary[piece]
    elif side_to_check == False: # Check for Black pieces
        piece_to_check_for = piece_dictionary[piece] + 6
    #
    for r in real_board:
        if r[column] == piece_to_check_for:
            print(r[column])

def checkRow(piece, row, side_to_check = None):
    global real_board
    piece_to_check_for = piece
    # Just in case
    if side_to_check == None: # Check for current side's pieces
        piece_to_check_for = piece_dictionary[piece] + (move % 2 * 6)
    elif side_to_check == True: # Check for White pieces
        piece_to_check_for = piece_dictionary[piece]
    elif side_to_check == False: # Check for Black pieces
        piece_to_check_for = piece_dictionary[piece] + 6
    #
    for r in real_board[7-row]:
        if r == piece:
            print(r)


# These are useless for now

update_board()
#interpreter(input())


# Have checks for each piece.
# These checks are checking destination availability first. (Wether or not capturing)
# Then go backwards from destination to location. (Unless piece = Knight)
# If no location given, trace every space in same pattern as piece's. 
# (To check for more than one pieces that can make the same move provided)


# If pieces found > 1, throw error.
# Otherwise make move with the found piece. 


# test = input()
# match = re.match(r'([NBRQK])?([a-h])?([1-8])?(x)?([a-h])([1-8])',test)
# print(match.groups())

# Assume input of only destination is a pawn, check if there is one.
# Erase current position of pawn, place pawn in new destination.


#NOTES
# White Wins:   1-0
# Black Wins:   0-1
# Draw:         1/2-1/2

# (Notation)
#            Move#. White   Black
# Example:       1. e3      d5
# Short-side Castle:    O-O     (Also known as Kingside Castle)
# Long-side Castle:     O-O-O   (Also known as Queenside Castle)
# Check:                +
# Checkmate:            #

# Format:   Piece, Column (If necessary), Row (If necessary), Capture?, Destination (Column, Row)
# Examples: Ngf3, Rh3xh5 N2d1
