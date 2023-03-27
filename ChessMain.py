"""This is main driver file. User input and display current GameState object.
"""
import pygame as p
import ChessEngine, ChessAI

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
    animate= False # Flag variable for when we should animate a move
    validMoves= gs.getValidMoves()
    moveMade= False #flag variable when a move is made
    
    loadImages() #only once before the while loop
    running= True
    sqSelected= () # no square is selected, keep track of last click 
    playerClicks=[] # 2 tuples
    gameOver= False
    playerOne=False #If a Human is playing white, then this will be true. If Ai is playing white it will be false
    playerTwo=False 
    
    while running:
        humanTurn= (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type== p.QUIT:
                running = False
            #mouse handle
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade= True
                                animate= True
                                sqSelected=()#reset user clicks
                                playerClicks=[]
                        if not moveMade:
                            playerClicks=[sqSelected]
            #key handlers
            elif e.type== p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade= True
                    animate=False
                    gameOver=False
                if e.key== p.K_r: #reset the board when R is pressed.
                    gs = ChessEngine.GameState()
                    validMoves=gs.getValidMoves()
                    sqSelected=()
                    playerClicks=[]
                    moveMade=False
                    animate=False
                    gameOver=False
        #AI move finder
        if not gameOver and not humanTurn:
            AIMove=ChessAI.findBestMove(gs, validMoves)
            if AIMove == None:
                AIMove= ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade=True
            animate=True
            
        
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen,gs.board, clock)
            validMoves= gs.getValidMoves()
            moveMade= False
            animate=False
            
        drawGameState(screen,gs,validMoves,sqSelected)
        if gs.checkMate== True:
            gameOver= True
            if gs.whiteToMove:
                drawText(screen,'Black wins by checkmate')
            elif gs.staleMate:
                gameOver= True
                drawText(screen,'Stalemate')
            else:
                drawText(screen, 'White wins by checkmate')

        clock.tick(MAX_FPS)
        p.display.flip()
        
    """
    Highlighting squares on the board
    """
def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected != ():
        r,c=sqSelected
        if gs.board[r][c][0]== ('w'if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #highlight selected square
            s= p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #transparency value if 0 = transparent completely
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol== c:
                    screen.blit(s,(SQ_SIZE*move.endCol,SQ_SIZE*move.endRow))

"""Responsible for all graphics in current gamestate."""

def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)#draw squares on board
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board) #draw pieces on top of the squares
    
"""
draw squares on the board.
"""
def drawBoard(screen):
    global colors
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
                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    """
    Animating a move
    """
def animateMove(move,screen,board,clock):
    global colors
    dR= move.endRow - move.startRow
    dC= move.endCol - move.startCol
    framesPerSquare= 10 #frames to move one square
    frameCount=(abs(dR)+abs(dC)*framesPerSquare)
    for frame in range(frameCount+1):
        r,c=(move.startRow + dR*frame/frameCount,move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color=colors[(move.endRow+move.endCol)%2]
        endSquare= p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen,color, endSquare)
        #draw captured piece
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)
        
def drawText(screen,text):
    font= p.font.SysFont('Helvetica', 16,False,False)
    textObject= font.render(text,0,p.Color('Gray'))
    textLocation= p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2-textObject.get_width()/2,HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject= font.render(text,0,p.Color('Black'))
    screen.blit(textObject,textLocation.move(2,2))

if __name__ == '__main__':
    main()
