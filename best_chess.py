import re

# the indexing is so messed up
# Maybe if python actually had 2D arrays,
# this would not be making my head hurt.

class piece:
    def __init__(self, ICON, SIDE, VALUE, NAME):
        self.icon = ICON
        self.side = SIDE
        self.value = VALUE
        self.fullName = NAME
    icon = str
    side = bool
    value = int
    fullName = str

def parser(inp):
    global move, previous_move, input_error, running, piece_dictionary
    input_error = False

    # Information to pass:
    _piece = 1 # For potential checks
    _location = (None, None) # For specification cases
    _capture = False # Always required when capturing
    _destination = (None,None) # Always required

    if len(inp) < 2 or len(inp) > 6:
        input_error = True
        return
    elif inp == "qq":
        input_error = False
        running = False
        return

    # Regex Matching    --------------------------------------------------------------------
    match = re.match(r'([NBRQK])?([a-h])?([1-8])?(x)?([a-h][1-8])',inp)

    if match:
        # Destination   --------------------------------------------------------------------
        if match.group(5) == None:
            input_error = True
            return
        elif match.group(5)[0] == None or match.group(5)[1] == None:
            input_error = True
            return
        else:  
            _destination = (match.group(5)[1], match.group(5)[0])

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
    else:
        input_error = True
        return
    # --------------------------------------------------------------------------------------

    # If you are black
    if move % 2 == 1:
        _piece += 6

    if input_error == False:
        _location = Move2Index(_location)
        _destination = Move2Index(_destination)
        previous_move = _piece, _location, _capture, _destination
        return

def interpreter(inp):
    global move, input_error
    possible_pieces = []
    if move % 2 == 1:

        # Black

        if inp[0] == 7 and inp[3][0] < 6: # Black Pawn
            if check_Spot(inp[3],7):
                input_error = True
                return
            destinations = ((inp[3][0]+1,inp[3][1]),(inp[3][0]+2,inp[3][1]))
            # print(destinations)
            # print(Index2Coord((destinations[0][1],destinations[0][0])),Index2Coord((destinations[1][1],destinations[1][0])))
            check = check_Pawn(destinations,7)
            if check == None or check[0] == None or check[1] == None:
                input_error = True
                return
            inp = inp[0],check,inp[2],inp[3]
            if inp[1] != (None,None):
                if inp[1][0] == 6 and inp[3][0] == 4:
                    move_piece(inp)
                    return
                if inp[1][0] - inp[3][0] == 1:
                    move_piece(inp)
                    return
            input_error = True

        elif inp[0] == 9: # Black Bishop
            if check_Spot(inp[3],9):
                input_error = True
                return
            possible_pieces = check_Diagonally((inp[3][0],inp[3][1]),9)
            print(possible_pieces)
            if len(possible_pieces) == 0:
                input_error = True
                return
            move_piece(possible_pieces[0])
            return

        else:
            input_error = True
            return

    else:

        # White

        if inp[0] == 1 and inp[3][0] > 1: # White Pawn
            if check_Spot(inp[3],1):
                input_error = True
                return
            destinations = ((inp[3][0]-1,inp[3][1]),(inp[3][0]-2,inp[3][1]))
            # print(destinations)
            # print(Index2Coord((destinations[0][1],destinations[0][0])),Index2Coord((destinations[1][1],destinations[1][0])))
            check = check_Pawn(destinations,1)
            if check == None or check[0] == None or check[1] == None:
                input_error = True
                return
            inp = inp[0],check,inp[2],inp[3]
            if inp[1][0] == 1 and inp[3][0] == 3:
                move_piece(inp)
                return
            elif inp[3][0] - inp[1][0] == 1:
                move_piece(inp)
                return
            input_error = True
            return

        elif inp[0] == 3: # White Bishop

            if check_Spot(inp[3],3):
                input_error = True
                return

            # Check if there already is location from inp

            possible_pieces = check_Diagonally(inp[3],3)
            if len(possible_pieces) == 0:
                input_error = True
                return
            elif len(possible_pieces) == 1:
                print(possible_pieces[0])
                inp = inp[0],possible_pieces[0],inp[2],inp[3]
                move_piece(inp)
            else:
                input_error = True
                return
            return

        else:
            input_error = True
            return



def move_piece(inp):
    global real_board, piece_dictionary

    real_board[inp[1][0]][inp[1][1]] = 0
    real_board[inp[3][0]][inp[3][1]] = inp[0]


def print_input_error():
    print("\nPlease make sure your input follows the algebraic notation rules.\n")

# Converts a tuple [int,int], to readable board coordinate.
def Index2Coord(row_column):
    if row_column[0] > 7 or row_column[0] < 0: return "Bruh, Index2Coord(*row_column), 0 ≤ row ≤ 7"
    if row_column[1] > 7 or row_column[1] < 0: return "Bruh2, Index2Coord(row_*column), 0 ≤ column ≤ 7"
    return f"{chr(row_column[0] + 97)}{row_column[1]+1}"

# Other way around.
def Coord2Index(row_column):
    if len(row_column) != 2: return "Bruh, Coord2Index(*row_column*), must be 2 characters"
    r = ord(row_column[0]) - 97 # Row
    c = int(row_column[1]) - 1 # Column
    if r > 7 or r < 0: return "Bruh, Coord2Index(*row_column), first char must be a-h only"
    if c > 7 or c < 0: return "Bruh, Coord2Index(row_*column), second char must be 0 ≤ row ≤ 7"
    return r,c

# Converts the what I call "algebraic index" or "move" to index.
# Specifically for the parser.
def Move2Index(row_column):
    if row_column == None:
        return None,None
    elif row_column[0] == None:
        return None,None
    elif row_column[1] == None:
        return None,None
    
    r = int(row_column[0]) - 1          # Row
    c = int(ord(row_column[1]) - 97)    # Column
    c = 7-c
    if r > 7 or r < 0: return None,None
    if c > 7 or c < 0: return None,None
    return r,c


def ForwardThenBackward(x,y): # 2018 LeBron fr
    _list = [0,1,2,3,4,5,6,7]
    e = _list[x+1:]
    w = list(reversed(_list[:x]))
    n = _list[y+1:]
    s = list(reversed(_list[:y]))
    return e,w,n,s

def DiagonalFTB(y,x):
    _list = [0,1,2,3,4,5,6,7]
    ne = _list[x+1:x+min(7-x,7-y)+1]
    nw = list(reversed(_list[x-min(x,7-y):x]))
    se = _list[x+1:x+min(7-x,y)+1]
    sw = list(reversed(_list[x-min(x,y):x]))
    return ne, nw, se, sw

def check_Spot(destination, piece):
    global real_board
    # print(destination)
    if real_board[destination[0]][destination[1]] == piece:
        return True
    else:
        return False

def check_Spot_4_Any(destination):
    global real_board
    if real_board[destination[0]][destination[1]] != 0:
        return True
    else:
        return False
    
def check_PieceSide(piece):
    global real_board, move, piece_dictionary
    p = piece_dictionary[piece]
    if move % 2 == 1:                   # For black=
        if p.SIDE == True: return  True # Then take.
        else:              return False # Dont take.
    else:                               # For white=
        if p.SIDE == False:return  True # Then take.
        else:              return False # Dont take.

def return_Spot(destination):
    global real_board
    return real_board[destination[0]][destination[1]]

def check_Straight(destination, piece): # Calm down python
    global real_board
    spots = ForwardThenBackward(destination[0],destination[1])
    possible_pieces = []
    for horizontal in spots[0:2]:
        for x in horizontal:
            if check_Spot((destination[0],x),piece):
                possible_pieces += [(destination[0],x)]
                break
            elif check_Spot_4_Any((destination[0],x)) != True:
                continue
            else: break
    for vertical in spots[2:]:
        for y in vertical:
            if check_Spot((y,destination[1]),piece):
                possible_pieces += [(y,destination[1])]
                break
            elif check_Spot_4_Any((y,destination[1])) != True:
                continue
            else: break
    return possible_pieces

def check_Diagonally(destination, piece): # I DONT CARE
    global real_board
    spots = DiagonalFTB(destination[0],7-destination[1])
    print(spots)
    print(destination)
    possible_pieces = []
    for positive in spots[0:2]:
        if len(positive) == 0:
            continue
        index = 1
        for p in positive:
            check = destination[0]+index,p
            if check_Spot(check,piece):
                possible_pieces += [check]
                break
            elif check_Spot_4_Any(check) == True:
                break
            #print(check,index)
            index += 1
        # Next loops should like this loop
        # loop first two lists in 'spots' individually

    for negative in spots[2:]:
        if len(negative) == 0:
            continue
        index = 1
        for n in negative:
            check = destination[0]-index,n
            if check_Spot(check,piece):
                possible_pieces += [check]
                break
            elif check_Spot_4_Any(check) == True:
                break
            print(check,index)
            index += 1
    return possible_pieces

def check_Pawn(destinations, piece):
    global real_board
    for destination in destinations:
        if check_Spot(destination,piece):
            return destination

def flip_board():
    global real_board
    real_board.reverse()
    for x in real_board:
        x.reverse()

def board():
    global real_board, move, piece_dictionary
    # cheeky. Also dont reverse maybe if multiplayering later idk
    r = 8
    if move % 2 == 0:
        flip_board()
    line = ""
    for row in real_board:
        c = 0
        if move % 2 == 0:
            line += f"{str(r)}  "
        else:
            line += f"{str(9-r)}  "
            
        for column in row:
            line += "|"
            if (r-c) % 2 == 0:
                if column == 0:
                    line += f"===="
                else:
                    line += f"={piece_dictionary[column].icon} ="
            else:
                if column == 0:
                    line += f"    "
                else:
                    line += f" {piece_dictionary[column].icon}  "
            c += 1
        line += "|\n\n"
        r -= 1
    
    if move % 2 == 0:
        line += "     a    b    c    d    e    f    g    h\n\n"
        flip_board()
    else:
        line += "     h    g    f    e    d    c    b    a\n\n"
        
    return line

# def print_previous(inp):
#     #return f"({inp[0]},{inp[1][0],7-inp[1][1]},{inp[2],inp[3]})"
#     #return f"{inp[1][1]}"
#     return inp

piece_dictionary = {0   : piece(    " ",    None,   None,   "Empty"         ),
                    1   : piece(    "♟",   True,   1,      "White Pawn"    ),
                    2   : piece(    "♞",   True,   3,      "White Knight"  ),
                    3   : piece(    "♝",   True,   3,      "White Bishop"  ),
                    4   : piece(    "♜",   True,   5,      "White Rook"    ),
                    5   : piece(    "♛",   True,   9,      "White Queen"   ),
                    6   : piece(    "♚",   True,   None,   "White King"    ),
                    7   : piece(    "♙",   False,  1,      "Black Pawn"    ),
                    8   : piece(    "♘",   False,  3,      "Black Knight"  ),
                    9   : piece(    "♗",   False,  3,      "Black Bishop"  ),
                    10  : piece(    "♖",   False,  5,      "Black Rook"    ),
                    11  : piece(    "♕",   False,  9,      "Black Queen"   ),
                    12  : piece(    "♔",   False,  None,   "Black King"    ),
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

# DELETE LATER DELETE LATER DELETE LATER DELETE LATER DELETE LATER DELETE LATER DELETE LATER DELETE LATER
real_board = [
    [10,8,9,11,12,9,8,10],
    [7,7,7,0,0,7,7,7],
    [0,0,0,0,0,0,0,0],
    [0,0,0,7,7,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0],
    [1,1,1,0,0,1,1,1],
    [4,2,3,5,6,3,2,4]
    ]

# temp = check_Diagonally((1,3),3)
# print(Index2Coord((3,1)))
# if len(temp) == 0:
#     print("None")
# else:
#     print(Index2Coord((temp[0][0],temp[0][1])))

# DELETE LATER DELETE LATER DELETE LATER DELETE LATER DELETE LATER DELETE LATER DELETE LATER DELETE LATER

flip_board()
move = 0 
move_history = []
running = True
input_ = ""
previous_move = ""
input_error = False

# Parse
# Check
# Repeat

while running:
    if input_error:
        print_input_error()
    if move % 2 == 0:
        print("\n\n\nTurn: White,")
    else:
        print("\n\n\nTurn: Black,")
    print("Move:",move+1,"\n")

    # if move > 0 and previous_move != "":
    #     print("Previous:",input_, f"{print_previous(previous_move)}","\n\n")
    # else:
    #     print("\n")       For some reason I can't get previous_move to actually update
        
    print(board())
    input_ = input("Enter your move:  \n")
    parser(input_)
    while input_error == True:
        print_input_error()
        input_ = input("Enter your move:  \n")
        parser(input_)
    
    interpreter(previous_move)

    if previous_move != None and previous_move != "" and input_error == False:
        move = move + 1

# Both Straight and Diagonal methods assume destination
# is already free or ready to take.

# TODO: Tahiti
# Just remembered that i cant let people move pieces that will leave
# themselves in check. So simple way to fix this is to use the
# horizontal and vertical checks.
# ONLY do these checks when you move a piece that has a straight
# and clear view of the king.
# If you move a piece on the N, E, S, or W squares, do straight.
# Otherwise for NE, NW, SE, and SW squares, do diagonal.

# Basically,
# 1. check king relativity when you move a piece.
# 2. If king in sight, move piece temporarily.
# 3. Do the check
# 4. Hooray!
# 5. If found opponent piece doesn't do check, return
# 6. If piece moves moves within sight of king from found piece, return
# 7. Otherwise, return the piece and print knee surgery

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
