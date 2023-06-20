import random
import time
import ChessWeight as cw
from ChessEngine import GameState
from random import getrandbits

#import pickle
gs=GameState()
pieceScore={"K":0,"Q":10,'R':5,'B':3,"N":3,'p':1,'-':0}

piecePositionScores={
    "wN": cw.knightScores,
    'bN': cw.knightScores,
    'wB': cw.bishopsScoresw,
    'bB': cw.bishopsScoresb,
    'wQ': cw.queensScorew,
    'bQ':cw.queensScoreb,
    'wR': cw.rooksScorew,
    'bR': cw.rooksScoreb,
    'wp': cw.pawnScoresw,
    'bp': cw.pawnScoresb,
    'wK': cw.kingsScorew,
    'bK': cw.kingsScoreb
}


CHECKMATE= 10000
STALEMATE=0
global DEPTH, MAX_DEPTH
DEPTH=2
MAX_DEPTH=4
global killer_moves_white,killer_moves_black
killer_moves_white = [[None, None] for _ in range(DEPTH+10)]  # maintain a list of killer moves for each depth for white
killer_moves_black = [[None, None] for _ in range(DEPTH+10)]  # maintain a list of killer moves for each depth for black
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
def findBestMove(gs, validMoves,returnQueue,Zorbist_Hash):
    global nextMove, counter, DEPTH
    counter=0
    moveLogForDepthInc= len(gs.moveLog)
    if moveLogForDepthInc >49:
        DEPTH=4
        #trigger_end_game() Not implemented yet
    elif moveLogForDepthInc > 25:
        DEPTH=4
    elif moveLogForDepthInc>12:
        DEPTH=4
        trigger_mid_game(moveLogForDepthInc)
    nextMove=None
    
    alpha_beta_search(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1,Zorbist_Hash)
    #random.shuffle(validMoves)
    """if gs.whiteToMove:
        #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1)
        iterativeDeepening(gs,validMoves,(1 if gs.whiteToMove else -1),Zorbist_Hash)
        #findMoveKillerMoveHeuristic(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1)
    else:
        #iterativeDeepening(gs,validMoves,(1 if gs.whiteToMove else -1))
        #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1,Zorbist_Hash)
        #findMoveNegaMax(gs,validMoves,MAX_DEPTH,1 if gs.whiteToMove else -1)
        findMoveKillerMoveHeuristic(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)"""
    #findMoveNegaMax(gs,validMoves,DEPTH, 1 if gs.whiteToMove else -1)
    #iterativeDeepening(gs,validMoves,(1 if gs.whiteToMove else -1), Zorbist_Hash)
    #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1)
    #nullMoveHeuristicNegaMax(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1) 
    #findMoveNegaMaxAlphaBetaTEST(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1)
    #returnQD={"nextMove":nextMove,'table':Zorbist_Hash.transpositionTable,'zorb':Zorbist_Hash.zorbistTable}
    returnQD={'nextMove':nextMove}
    returnQueue.put(returnQD)
    #returnQueue.put(nextMove)
    #print(len(Zorbist_Hash1.transpositionTable))
    #Zorbist_Hash.transpositionTable={}
    print(counter, 'Moves Calculated')

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
    validMoves.sort(key=mvv_lva_h, reverse=True)
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        nextMoves.sort(key=mvv_lva_h, reverse=True)
        score= -findMoveNegaMax(gs,nextMoves,depth-1,-turnMultiplier)
        if score >maxScore:
            maxScore= score
            if depth== DEPTH:
                nextMove= move
                print(move,score,scoreBoard(gs))
        
        gs.undoMove()
    return maxScore
def findMoveNegaMaxAlphaBetaTEST(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter, DEPTH
    counter += 1

    # Check if we reached the maximum depth, then evaluate board
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE

    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()

        # If the opponent has no valid moves after this move
        if gs.staleMate:
            score = 0
        elif gs.checkMate:
            # If the opponent is checkmated, then this move is a winning move.
            # But we need to consider whose perspective we are evaluating from.
            if gs.whiteToMove:  # It's white's turn, but black just made a move and checkmated
                score = -CHECKMATE
            else:
                score = CHECKMATE
        else:
            # Otherwise, proceed with regular alpha-beta search
            score = -findMoveNegaMaxAlphaBetaTEST(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)

        gs.undoMove()  # undo move to restore the board state

        # Alpha-beta pruning logic
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score * turnMultiplier, "depth:", depth, scoreBoard(gs), maxScore)

        if maxScore > alpha:  # pruning
            alpha = maxScore

        if alpha >= beta:
            break

    return maxScore


def findMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier, Zorbist_Hash):
    global nextMove, counter, DEPTH
    counter+=1
    if depth==0:
        return turnMultiplier * scoreBoard(gs)

    validMoves.sort(key=mvv_lva_h,reverse=True)
    maxScore=-CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        #sort_moves(nextMoves)#Sort using MVV-LVA heuristic
        nextMoves.sort(key=mvv_lva_h, reverse=True)
        score= -findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier, Zorbist_Hash)
        if score == CHECKMATE:
            if gs.checkMate:
                score=CHECKMATE
            else:
                score=0
        if score >maxScore:
            maxScore= score
            if depth== DEPTH:
                nextMove= move
                print(move,score*turnMultiplier, "depth:",depth)
                #debug()
        gs.undoMove()
        if maxScore > alpha: #pruning
            alpha=maxScore
        if alpha >=beta:
            break


    return maxScore


def findMoveKillerMoveHeuristic(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter, DEPTH, killer_moves_white, killer_moves_black
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    validMoves.sort(key=mvv_lva_h, reverse=True) # Sort using MVV-LVA Heuristic
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        nextMoves.sort(key=mvv_lva_h,reverse=True) #Sort using MVV-LVA Heuristic
        # Killer heuristic: If the current move is a killer move at this depth, give it a high priority
        if gs.whiteToMove:
            if move in killer_moves_white[depth] and move in nextMoves:
                nextMoves.insert(0, nextMoves.pop(nextMoves.index(move)))  # Move killer move to the front
        else:
            if move in killer_moves_black[depth] and move in nextMoves:
                nextMoves.insert(0, nextMoves.pop(nextMoves.index(move)))  # Move killer move to the front

        
        score = -findMoveKillerMoveHeuristic(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score == CHECKMATE:
            if gs.checkMate:
                score=CHECKMATE
            else:
                score=0
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score * turnMultiplier, "depth:", depth)
        gs.undoMove()
        if maxScore > alpha:  # Pruning
            alpha = maxScore
        if alpha >= beta:
            #If there is a beta cutoff, add that move to the killer move list
            if gs.whiteToMove:
                killer_moves_white[depth] = [killer_moves_white[depth][1], move]  # Replace the oldest move
            else:
                killer_moves_black[depth] = [killer_moves_black[depth][1], move]  # Replace the oldest move
            break

    return maxScore
def alpha_beta_search(gs,validMoves, depth, alpha, beta,turnMultiplier,Zorbist_Hash):
    global nextMove, counter, DEPTH
    counter+=1
    if depth==0:
        return turnMultiplier * scoreBoard(gs)
    #Compute hash for the current board position
    hash_key=computeHash(gs.board)
    stored_info=Zorbist_Hash.get(hash_key) if hash_key in Zorbist_Hash else None

    if stored_info is not None and stored_info['depth'] >= depth:
        # Use stored information from transposition table
        #print('hit')
        return stored_info['score']
    validMoves.sort(key=mvv_lva_h,reverse=True)
    maxScore=-CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        nextMoves.sort(key=mvv_lva_h, reverse=True)#Sort using MVV-LVA heuristic
        if gs.whiteToMove:
            if move in killer_moves_white[depth] and move in nextMoves:
                nextMoves.insert(0, nextMoves.pop(nextMoves.index(move)))  # Move killer move to the front
        else:
            if move in killer_moves_black[depth] and move in nextMoves:
                nextMoves.insert(0, nextMoves.pop(nextMoves.index(move)))  # Move killer move to the front
        score= -alpha_beta_search(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier,Zorbist_Hash)

        if score >maxScore:
            maxScore= score
            if depth== DEPTH:
                nextMove= move
                print(move,score*turnMultiplier, "depth:",depth,len(Zorbist_Hash),scoreBoard(gs))
                #Zorbist_Hash.storePosition(hash_key, maxScore, depth, nextMove)
                #debug()
        gs.undoMove()
        if maxScore > alpha: #pruning
            alpha=maxScore
        if alpha >=beta:
            #If there is a beta cutoff, add that move to the killer move list
            if gs.whiteToMove:
                killer_moves_white[depth] = [killer_moves_white[depth][1], move]  # Replace the oldest move
            else:
                killer_moves_black[depth] = [killer_moves_black[depth][1], move]  # Replace the oldest move
            break

        # After evaluating the position, store the information in the transposition table
        
        Zorbist_Hash[hash_key]={'score':maxScore,'depth':depth,'nextMove':nextMove} #Store the position in the hash table
        #Zorbist_Hash.storePosition(hash_key,0,depth,nextMove)
    return maxScore

"""
Iterative deepening with nega max alpha beta pruning with heuristics
"""
def iterativeDeepening(gs,validMoves,turnMultiplier,Zorbist_Hash):
    global nextMove, DEPTH
    for depth in range(1, DEPTH+1):
        bestMove= alpha_beta_search(gs, validMoves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1,Zorbist_Hash)

        #print(bestMove)
        print(nextMove,bestMove*(1 if gs.whiteToMove else -1))
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
        nextMoves.sort(key=mvv_lva_h,reverse=True)
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
    score= 0
    if gs.checkMate:
        if gs.staleMate:
            return STALEMATE
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    Treefold=treeFoldScore(gs)
    if Treefold:
        print('STALEMATE')
        return STALEMATE
    
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square=gs.board[row][col]
            if square != '--':
                piece_position_score=0
                if square[1]!='K':
                    piece_position_score= piecePositionScores[square][row][col]
                if square[0]=='w':
                    score+= pieceScore[square[1]]+piece_position_score
                if square[0]=='b':
                    score-=pieceScore[square[1]]+piece_position_score
                #score it positionally
                
    """if (score== CHECKMATE or score== -CHECKMATE) and not gs.inCheck():
        score=0
    else:
        score=CHECKMATE* 1 if gs.whiteToMove else -1"""
    return score

def treeFoldScore(gs):
    if len(gs.moveLog)> 8:
        moveOne=(gs.moveLog[-2],gs.moveLog[-1])
        moveTwo=(gs.moveLog[-4],gs.moveLog[-3])
        moveThree=(gs.moveLog[-6],gs.moveLog[-5])
        moveFour=(gs.moveLog[-8],gs.moveLog[-7])
        if moveOne==moveThree and moveTwo == moveFour:
            return True
    else:
        return False
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
def mvv_lva_h(move):
    if move.pieceCaptured == '--':
        return 0
    else:
        attacker_value = pieceScore[move.pieceMoved[1]]
        victim_value = pieceScore[move.pieceCaptured[1]]
        return 10 * victim_value - attacker_value
    
def trigger_mid_game(moveLogForDepthInc):
    if  moveLogForDepthInc>17:
        pass
    else:
        piecePositionScores["N"] = cw.knightScoreMidGamew
        piecePositionScores["B"] = [cw.bishopScoreMidGamew, cw.bishopScoreMidGameb]
        piecePositionScores["R"] = [cw.rookScoreMidGamew, cw.rookScoreMidGameb]
        piecePositionScores["Q"] = [cw.queenScoreMidGamew, cw.queenScoreMidGameb]
        piecePositionScores["p"] = [cw.pawnsScoreMidGamew, cw.pawnsScoreMidGameb]
        piecePositionScores["K"] = [cw.kingScoreMidGamew, cw.kingScoreMidGameb]
        print('Midgame Triggered')

def trigger_end_game(piecePositionScores):
    if not hasattr(trigger_end_game,"ran"):
        piecePositionScores["N"] = cw.knightTableEndGameW
        piecePositionScores["B"] = [cw.bishopTableEndGameW, cw.bishopTableEndGameB]
        piecePositionScores["R"] = [cw.rookTableEndGameW, cw.rookTableEndGameB]
        piecePositionScores["Q"] = [cw.queenTableEndGameW, cw.queenTableEndGameB]
        piecePositionScores["p"] = [cw.pawnTableEndGameW, cw.pawnTableEndGameB]
        piecePositionScores["K"] = [cw.kingTableEndGameW, cw.kingTableEndGameB]
        # Set attribute to indicate function has been run
        trigger_end_game.ran=True

def debug():
    """print(gs.board)
    #print(len(gs.getValidMoves()))
    print('Is king in check: ' ,gs.inCheck())
    print('Is this checkmate?',gs.checkMate)
    print('Is this stalemate?', gs.staleMate)
    print('Whos playing', (1 if gs.whiteToMove else -1))
    print('Possible moves', len(gs.getAllPossibleMoves()),'valid moves', len(gs.getValidMoves()))
    print(scoreBoard(gs))"""
    for j in gs.getValidMoves():
        print(j,"VM",scoreBoard(gs))
"""    for i in gs.getAllPossibleMoves():
        print(i,'PM')"""

"""
Zorbist Hashing function
"""
#Defining pieces and board size
pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp','--']

def initZorbistTable():
    zorbisttable = {}
    for i in range(8): # Generate random bitstrings
        for j in range(8):
            for piece in pieces:
                zorbisttable[(i,j,piece)]=getrandbits(64)
    #print('There was an init for zorbistTable')
    return zorbisttable
#Hash function
def computeHash(board):
    h=0
    for i in range(8):
        for j in range(8):
            piece= board[i][j]
            h ^=zorbistTable[(i,j,piece)]
    return h
def storePosition(hashKey, maxScore, depth, bestMove):
    Zorbist_Hash[hashKey]={
        'score': maxScore,
        'depth':depth,
        'bestMove':bestMove
    }

def retrievePosition(hashKey):
    return Zorbist_Hash.get(hashKey)
zorbistTable=initZorbistTable()