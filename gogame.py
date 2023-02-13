import go 
from ursina import *

app = Ursina()



BOARDOBJ = "board.obj"
BOARDTEXTURE = "boardtexture.png"

PIECEOBJ = "piece.obj"
WHITETEXTURE = "white.png"
BLACKTEXTURE = "black.png"


whitepieces = []
blackpieces = []

TOPRIGHT = (-0.5,0.5)
BOTTOMLEFT = (-0.5,0.5)

#need to remove this
xrange = (-0.5,0.5)
yrange = (-0.5,0.5)

xlen = xrange[1]-xrange[0]
ylen = yrange[1]-yrange[0]

boardxrange = (xrange[0]+50*xlen/820,xrange[1]-50*xlen/820)
boardyrange = (xrange[0]+50*ylen/820,xrange[1]-50*ylen/820)

boxsize = 40*xlen/820


turn = 0

color2texture = {go.BLACK:BLACKTEXTURE,go.WHITE:WHITETEXTURE}

class Stone(go.Stone):
    def __init__(self,board,point,color):
        super(Stone,self).__init__(board,point,color)
        self.coords = (boardxrange[0]+self.point[0]*40/820,boardyrange[0]+self.point[1]*40/820)
        self.item = None
        self.x = self.coords[0]
        self.y = 0.5
        self.z = self.coords[1]
        # print(self.x,self.z,self.coords)
        self.draw()

    def draw(self):
##        piece = Entity(parent=board.cube,model="cube",
##                       position=(self.x,self.y+0.1,self.z),
##                       scale=(0.04,0.04,0.1),rotation=(90,0,0),texture=color2texture[self.color])
        piece = Entity(parent=board.cube,model=PIECEOBJ,
                       position=(self.x,self.y+0.1,self.z),
                       scale=(0.1,0.1,0.1),rotation=(90,0,0),double_sided=True,texture=BLACKTEXTURE)
        piece.rotation_x += 30
        self.item = piece
        
    def remove(self):
        self.item.enabled = False
        super(Stone,self).remove()


class Board(go.Board):
    def __init__(self):
        super(Board, self).__init__()
        self.bottomleft = BOTTOMLEFT
        self.topright = TOPRIGHT
        self.cube = self.draw()

    def draw(self):
        cube = Entity(parent=rotation_resetter, model=BOARDOBJ, scale=(10, 1, 10), collider='box', texture=BOARDTEXTURE,
                      on_click=action)
        rotation_resetter.rotation_x -= 40
        return cube



def nearestJunction(x,y):
    x -= boardxrange[0]
    y -= boardyrange[0]
    n1 = round(x/boxsize)
    n2 = round(y/boxsize)


    
    return n1,n2

def action():
    
    '''clicked on the board'''
    # print(mouse.point)
    if(mouse.point[1]==0.5):
        # clicked on the correct face of board
        x,y,z = mouse.point
        print(x,y,z)
        if x<boardxrange[0] or z<boardyrange[0]:
            return

        # clicked inside game areaa
        n1,n2 = nearestJunction(x,z)
        print("hey:",n1,n2)
        stone = board.search(point=(n1,n2))
        if stone:
            # There's already a stone at that postion
            return
        added_stone = Stone(board,(n1,n2),board.turn())
        board.update_liberties(added_stone)


        
        
##        piece = Entity(parent=cube,model="go.obj",position=(mouse.point[0],mouse.point[1]+0.1,mouse.point[2]),scale=(0.004,0.004,0.05),rotation=(90,0,0),texture="texture1.png")
        
##        piece = Entity(parent=cube,model=Cylinder(resolution=14,direction=(0,0,1)),position=(mouse.point[0],mouse.point[1]+0.1,mouse.point[2]),scale=(0.04,0.04,0.4),rotation=(90,0,0),texture="texture1.png")




        # COLOR = board.turn()
        # piece = Entity(parent=cube,model="cube",position=(x,y+0.1,z),scale=(0.04,0.04,0.1),rotation=(90,0,0),texture=color2texture[COLOR])



def input(key):
    if key == "q":
        quit()

def update():
    rotation_resetter.rotation_x += 100 * (held_keys['a'] - held_keys['d']) * time.dt
    rotation_resetter.rotation_z += 100 * (held_keys['w'] - held_keys['s']) * time.dt

    board.cube.rotation = board.cube.world_rotation
    rotation_resetter.rotation = (0,0,0)



if __name__ == "__main__":
    rotation_resetter = Entity()
    board = Board()
    EditorCamera()
    app.run()


