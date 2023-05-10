import random
import time
import ChessWeight
from ChessEngine import GameState

gs=GameState()
pieceScore={"K":0,"Q":9.5,'R':5.63,'B':3.33,"N":3.05,'p':1}

knightScores=[ [ -50, -40, -30, -30, -30, -30, -40, -50 ],
[ -40, -20,   0,   0,   0,   0, -20, -40 ],
[ -30,   0,  10,  15,  15,  10,   0, -30 ],
[ -30,   5,  15,  20,  20,  15,   5, -30 ],
[ -30,   0,  15,  20,  20,  15,   0, -30 ],
[ -30,   5,  10,  15,  15,  10,   5, -30 ],
[ -40, -20,   0,   5,   5,   0, -20, -40 ],
[ -50, -40, -30, -30, -30, -30, -40, -50 ]
]
pawnScoresw=[
    [10,10,10,10,10,10,10,10],
    [9,9,9,9,9,9,9,9],
    [7,7,7,7,7,7,7,7],
    [5,5,8,8,8,8,5,5],
    [0,0,0,5,5,0,0,0],
    [1,-1,-1,0,0,-1,-1,1],
    [5,1,1,1,1,1,1,5],
    [0,0,0,0,0,0,0,0]
    ]
pawnScoresw=[
[ 0,   0,   0,   0,   0,   0,   0,   0 ],
[ 50,  50,  50,  50,  50,  50,  50,  50 ],
[ 10,  10,  20,  30,  30,  20,  10,  10 ],
[ 5,   5,  10,  25,  25,  10,   5,   5 ],
[ 0,   0,   0,  20,  20,   0,   0,   0 ],
[ 5,  -5, -10,   1,   1, -10,  -5,   5 ],
[ 5,  10,  10, -20, -20,  10,  10,   5 ],
[ 0,   0,   0,   0,   0,   0,   0,   0 ]
]
#Just reversing the order of weight elements for black pieces
pawnScoresb=[pawnScoresw[x] for x in range(len(pawnScoresw)-1,-1,-1)]
bishopsScoresw =[ 
[ -20, -10, -10, -10, -10, -10, -10, -20 ],
[ -10,   0,   0,   0,   0,   0,   0, -10 ],
[ -10,   0,   5,  10,  10,   5,   0, -10 ],
[ -10,   5,   5,  10,  10,   5,   5, -10 ],
[ -10,   0,  10,  10,  10,  10,   0, -10 ],
[ -10,  10,  10,  10,  10,  10,  10, -10 ],
[ -10,   5,   0,   0,   0,   0,   5, -10 ],
[ -20, -10, -10, -10, -10, -10, -10, -20 ]
]
bishopsScoresb=[bishopsScoresw[x] for x in range(len(bishopsScoresw)-1,-1,-1)]

rooksScorew =[
[  0,   0,   0,   0,   0,   0,   0,   0 ],
[  5,  10,  10,  10,  10,  10,  10,   5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[  0,   -3,   0,   5,   5,   0,   -3,   0 ]
]
rooksScoreb=[rooksScorew[x] for x in range(len(rooksScorew)-1,-1,-1)]

queensScorew=[
[ -20, -10, -10,  -5,  -5, -10, -10, -20 ],
[ -10,   0,   0,   0,   0,   0,   0, -10 ],
[ -10,   0,   5,   5,   5,   5,   0, -10 ],
[  -5,   0,   5,   5,   5,   5,   0,  -5 ],
[   0,   0,   5,   5,   5,   5,   0,  -5 ],
[ -10,   5,   5,   5,   5,   5,   0, -10 ],
[ -10,   0,   5,   0,   0,   0,   0, -10 ],
[ -20, -10, -10,  -5,  -5, -10, -10, -20 ]
]
queensScoreb=[queensScorew[x] for x in range(len(queensScorew)-1,-1,-1)]

kingsScorew=[
[-30, -40, -40, -50, -50, -40, -40, -30], 
[-30, -40, -40, -50, -50, -40, -40, -30], 
[-30, -40, -40, -50, -50, -40, -40, -30], 
[-30, -40, -40, -50, -50, -40, -40, -30], 
[-20, -30, -30, -40, -40, -30, -30, -20], 
[-10, -20, -20, -20, -20, -20, -20, -10], 
[20, 20, 0, 0, 0, 0, 20, 20], 
[20, 30, 10, -1, 0, -1, 30, 20]]
kingsScoreb=[kingsScorew[x] for x in range(len(kingsScorew)-1,-1,-1)]


piecePositionScores= {"N":knightScores,
                        "B":[bishopsScoresw,bishopsScoresb],
                        "R":[rooksScorew,rooksScoreb],
                        "Q":[queensScorew,queensScoreb],
                        "p":[pawnScoresw,pawnScoresb],
                        "K":[kingsScorew,kingsScoreb]}

CHECKMATE= 10000
STALEMATE=0
global DEPTH
DEPTH=6
global KILLER_MOVE_TABLE
KILLER_MOVE_TABLE= [None]* (DEPTH +3)
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
    global nextMove, counter, DEPTH
    counter=0
    moveLogForDepthInc= len(gs.moveLog)
    if moveLogForDepthInc >50:
        DEPTH=6

    nextMove=None
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)

    #random.shuffle(validMoves)
    #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1)
    negamaxAlphaBetaKillerMoveNew(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
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
def negamaxAlphaBetaKillerMove(gs,validMoves,depth,alpha,beta):
    global nextMove, counter
    counter+=1
    if depth == 0:
        return (1 if gs.whiteToMove else -1)*scoreBoard(gs)
    maxScore= -CHECKMATE
    #Try killer move first
    killer_moves = [[] for _ in range(depth+1)]
    for move in killer_moves[depth]:
        if move in validMoves:
            validMoves.remove(move)
            gs.makeMove(move)
            nextMoves= gs.getValidMoves()
            sort_moves(nextMoves)#Sort using MVV-LVA heuristic
            score= -negamaxAlphaBetaKillerMove(gs, nextMoves, depth-1, -beta, -alpha)
            if score>maxScore:
                maxScore = score
                nextMove=move
                #print(move,score,depth)
            gs.undoMove()
            alpha= max(alpha,maxScore)
            
            if alpha >=beta:
                break
    #Try other moves
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        sort_moves(nextMoves)#Sort using MVV-LVA heuristic
        score= -negamaxAlphaBetaKillerMove(gs, nextMoves, depth-1, -beta, -alpha)
        
        if score>maxScore:
            maxScore=score
            nextMove=move
            #print(move,score,depth)
        gs.undoMove()
        alpha= max(alpha,maxScore)
        if alpha>=beta:
            #Save killer move for this depth
            killer_moves[depth].append(move)
            break
    return maxScore
def findMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove, counter
    counter+=1
    if depth==0:
        return turnMultiplier * scoreBoard(gs)
    #move ordering - implement later?
    
    maxScore=-CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        sort_moves(nextMoves)#Sort using MVV-LVA heuristic
        score= -findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
        if score >maxScore:
            maxScore= score
            if depth== DEPTH:
                nextMove= move
                print(move,score*turnMultiplier, "depth:",depth)
        gs.undoMove()
        if maxScore > alpha: #pruning
            alpha=maxScore
        if alpha >=beta:
            break
    #print(maxScore)
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
            if depth == DEPTH:
                nextMove = move
                print(move, score * turnMultiplier, "depth:", depth, "killer moves:",len(KILLER_MOVE_TABLE))
        gs.undoMove()
        if maxScore > alpha:  # pruning
            alpha = maxScore
        if alpha >= beta:
            # Store the killer move in the table for the current depth
            KILLER_MOVE_TABLE[depth] = move
            break
    return maxScore
"""
Pos score good for white, negative score is good for black
"""
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.staleMate:
        return STALEMATE
    
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
                    score+= pieceScore[square[1]] + piecePositionScore *0.16
                elif square[0]=='b':
                    score-= pieceScore[square[1]] + piecePositionScore *0.16
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
            if gs.move_value(validMoves[j])> gs.move_value(validMoves[i]):
                validMoves[i], validMoves[j]= validMoves[j], validMoves[i]