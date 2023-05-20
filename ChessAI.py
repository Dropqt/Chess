import random
import time
import ChessWeight as cw
from ChessEngine import GameState

gs=GameState()
pieceScore={"K":0,"Q":10,'R':5,'B':3,"N":3,'p':1}
piecePositionScores= {"N":cw.knightScores,
                        "B":[cw.bishopsScoresw,cw.bishopsScoresb],
                        "R":[cw.rooksScorew,cw.rooksScoreb],
                        "Q":[cw.queensScorew,cw.queensScoreb],
                        "p":[cw.pawnScoresw,cw.pawnScoresb],
                        "K":[cw.kingsScorew,cw.kingsScoreb]}

CHECKMATE= 10000
STALEMATE=0
global DEPTH, MAX_DEPTH
DEPTH=4
MAX_DEPTH=6
global KILLER_MOVE_TABLE
KILLER_MOVE_TABLE=  [[] for _ in range(10)]
global GAME_STAGE
GAME_STAGE=1
"""
Random Move
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]
    
"""
Find the best move based on material (MinMax without recursion)
"""
def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier= 1 if gs.whiteToMove else -1

    
    opponentMinMaxScore= CHECKMATE
    bestPlayerMove= None
    random.shuffle(validMoves)
    opponentMaxScore=0
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves= gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore= STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score=CHECKMATE
                elif gs.staleMate:
                    score=STALEMATE
                else:
                    score= -turnMultiplier*scoreMaterial(gs.board)
                if score >opponentMaxScore:
                    opponentMaxScore=score
                gs.undoMove()
        if opponentMinMaxScore > opponentMaxScore:
            opponentMinMaxScore=opponentMaxScore
            bestPlayerMove= playerMove
        gs.undoMove()
    return bestPlayerMove

""" 
Helper method for making the first recursive call
"""
def findBestMove(gs, validMoves,returnQueue):
    global nextMove, counter, DEPTH, GAME_STAGE
    counter=0
    moveLogForDepthInc= len(gs.moveLog)
    if moveLogForDepthInc >60:
        DEPTH=5
    if moveLogForDepthInc>13:
        DEPTH=4
        trigger_mid_game(piecePositionScores, GAME_STAGE)
    nextMove=None
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)

    #random.shuffle(validMoves)
    if gs.whiteToMove:
        findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1)
        #iterativeDeepening(gs,validMoves,(1 if gs.whiteToMove else -1))
    else:
        #negamaxAlphaBetaKillerMoveNew(gs, validMoves, MAX_DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
        iterativeDeepening(gs,validMoves,(1 if gs.whiteToMove else -1))
        #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1)
    #negamaxAlphaBetaKillerMoveNew(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    #iterativeDeepening(gs,validMoves,(1 if gs.whiteToMove else -1))
    #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1)
    #nullMoveHeuristicNegaMax(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1) 
    print(counter, 'counter')
    returnQueue.put(nextMove)
    

def findMoveMinMax(gs,validMoves,depth,whiteToMove):
    global nextMove
    if depth ==0:
        return scoreMaterial(gs.board)
    
    if whiteToMove: #maximize
        maxScore= -CHECKMATE
        for move in validMoves: 
            gs.makeMove(move)
            nextMoves=gs.getValidMoves()
            score=findMoveMinMax(gs, nextMoves, depth-1, False)
            if score >maxScore:
                maxScore= score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
        
    else:
        minScore=CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves= gs.getValidMoves()
            score=findMoveMinMax(gs, nextMoves, depth -1, True)
            if score<minScore:
                minScore=score
                if depth==DEPTH:
                    nextMove=move
            gs.undoMove()
        return minScore
    
def findMoveNegaMax(gs,validMoves,depth,turnMultiplier):
    global nextMove,counter
    counter+=1
    if depth==0:
        return turnMultiplier * scoreBoard(gs)
    maxScore=-CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        score= -findMoveNegaMax(gs,nextMoves,depth-1,-turnMultiplier)
        if score >maxScore:
            maxScore= score
            if depth== DEPTH:
                nextMove= move
                
        
        gs.undoMove()
    return maxScore
def negamaxAlphaBetaKillerMove(gs,validMoves,depth,alpha,beta,turnMultiplier):
    #This is for iterative deepening since the code changes a bit
    global nextMove, counter, KILLER_MOVE_TABLE,depth_it,nextMove_it
    bestMove=None
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    killer_move = KILLER_MOVE_TABLE[depth] if depth < len(KILLER_MOVE_TABLE) else None

    # Move the killer move to the front of the validMoves list
    if killer_move is not None and killer_move in validMoves:
        validMoves.remove(killer_move)
        validMoves.insert(0, killer_move)

    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        sort_moves(nextMoves)  # Sort using MVV-LVA heuristic
        score= -negamaxAlphaBetaKillerMove(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            nextMove_it=move
            #print(move, score * turnMultiplier, "depth:", depth, "killer moves:",len(KILLER_MOVE_TABLE))
        gs.undoMove()
        if maxScore > alpha:  # pruning
            alpha = maxScore
        if alpha >= beta:
        # Store the killer move in the table for the current depth
            KILLER_MOVE_TABLE[depth] = move
            break
    return maxScore
def findMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove, counter
    STALEMATE
    counter+=1
    if depth==0:
        return turnMultiplier * scoreBoard(gs)
    #move ordering - implement later?
    
    maxScore=-CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        #sort_moves(nextMoves)#Sort using MVV-LVA heuristic
        nextMoves.sort(key=lambda move: (get_values(move.pieceCaptured[1]),-get_values(move.pieceMoved[1])), reverse= True)
        score= -findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
        if score >maxScore:
            maxScore= score
            if depth== DEPTH:
                nextMove= move
                print(move,score*turnMultiplier, "depth:",depth, scoreBoard(gs))
                #debug()
        gs.undoMove()
        if maxScore > alpha: #pruning
            alpha=maxScore
        if alpha >=beta:
            break


    return maxScore


def negamaxAlphaBetaKillerMoveNew(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove, counter, KILLER_MOVE_TABLE
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    killer_move = KILLER_MOVE_TABLE[depth] if depth < len(KILLER_MOVE_TABLE) else None

    # Move the killer move to the front of the validMoves list
    if killer_move is not None and killer_move in validMoves:
        validMoves.remove(killer_move)
        validMoves.insert(0, killer_move)

    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        sort_moves(nextMoves)  # Sort using MVV-LVA heuristic
        score = -negamaxAlphaBetaKillerMoveNew(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == MAX_DEPTH:
                nextMove = move
                print(move, score*turnMultiplier , "depth:", depth, scoreBoard(gs))
        gs.undoMove()
        if maxScore > alpha:  # pruning
            alpha = maxScore
        if alpha >= beta:
            # Store the killer move in the table for the current depth
            #if len(KILLER_MOVE_TABLE[depth])
            KILLER_MOVE_TABLE[depth] = move
            break
    return maxScore

"""
Iterative deepening with nega max alpha beta pruning with heuristics
"""
def iterativeDeepening(gs,validMoves,turnMultiplier):
    global nextMove,nextMove_it, DEPTH
    for depth in range(1, DEPTH+1):
        bestMove= findMoveNegaMaxAlphaBeta(gs, validMoves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
        #print(bestMove)
        if bestMove== (10000*(1 if gs.whiteToMove else -1)):
            return bestMove
        print(nextMove,bestMove)
        #debug()
    return bestMove
def nullMoveHeuristicNegaMax(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove, counter
    counter+=1
    if depth==0:
        return turnMultiplier*scoreBoard(gs)
    R=1 #reduce search depth
    #Null Move Heuristic
    n_move='--'
    if depth >=2 and  not gs.inCheck(): #Only consider null moves at certain depth
        gs.makeNullMove()
        score=-nullMoveHeuristicNegaMax(gs,validMoves,depth - 1 - R,alpha,beta,turnMultiplier)
        gs.undoNullMove()
        if score>=beta:
            return beta
    
    maxScore= -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves= gs.getValidMoves()
        sort_moves(nextMoves)
        score= -nullMoveHeuristicNegaMax(gs,nextMoves,depth-1, -beta,-alpha, -turnMultiplier)
        gs.undoMove()
        if score > maxScore:
            maxScore= score
            if depth == DEPTH:
                nextMove=move
        if maxScore > alpha:
            alpha= maxScore
        if alpha >=beta:
            break
    return maxScore
        
"""
Pos score good for white, negative score is good for black
"""
def scoreBoard(gs):
    if gs.staleMate:
        return STALEMATE
    elif gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    
    score= 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square=gs.board[row][col]
            if square != '--':
                #score it positionally
                piecePositionScore=0
                if square[1]== 'N':
                    piecePositionScore= piecePositionScores['N'][row][col]
                if square[1]=='B':
                    #checking if the piece is black or white to check list within a list.
                    if square[0]=='w':
                        piecePositionScore= piecePositionScores['B'][0][row][col]
                    else:
                        piecePositionScore= piecePositionScores['B'][1][row][col]
                if square[1]=='R':
                    if square[0]=='w':
                        piecePositionScore= piecePositionScores['R'][0][row][col]
                    else:
                        piecePositionScore= piecePositionScores['R'][1][row][col]
                if square[1]=='Q':
                    if square[0]=='w':
                        piecePositionScore= piecePositionScores['Q'][0][row][col]
                    else:
                        piecePositionScore= piecePositionScores['Q'][1][row][col]
                if square[1]=='K':
                    if square[0]== 'w':
                        piecePositionScore= piecePositionScores['K'][0][row][col]
                    else:
                        piecePositionScore= piecePositionScores['K'][1][row][col]
                if square[1]=='p':
                    if square[0]=='w':
                        piecePositionScore= piecePositionScores['p'][0][row][col]
                    else:
                        piecePositionScore= piecePositionScores['p'][1][row][col]
                if square[0] == 'w':
                    score+= pieceScore[square[1]] + piecePositionScore *0.2
                elif square[0]=='b':
                    score-= pieceScore[square[1]] + piecePositionScore *0.2
    return score
"""
Score the board based on material
"""
def scoreMaterial(board):
    score= 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score+= pieceScore[square[1]]
            elif square[0]=='b':
                score-= pieceScore[square[1]]
    
    return score

    """
    Sort moves
    """
def sort_moves(validMoves):
    for i in range(len(validMoves)):
        for j in range(i+1, len(validMoves)):
            if gs.move_value(validMoves[j],gs.board,gs)> gs.move_value(validMoves[i],gs.board,gs):
                validMoves[i], validMoves[j]= validMoves[j], validMoves[i]

def get_values(piece):
    pieceScore={"K":0,"Q":10,'R':5,'B':3,"N":3,'p':1,'--':0,'-':0}
    if piece in pieceScore:
        return pieceScore[piece]
def trigger_mid_game(piecePositionScores,game_stage):
    global GAME_STAGE
    gameFlag=False
    game_stage=GAME_STAGE
    
    if gameFlag ==True:
        pass
    else:
        piecePositionScores= {"N":cw.knightTableMidGamew,
                        "B":[cw.bishopTableMidGamew,cw.bishopTableMidGameb],
                        "R":[cw.rookTableMidGamew,cw.rookTableMidGameb],
                        "Q":[cw.queenTableMidGamew,cw.queenTableMidGameb],
                        "p":[cw.pawnTableMidGamew,cw.pawnTableMidGameb],
                        "K":[cw.kingTableMidGamew,cw.knightTableMidGameb]}
        GAME_STAGE=2
        gameFlag=True
        print('Midgame Triggered')
        return piecePositionScores
def debug():
    print(gs.board)
    #print(len(gs.getValidMoves()))
    print('Is king in check: ' ,gs.inCheck())
    print('Is this checkmate?',gs.checkMate)
    print('Is this stalemate?', gs.staleMate)
    print('Whos playing', gs.whiteToMove)
    print('Possible moves', len(gs.getAllPossibleMoves()),'valid moves', len(gs.getValidMoves()))
    for j in gs.getValidMoves():
        print(j,"VM")
"""for i in gs.getAllPossibleMoves():
        print(i,'PM')"""
