"""This is main driver file. User input and display current GameState object.
"""
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT']= '1'
import pygame as p
import ChessEngine, ChessAI,ChessWeight
import time
from multiprocessing import Process, Queue, Manager
from threading import Thread
import logging
#import queue
#from functools import lru_cache
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH= 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION= 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
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
    screen= p.display.set_mode((BOARD_WIDTH+MOVE_LOG_PANEL_WIDTH,BOARD_HEIGHT))
    clock= p.time.Clock()
    screen.fill(p.Color('white'))
    
    global moveLogFont
    moveLogFont= p.font.SysFont('Arial', 14,False,False)
    gs=ChessEngine.GameState()
    animate= False # Flag variable for when we should animate a move
    validMoves= gs.getValidMoves()
    manager=Manager()
    ZorbistHash=manager.dict()
    logging.basicConfig(filename='app1.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    moveMade= False #flag variable when a move is made
    
    loadImages() #only once before the while loop
    running= True
    sqSelected= () # no square is selected, keep track of last click 
    playerClicks=[] # 2 tuples
    gameOver= False
    playerOne=False #If a Human is playing white, then this will be true. If Ai is playing white it will be false
    playerTwo=False
    AIThinking= False
    moveFinderProcess= None
    moveUndone= False
    
    
    while running:
        humanTurn= (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type== p.QUIT:
                running = False
            #mouse handle
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location= p.mouse.get_pos()#x,y location of the mouse
                    col=location[0]//SQ_SIZE
                    row=location[1]//SQ_SIZE
                    if sqSelected == (row,col) or col >=8:#user clicks the same square twice or mouse log
                        sqSelected=()#deselect
                        playerClicks=[] # clear player clicks
                    else:
                        sqSelected= (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and humanTurn:#after 2nd click
                        move= ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                        #print(move.getChessNotation()) #Chess moves from where the piece started, to where it went
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
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking= False
                    moveUndone=True
                if e.key== p.K_r: #reset the board when R is pressed.
                    gs = ChessEngine.GameState()
                    validMoves=gs.getValidMoves()
                    sqSelected=()
                    playerClicks=[]
                    moveMade=False
                    animate=False
                    gameOver=False
                    ZorbistHash=manager.dict()
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking= False
                    moveUndone=True
                if e.key== p.K_a: #Swap player two for AI
                    if playerTwo:
                        playerTwo = False
                        print('AI On')
                    else:
                        playerTwo= True
                        print('AI Off')
        #AI move finder
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                logging.debug('If not aithinking start')
                AIThinking=True
                print("Thinking....")
                returnQueue= Queue()# used to pass data between threads
                #returnQueue=queue.Queue()
                moveFinderProcess= Process(target=ChessAI.findBestMove,args=(gs, validMoves, returnQueue, ZorbistHash))
                moveFinderProcess.start()# call findBestMove with (gs,validMoves, returnQueue)
                #AIMove=ChessAI.findBestMove(gs, validMoves) ^^ ^^
                #moveFinderThread= Thread(target=ChessAI.findBestMove(gs, validMoves, returnQueue, ZorbistHash))
                #moveFinderThread.start()
            if not moveFinderProcess.is_alive():
                print('Done thinking')
                try:
                    returnQD=returnQueue.get()
                    AIMove=returnQD["nextMove"]
                    
                    #ZorbistHash.transpositionTable=returnQD['table']
                    #ZorbistHash.zorbistTable=returnQD['zorb']
                    #print(len(ZorbistHash.transpositionTable),'ovamo')
                    #print(ChessAI.ZorbistHash.transpositionTable)
                    #AIMove,Zorbist_Hash.transpositionTable=returnqueue.get()
                    #Zorbist_Hash.transpositionTable = returnQueue.get(timeout=1)  # wait up to 1 second
                    #Zorbist_Hash.zorbistTable=returnQueue.get(timeout=1)
                    #AIMove = returnQueue.get(timeout=1)
                except returnQueue.empty():  # 
                    print("Queue.get() timed out.")
                logging.debug('Done thinking')
                #Zorbist_Hash=returnQueue.get()
                #AIMove=returnQueue.get()
                if AIMove == None:
                    AIMove= ChessAI.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade=True
                animate=True
                AIThinking= False
        
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen,gs.board, clock)
            validMoves= gs.getValidMoves()
            moveMade= False
            animate=False
            moveUndone=False
            
        drawGameState(screen,gs,validMoves,sqSelected,moveLogFont)
        if gs.checkMate or gs.staleMate or gs.treeFoldRep():
            gameOver= True  
            if gs.staleMate:
                drawEndGameText(screen,'Stalemate')
            elif gs.treeFoldRep():
                drawEndGameText(screen, 'Draw by 3fold repetition')
            else:
                if gs.whiteToMove:
                    drawEndGameText(screen,'Black wins by checkmate')
                else:
                    drawEndGameText(screen, 'White wins by checkmate')

        clock.tick(MAX_FPS)
        p.display.flip()
def drawBoard(screen):
    global colors
    colors=[p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


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

def drawGameState(screen,gs,validMoves,sqSelected,font):
    drawBoard(screen)#draw squares on board
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board) #draw pieces on top of the squares
    drawMoveLog(screen,gs,moveLogFont)
"""
draw squares on the board.
"""


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
def drawMoveLog(screen,gs,font):
    moveLogRect= p.Rect(BOARD_WIDTH,0,MOVE_LOG_PANEL_WIDTH,MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen,p.Color('black'),moveLogRect)
    moveLog=gs.moveLog
    moveTexts=[]
    #global moveLogForDepthInc
    
    
    #print(moveLogForDepthInc,'This is for depth ')
    for i in range(0,len(moveLog),2):
        moveString= str(i//2+1)+ ". "+str(moveLog[i]) +" "
        if i+1 < len(moveLog): #make sure black made a move
            moveString+= str(moveLog[i+1]) + ' '
        moveTexts.append(moveString)
    
    movesPerRow=2
    
    padding= 5
    lineSpacing=2
    textY= padding
    for i in range(0,len(moveTexts), movesPerRow):
        text=''
        for j in range(movesPerRow):
            if i + j <len(moveTexts):
                text+=moveTexts[i+j]
        textObject= font.render(text,True,p.Color('White'))
        textLocation= moveLogRect.move(padding,textY)
        screen.blit(textObject, textLocation)
        textY+=textObject.get_height() + lineSpacing
"""
Draws the move log
"""

def animateMove(move,screen,board,clock):
    global colors
    dR= move.endRow - move.startRow
    dC= move.endCol - move.startCol
    framesPerSquare= 10 #frames to move one square
    frameCount=((abs(dR)+abs(dC))*framesPerSquare)
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
            if move.isEnpassantMove:
                enPassantRow=(move.endRow +1) if move.pieceCaptured[0] =='b' else move.endRow-1
                endSquare= p.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)
        
def drawEndGameText(screen,text):
    font= p.font.SysFont('Times New Roman', 24,False,False)
    textObject= font.render(text,0,p.Color('Gray'))
    textLocation= p.Rect(0,0,BOARD_WIDTH,BOARD_HEIGHT).move(BOARD_WIDTH/2-textObject.get_width()/2,BOARD_HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject= font.render(text,0,p.Color('Black'))
    screen.blit(textObject,textLocation.move(2,2))
    


if __name__ == '__main__':
    main()
