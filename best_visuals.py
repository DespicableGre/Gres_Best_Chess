import turtle as trtl
import best_chess

def Index2Pos(x,y):
    return x * 96 - 336, y * 96 - 336

def ReturnDrawer():
    global drawer
    drawer.shape("Pieces/None.gif")
    drawer.goto(Index2Pos(0,0))


drawer = trtl.Turtle()
wn = trtl.Screen()
wn.register_shape("board.gif")

for i in range(13):
    wn.register_shape(best_chess.piece_dictionary[i].sprite)

drawer.penup()
drawer.hideturtle()
drawer.speed(0)

drawer.shape("board.gif")
drawer.stamp()

drawer.shape("Pieces/WhitePawn.gif")

drawer.goto(Index2Pos(1,1))
drawer.stamp()
drawer.goto(Index2Pos(0,1))
drawer.stamp()
drawer.goto(Index2Pos(2,1))
drawer.stamp()
drawer.goto(Index2Pos(3,1))
drawer.stamp()

ReturnDrawer()

wn.mainloop()