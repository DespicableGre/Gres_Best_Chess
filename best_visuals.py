import chess
import turtle
import math

class vPiece:
	def __init__(self, t, s, i):
		self.type = t
		self.side = s
		self.position = i

squares = [
	chess.A1,	chess.B1,	chess.C1,	chess.D1,	chess.E1,	chess.F1,	chess.G1,	chess.H1,
	chess.A2,	chess.B2,	chess.C2,	chess.D2,	chess.E2,	chess.F2,	chess.G2,	chess.H2,
	chess.A3,	chess.B3,	chess.C3,	chess.D3,	chess.E3,	chess.F3,	chess.G3,	chess.H3,
	chess.A4,	chess.B4,	chess.C4,	chess.D4,	chess.E4,	chess.F4,	chess.G4,	chess.H4,
	chess.A5,	chess.B5,	chess.C5,	chess.D5,	chess.E5,	chess.F5,	chess.G5,	chess.H5,
	chess.A6,	chess.B6,	chess.C6,	chess.D6,	chess.E6,	chess.F6,	chess.G6,	chess.H6,
	chess.A7,	chess.B7,	chess.C7,	chess.D7,	chess.E7,	chess.F7,	chess.G7,	chess.H7,
	chess.A8,	chess.B8,	chess.C8,	chess.D8,	chess.E8,	chess.F8,	chess.G8,	chess.H8
]

pieces = [ "empty",
			"sprites/WhitePawn.gif","sprites/WhiteKnight.gif","sprites/WhiteBishop.gif",
			"sprites/WhiteRook.gif","sprites/WhiteQueen.gif", "sprites/WhiteKing.gif",
			"sprites/BlackPawn.gif","sprites/BlackKnight.gif","sprites/BlackBishop.gif",
			"sprites/BlackRook.gif","sprites/BlackQueen.gif", "sprites/BlackKing.gif"
]

update = False

# p: painter (Turtle())
#i: index (int)
def paint_piece(p,i):
	y = math.floor(i/8)
	x = 3-i+y*8
	p.goto(-45 - (x * 90), -45 - (3 - y) * 90)
	
	piece = board.piece_at(i)
	
	if piece == None:
		return
	
	if piece.piece_type == 0:
		p.clear()
		return
	else:
			id = piece.piece_type
			if piece.color == False:
				id += 6
			p.shape(pieces[id])

	p.stamp()
	
# Get position of selected square
def mouse_down(x, y):
	global board, s1, s2, update, painter
	_x = math.floor(x/90)+4
	_y = math.floor(y/90)+4
	i = _x+_y*8
	
	
	s2 = s1
	s1 = squares[i]
	
	move = chess.Move(s2,s1)
	
	if s1 != None and s2 != None and board.piece_at(s2) != None:
	# Get legal moves for the piece at the selected square
		legal_moves = board.legal_moves
		piece_moves = [move for move in legal_moves if move.from_square == s2]
		
		for legal_move in piece_moves:
			if move == legal_move:
				board.push(move)
				update = True
				
				# Paint the board over everything
				painter.goto(0,0)
				painter.shape("sprites/board.gif")
				painter.stamp()
				return
		
	if board.piece_at(s1) == None:
		s1 = None
	
	if s1 == s2:
		s1 = None
		s2 = None
	
	
	
	

# Variables
board = chess.Board()
visual_board = []
running = True

# Selected piece and destination, they swap places idk how to fix
s1 = None
s1 = None

# Set up the screen
wn = turtle.Screen()
wn.setup(width=720, height=720)
wn.register_shape("sprites/board.gif")

# Load all pieces
for i in range(12):
	wn.register_shape(pieces[i+1])

painter = turtle.Turtle()
painter.shape("sprites/board.gif")
painter.speed(0)
painter.penup()
painter.stamp()

for i in range(64):
	piece = board.piece_at(i)
	v_piece = None
	if piece != None:
		v_piece = vPiece(piece.piece_type, piece.color, i)
	else:
		v_piece = vPiece(0, None, i)
	visual_board.append(v_piece)

wn.onclick(mouse_down) # Register the click event listener

while running:
	# Infinite loop that doesn't freeze
	for i in range(64):
		paint_piece(painter,i)
	# Paint pieces over the new board

wn.mainloop()
