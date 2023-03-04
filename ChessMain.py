"""This is main driver file. User input and display current GameState object.
"""
import pygame as p
import ChessEngine
WIDTH= HEIGHT= 512
DIMENSION= 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS= 15 #  for animations
IMAGES= {}

'''
Init global dict of images. Only 1 execute in the main because its expensive
'''

def loadImages():
    pieces=['wR','wN','wB','wQ','wK','wp','bR','bN','bB','bQ','bK','bp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/'+ piece+'.png'),(SQ_SIZE,SQ_SIZE))
    #we can access an image in by saying 'IMAGES['wp']'

    """
    Main driver code. Input and update to graphics
    """
def main():
    p.init()
    screen= p.display.set_mode((WIDTH,HEIGHT))
    clock= p.time.Clock()
    screen.fill(p.Color('white'))
    gs=ChessEngine.GameState()
    validMoves= gs.getValidMoves()
    moveMade= False #flag variable when a move is made
    
    loadImages() #only once before the while loop
    running= True
    sqSelected= () # no square is selected, keep track of last click 
    playerClicks=[] # 2 tuples
    while running:
        for e in p.event.get():
            if e.type== p.QUIT:
                running = False
            #mouse handle
            elif e.type == p.MOUSEBUTTONDOWN:
                location= p.mouse.get_pos()#x,y location of the mouse
                col=location[0]//SQ_SIZE
                row=location[1]//SQ_SIZE
                if sqSelected == (row,col):#user clicks the same square twice
                    sqSelected=()#deselect
                    playerClicks=[] # clear player clicks
                else:
                    sqSelected= (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:#after 2nd click
                    move= ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade= True
                        sqSelected=()#reset user clicks
                        playerClicks=[]
                    else:
                        playerClicks=[sqSelected]
            #key handlers
            elif e.type== p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade= True
        if moveMade:
            validMoves= gs.getValidMoves()
            moveMade= False
            
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    """
    Responsible for all graphics in current gamestate.
    """
def drawGameState(screen,gs):
    drawBoard(screen)#draw squares on board
    drawPieces(screen,gs.board) #draw pieces on top of the squares
    
"""
draw squares on the board.
"""
def drawBoard(screen):
    colors=[p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))



    """
    draw pieces on the GameState.board
    """
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--': #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
