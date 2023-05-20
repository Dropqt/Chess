import copy
import time
import ChessWeight as cw
"""Class stores all information about the current chess game.
    And checking for valid moves for current GameState, and move log.
"""
class GameState():
    def __init__(self):
        # board 8x8 2D list, 2 characters, 1st char color of piece, 2nd char is type of piece
        # '--' is empty space with no piece

        
        self.board = [
            ['bR','--','bB','bQ','bK','--','bN','bR'],
            ['bp','bp','bp','bp','--','bp','bp','bp'],
            ['--','--','bN','--','--','--','--','--'],
            ['--','--','bB','--','bp','--','--','--'],
            ['--','--','wB','--','wp','--','--','--'],
            ['--','--','--','--','--','wN','--','--'],
            ['wp','wp','wp','wp','--','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','--','--','wR']]
        """self.board = [
            ['bQ','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','bK'],
            ['--','--','--','--','--','bR','bp','--'],
            ['--','--','--','--','--','--','wp','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','wp','wp'],
            ['--','--','--','--','--','--','--','wK']]"""
        """self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']]"""


        
        self.whiteToMove= True
        self.moveLog=[]
        self.moveFunctions={'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                            'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.checkMate= False
        self.staleMate= False
        self.draw=False
        self.enpassantPossible=() #coordinates for square where en passant is possible
        self.enpassantPossibleLog=[self.enpassantPossible]
        self.currentCastlingRight= CastleRights(True,True,True,True)
        self.castleRightLog=[CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]
        
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]= '--'
        self.board[move.endRow][move.endCol]= move.pieceMoved
        self.moveLog.append(move)# log the move for undo purposes or history
        self.whiteToMove= not self.whiteToMove # swap players
        #update kings location if moved
        if move.pieceMoved=='wK':
            self.whiteKingLocation=(move.endRow,move.endCol)
        elif move.pieceMoved=='bK':
            self.blackKingLocation=(move.endRow,move.endCol)
        #Pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]= move.pieceMoved[0]+'Q'
        
        #Enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol]= '--' # capturing the pawn
        #update enpassant possible variable
        if move.pieceMoved[1]=='p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advance
            self.enpassantPossible=((move.startRow+move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible=()
        
        #Castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:# kingside castle move
                self.board[move.endRow][move.endCol-1]= self.board[move.endRow][move.endCol+1]#moves the rook into its new square
                self.board[move.endRow][move.endCol+1]='--' #erase old rook
            else:#queenside castle move
                self.board[move.endRow][move.endCol+1]= self.board[move.endRow][move.endCol-2]#moves the rook
                self.board[move.endRow][move.endCol-2]= '--'
        #update castling rights when its a rook or a king move
        self.enpassantPossibleLog.append(self.enpassantPossible)
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))
        
    def makeNullMove(self):
        move='--'
        self.whiteToMove= not self.whiteToMove
        """
        Undo the last move made
        """
    def undoNullMove(self):
        self.staleMate= False
        self.checkMate= False
        self.treeFoldRep= False
        self.whiteToMove= not self.whiteToMove
    def undoMove(self):
        if len(self.moveLog) != 0: #check if there are moves
            move= self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove= not self.whiteToMove
            #update the king's position if needed
            if move.pieceMoved=='wK':
                self.whiteKingLocation=(move.startRow, move.startCol)
            elif move.pieceMoved=='bK':
                self.blackKingLocation=(move.startRow, move.startCol)
            #undo enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol]= '--' #leave landing square blank
                self.board[move.startRow][move.endCol]= move.pieceCaptured
            self.enpassantPossibleLog.pop()
            self.enpassantPossible=self.enpassantPossibleLog[-1]
                
                
            #undo castling rights
            self.castleRightLog.pop() #undo last log 
            """
            self.currentCastlingRight = self.castleRightLog[-1] #set current castle rights to last one
            """
            castleRights=copy.deepcopy(self.castleRightLog[-1])
            self.currentCastlingRight=castleRights
            #undo castle move
            if move.isCastleMove:
                if move.endCol-move.startCol == 2:#kingside
                    self.board[move.endRow][move.endCol+1]= self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1]= '--'
                else:       #queenside
                    self.board[move.endRow][move.endCol-2]= self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1]= '--'
        self.staleMate= False
        self.checkMate= False
        """
        Update the castle rights given the move
        """
    def updateCastleRights(self,move):
        if move.pieceMoved=='wK':
            self.currentCastlingRight.wks=False
            self.currentCastlingRight.wqs=False
            
        elif move.pieceMoved=='bK':
            self.currentCastlingRight.bks=False
            self.currentCastlingRight.bqs=False
            
        elif move.pieceMoved=='wR':
            if move.startRow==7: #White side
                if move.startCol==0: #left rook
                    self.currentCastlingRight.wqs=False
                elif move.startCol==7: #right rook
                    self.currentCastlingRight.wks=False
                    
        elif move.pieceMoved =='bR':
            if move.startRow==0: #Black side
                if move.startCol==0: #left rook
                    self.currentCastlingRight.bqs=False
                elif move.startCol==7:#Right rook
                    self.currentCastlingRight.bks=False
                
    
    #all moves considering checks
    def getValidMoves(self):
        tempEnpassantPossible= self.enpassantPossible
        tempCastleRights= CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                    self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)#copy the current castling rights
        #1. Generate all possible moves
        moves=self.getAllPossibleMoves()
        invalidMoves=[]
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)
        #2. For each move, make the move
        for i in range(len(moves)-1,-1,-1): #when removing from a list, go backwards
            self.makeMove(moves[i])
            #3. Generate all opponents moves
            #4. For each of your opponents moves, see if they attack your king
            self.whiteToMove= not self.whiteToMove
            if self.inCheck():
                invalidMoves.append(moves[i])
                #moves.remove(moves[i]) #5. if they do attack your king, its not a valid move
            self.whiteToMove= not self.whiteToMove
            self.undoMove()
        for move in invalidMoves:
            moves.remove(move)
        if len(moves)== 0: #either checkmate or stalemate
            if not self.inCheck():
                self.staleMate= True
            else:
                self.checkMate= True
        else:
            self.checkMate= False
            self.staleMate= False
        self.enpassantPossible= tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves





    """Check if current player is in check
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
        
    """Check if the enemy can attack the square r,c
    """
    def squareUnderAttack(self,r,c):
        self.whiteToMove= not self.whiteToMove #switch to opponents turn
        oppMoves=self.getAllPossibleMoves()
        self.whiteToMove= not self.whiteToMove
        for move in oppMoves:
            if move.endRow== r and move.endCol== c: #square is under attack
                return True
        return False
        
        
        
    #all moves without considering checks
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn =='b' and not self.whiteToMove):
                    piece= self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #calls the appropriate move function to the pieces. See constructor for more info
        return moves
        """ 
        Get all the pawn moves for the pawn located at row,col and add these moves to the list
        
        """
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #white pawns moves
            if self.board[r-1][c]== '--':#1square pawn advance
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c]== '--': # 2 square pawn adwance
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0: # capture to the left
                if self.board[r-1][c-1][0]=='b': #enemy piece to capture
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board, isEnpassantMove=True))
            if c+1 <=7: # captures to the right 
                if self.board[r-1][c+1][0] == 'b':#enemy piece to captre
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board, isEnpassantMove=True))
        else:
            if self.board[r+1][c]== '--':#1 square advance for black
                moves.append(Move((r,c),(r+1,c), self.board))
                if r==1 and self.board[r+2][c]== '--':#2 square pawn advance for black
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >=0: #capture to the left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c-1),self.board, isEnpassantMove=True))
            if c+1 <=7: # capture to the right?
                if self.board[r+1][c+1][0]=='w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c+1),self.board, isEnpassantMove=True))
        #add pawn promotions
        """ 
        Get all the pawn moves for the pawn located at row,col and add these moves to the list
        
        """
    def getRookMoves(self,r,c,moves):
        if self.whiteToMove:
            #check if rook can go up:
            for i in range(r-1,-1,-1):
                if self.board[i][c]=='--':
                    moves.append(Move((r,c),(i,c),self.board))
                if self.board[i][c][0]=='b':
                    moves.append(Move((r,c),(i,c),self.board))
                    break
                if self.board[i][c][0]=='w':
                    break
            #check if rook can go down:
            for i in range(r+1,8):
                if self.board[i][c]=='--':
                    moves.append(Move((r,c),(i,c),self.board))
                if self.board[i][c][0]=='b':
                    moves.append(Move((r,c),(i,c),self.board))
                    break
                if self.board[i][c][0]=='w':
                    break
            #check if rook can go left:
            for i in range(c-1,-1,-1):
                if self.board[r][i]=='--':
                    moves.append(Move((r,c),(r,i),self.board))
                if self.board[r][i][0]=='b':
                    moves.append(Move((r,c),(r,i),self.board))
                    break
                if self.board[r][i][0]=='w':
                    break
            #check if rook can go right:
            for i in range(c+1,8):
                if self.board[r][i]=='--':
                    moves.append(Move((r,c),(r,i),self.board))
                if self.board[r][i][0]=='b':
                    moves.append(Move((r,c),(r,i),self.board))
                    break
                if self.board[r][i][0]=='w':
                    break
        else:
            #check if rook can go up:
            for i in range(r-1,-1,-1):
                if self.board[i][c]=='--':
                    moves.append(Move((r,c),(i,c),self.board))
                if self.board[i][c][0]=='w':
                    moves.append(Move((r,c),(i,c),self.board))
                    break
                if self.board[i][c][0]=='b':
                    break
            #check if rook can go down:
            for i in range(r+1,8):
                if self.board[i][c]=='--':
                    moves.append(Move((r,c),(i,c),self.board))
                if self.board[i][c][0]=='w':
                    moves.append(Move((r,c),(i,c),self.board))
                    break
                if self.board[i][c][0]=='b':
                    break
            #check if rook can go left:
            for i in range(c-1,-1,-1):
                if self.board[r][i]=='--':
                    moves.append(Move((r,c),(r,i),self.board))
                if self.board[r][i][0]=='w':
                    moves.append(Move((r,c),(r,i),self.board))
                    break
                if self.board[r][i][0]=='b':
                    break
            #check if rook can go right:
            for i in range(c+1,8):
                if self.board[r][i]=='--':
                    moves.append(Move((r,c),(r,i),self.board))
                if self.board[r][i][0]=='w':
                    moves.append(Move((r,c),(r,i),self.board))
                    break
                if self.board[r][i][0]=='b':
                    break
    
    
    
    
    def getKnightMoves(self,r,c,moves):
        #Check if knight can go up like L
        if self.whiteToMove:
            #This is for Topleft move
            if r - 2 >= 0 and c-1>=0:
                if self.board[r-2][c-1]=='--':
                    moves.append(Move((r,c),(r-2,c-1),self.board))
                if self.board[r-2][c-1][0]=='b':
                    moves.append(Move((r,c),(r-2,c-1),self.board))
            #This is for Topright move
            if r-2 >=0 and c+1<=7:
                if self.board[r-2][c+1]=='--':
                    moves.append(Move((r,c),(r-2,c+1),self.board))
                if self.board[r-2][c+1][0]=='b':
                    moves.append(Move((r,c),(r-2,c+1),self.board))
            #This is for Downleft move
            if r+2 <=7 and c-1 >=0:
                if self.board[r+2][c-1]=='--':
                    moves.append(Move((r,c),(r+2,c-1),self.board))
                if self.board[r+2][c-1][0]=='b':
                    moves.append(Move((r,c),(r+2,c-1),self.board))
            #This is for Downright move
            if r+2 <=7 and c+1 <=7:
                if self.board[r+2][c+1]=='--':
                    moves.append(Move((r,c),(r+2,c+1),self.board))
                if self.board[r+2][c+1][0]=='b':
                    moves.append(Move((r,c),(r+2,c+1),self.board))
            #This is for LeftUp move
            if r+1<=7 and  c-2>=0:
                if self.board[r+1][c-2]== '--':
                    moves.append(Move((r,c),(r+1,c-2),self.board))
                if self.board[r+1][c-2][0]=='b':
                    moves.append(Move((r,c),(r+1,c-2),self.board))
            #This is for LeftDown move
            if r-1>=0 and c-2>=0:
                if self.board[r-1][c-2]=='--':
                    moves.append(Move((r,c),(r-1,c-2),self.board))
                if self.board[r-1][c-2][0]=='b':
                    moves.append(Move((r,c),(r-1,c-2),self.board))
            #This is for RightUp move
            if r+1<=7 and c+2<=7:
                if self.board[r+1][c+2]=='--':
                    moves.append(Move((r,c),(r+1,c+2),self.board))
                if self.board[r+1][c+2][0]=='b':
                    moves.append(Move((r,c),(r+1,c+2),self.board))
            #This is for RightDown move
            if r-1>=0 and c+2<=7:
                if self.board[r-1][c+2]== '--':
                    moves.append(Move((r,c),(r-1,c+2),self.board))
                if self.board[r-1][c+2][0]=='b':
                    moves.append(Move((r,c),(r-1,c+2),self.board))
        else:
            #This is for Topleft move
            if r - 2 >= 0 and c-1>=0:
                if self.board[r-2][c-1]=='--':
                    moves.append(Move((r,c),(r-2,c-1),self.board))
                if self.board[r-2][c-1][0]=='w':
                    moves.append(Move((r,c),(r-2,c-1),self.board))
            #This is for Topright move
            if r-2 >=0 and c+1<=7:
                if self.board[r-2][c+1]=='--':
                    moves.append(Move((r,c),(r-2,c+1),self.board))
                if self.board[r-2][c+1][0]=='w':
                    moves.append(Move((r,c),(r-2,c+1),self.board))
            #This is for Downleft move
            if r+2 <=7 and c-1 >=0:
                if self.board[r+2][c-1]=='--':
                    moves.append(Move((r,c),(r+2,c-1),self.board))
                if self.board[r+2][c-1][0]=='w':
                    moves.append(Move((r,c),(r+2,c-1),self.board))
            #This is for Downright move
            if r+2 <=7 and c+1 <=7:
                if self.board[r+2][c+1]=='--':
                    moves.append(Move((r,c),(r+2,c+1),self.board))
                if self.board[r+2][c+1][0]=='w':
                    moves.append(Move((r,c),(r+2,c+1),self.board))
            #This is for LeftUp move
            if r+1<=7 and  c-2>=0:
                if self.board[r+1][c-2]== '--':
                    moves.append(Move((r,c),(r+1,c-2),self.board))
                if self.board[r+1][c-2][0]=='w':
                    moves.append(Move((r,c),(r+1,c-2),self.board))
            #This is for LeftDown move
            if r-1>=0 and c-2>=0:
                if self.board[r-1][c-2]=='--':
                    moves.append(Move((r,c),(r-1,c-2),self.board))
                if self.board[r-1][c-2][0]=='w':
                    moves.append(Move((r,c),(r-1,c-2),self.board))
            #This is for RightUp move
            if r+1<=7 and c+2<=7:
                if self.board[r+1][c+2]=='--':
                    moves.append(Move((r,c),(r+1,c+2),self.board))
                if self.board[r+1][c+2][0]=='w':
                    moves.append(Move((r,c),(r+1,c+2),self.board))
            #This is for RightDown move
            if r-1>=0 and c+2<=7:
                if self.board[r-1][c+2]== '--':
                    moves.append(Move((r,c),(r-1,c+2),self.board))
                if self.board[r-1][c+2][0]=='w':
                    moves.append(Move((r,c),(r-1,c+2),self.board))






    def getBishopMoves(self,r,c,moves):
        #check if bishop can go NW(NorthWest)
        counter=1
        if self.whiteToMove:
            row_count=int(r)
            column_count=int(c)
            for i in range(8):
                if row_count ==0 or column_count==0:
                    break
                row_count-=counter
                column_count-=counter
                if self.board[row_count][column_count]== '--':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                if self.board[row_count][column_count][0]== 'b':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                    break
                if self.board[row_count][column_count][0]== 'w':
                    break
            #Check if bishop can go SW(SouthWest)
            row_count=int(r)
            column_count=int(c)
            for i in range(8):
                if row_count>=7 or column_count ==0:
                    break
                row_count+=counter
                column_count-=counter
                if self.board[row_count][column_count]== '--':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                if self.board[row_count][column_count][0]== 'b':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                    break
                if self.board[row_count][column_count][0]== 'w':
                    break
            #Check if bishop can go NE(NorthEast)
            row_count=int(r)
            column_count=int(c)
            for i in range(8):
                if row_count==0 or column_count >=7:
                    break
                row_count-=counter
                column_count+=counter
                if self.board[row_count][column_count]== '--':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                if self.board[row_count][column_count][0]== 'b':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                    break
                if self.board[row_count][column_count][0]== 'w':
                    break
            #Check if bishop can go SE(SouthEast)
            row_count=int(r)
            column_count=int(c)
            for i in range(8):
                if row_count>=7 or column_count >=7:
                    break
                row_count+=counter
                column_count+=counter
                if self.board[row_count][column_count]== '--':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                if self.board[row_count][column_count][0]== 'b':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                    break
                if self.board[row_count][column_count][0]== 'w':
                    break
        else:
            #check if bishop can go NW(NorthWest)
            counter=1
            row_count=int(r)
            column_count=int(c)
            for i in range(8):
                if row_count ==0 or column_count==0:
                    break
                row_count-=counter
                column_count-=counter
                if self.board[row_count][column_count]== '--':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                if self.board[row_count][column_count][0]== 'w':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                    break
                if self.board[row_count][column_count][0]== 'b':
                    break
        #Check if bishop can go SW(SouthWest)
            row_count=int(r)
            column_count=int(c)
            for i in range(8):
                if row_count>=7 or column_count ==0:
                    break
                row_count+=counter
                column_count-=counter
                if self.board[row_count][column_count]== '--':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                if self.board[row_count][column_count][0]== 'w':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                    break
                if self.board[row_count][column_count][0]== 'b':
                    break
        #Check if bishop can go NE(NorthEast)
            row_count=int(r)
            column_count=int(c)
            for i in range(8):
                if row_count==0 or column_count >=7:
                    break
                row_count-=counter
                column_count+=counter
                if self.board[row_count][column_count]== '--':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                if self.board[row_count][column_count][0]== 'w':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                    break
                if self.board[row_count][column_count][0]== 'b':
                    break
        #Check if bishop can go SE(SouthEast)
            row_count=int(r)
            column_count=int(c)
            for i in range(8):
                if row_count>=7 or column_count >=7:
                    break
                row_count+=counter
                column_count+=counter
                if self.board[row_count][column_count]== '--':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                if self.board[row_count][column_count][0]== 'w':
                    moves.append(Move((r,c),(row_count,column_count), self.board))
                    break
                if self.board[row_count][column_count][0]== 'b':
                    break

    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
        
    def getKingMoves(self,r,c,moves):
        king_moves=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor= 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow= r+ king_moves[i][0]
            endCol= c+king_moves[i][1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece= self.board[endRow][endCol]
                if endPiece[0]!= allyColor: #not an ally piece
                    moves.append(Move((r,c),(endRow,endCol),self.board))
        """
        Generate all valid castle moves for the king(r,c) and add them to the list of moves
        """


    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return #cant castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r,c,moves)
        
        
        
        
    def getKingsideCastleMoves(self,r,c,moves):
        if r+1 >7 or c +1 >7 or r-2<0 or c-2<0:
            isCastleMove=False
        else:
            if self.board[r][c+1]=='--' and self.board [r][c+2]== '--':
                if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                    moves.append(Move((r,c),(r,c+2),self.board, isCastleMove=True))
    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1]=='--' and self.board[r][c-2]=='--' and self.board[r][c-3]=='--':
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board, isCastleMove=True))
    """
            3fold repetition
    """
    def treeFoldRep(self):
        if len(self.moveLog)> 8:
            moveOne=(self.moveLog[-2],self.moveLog[-1])
            moveTwo=(self.moveLog[-4],self.moveLog[-3])
            moveThree=(self.moveLog[-6],self.moveLog[-5])
            moveFour=(self.moveLog[-8],self.moveLog[-7])
            if moveOne==moveThree and moveTwo == moveFour:
                self.draw=True
                return True
        else:
            return False
    
    def move_value(self,move,board,gs):
        piecePositionScores= {"N":[cw.knightScores,cw.knightScores],
                        "B":[cw.bishopsScoresw,cw.bishopsScoresb],
                        "R":[cw.rooksScorew,cw.rooksScoreb],
                        "Q":[cw.queensScorew,cw.queensScoreb],
                        "p":[cw.pawnScoresw,cw.pawnScoresb],
                        "K":[cw.kingsScorew,cw.kingsScoreb]}
        pieceScore={"K":0,"Q":10,'R':5,'B':3,"N":3,'p':1}

        attacker=board[move.startRow][move.startCol] #translated to wp or whatever
        victim=board[move.endRow][move.endCol]
        
        
        
        if attacker[0] != victim[0] and attacker!= '--' and victim!='--':
            #print(move.startRow,move.startCol)
            #print(pieceScore[victim[1]]+6-(pieceScore[attacker[1]]/100))
            return pieceScore[victim[1]]+6-(pieceScore[attacker[1]]/100)
            
        return 0
    
        """
            def move_value(self,move,board,gs):
        piecePositionScores= {"N":[cw.knightScores,cw.knightScores],
                        "B":[cw.bishopsScoresw,cw.bishopsScoresb],
                        "R":[cw.rooksScorew,cw.rooksScoreb],
                        "Q":[cw.queensScorew,cw.queensScoreb],
                        "p":[cw.pawnScoresw,cw.pawnScoresb],
                        "K":[cw.kingsScorew,cw.kingsScoreb]}
        pieceScore={"K":0,"Q":9.5,'R':5.33,'B':3.03,"N":3.05,'p':1}

        attacker=board[move.startRow][move.startCol] #translated to wp or whatever
        victim=board[move.endRow][move.endCol]
        
        
        
        if attacker[0] != victim[0] and attacker!= '--' and victim!='--':
            #print(move.startRow,move.startCol)
            if attacker[0] == 'w':
                attacker_pos_score=piecePositionScores[attacker[1]][0][move.startRow][move.startCol]
                victim_pos_score=piecePositionScores[victim[1]][1][move.endRow][move.endCol]
                #print(attacker_pos_score,victim_pos_score)
                return 10*(pieceScore[victim[1]]+victim_pos_score*0.16)-(pieceScore[attacker[1]]+attacker_pos_score)
            else:
                attacker_pos_score=piecePositionScores[attacker[1]][1][move.startRow][move.startCol]
                victim_pos_score=piecePositionScores[victim[1]][0][move.endRow][move.endCol]
                #print(attacker_pos_score,victim_pos_score)
                return 10*(pieceScore[victim[1]]+victim_pos_score*0.16)-(pieceScore[attacker[1]]+attacker_pos_score)
        return 0
        """




class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs
    
class Move():
    # maps keys to values
    #key : value
    ranksToRows= {'1':7,'2':6,'3':5,'4':4,
                '5':3,'6':2,'7':1,'8':0 }
    rowsToRanks= {v:k for k, v in ranksToRows.items()}
    filesToCols={'a':0,'b':1,'c':2,'d':3,
                'e':4,'f':5,'g':6,'h':7}
    colsToFiles= {v:k for k,v in filesToCols.items()}
    
    
    
    def __init__(self,startSq,endSq,board, isEnpassantMove=False, isCastleMove=False):
        self.startRow= startSq[0]
        self.startCol= startSq[1]
        self.endRow= endSq[0]
        self.endCol= endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        #pawn promotion
        self.isPawnPromotion= False
        if (self.pieceMoved == 'wp' and self.endRow == 0)or (self.pieceMoved == 'bp' and self.endRow==7):
            self.isPawnPromotion = True
        self.moveID=self.startRow*1000 + self.startCol*100+self.endRow*10+self.endCol
        #en passant
        self.isEnpassantMove=isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved =='bp' else 'bp'
        #castle move
        self.isCapture= self.pieceCaptured != '--'
        self.isCastleMove= isCastleMove
        
        #print(self.moveID)


            
        
    """ 
    Overriding the equals method
    """
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
        
        
        
    def getRankFile(self,r,c):
        return self.colsToFiles[c]+ self.rowsToRanks[r]
    
    
    #overriding str() function
    def __str__(self):
        if self.isCastleMove:
            return "O-O" if self.endCol==6 else "O-O-O"
        endSquare= self.getRankFile(self.endRow, self.endCol)
        #pawn moves
        if self.pieceMoved[1]=='p':
            if self.isCapture:
                return self.colsToFiles[self.startCol]+'x'+endSquare
            else:
                return endSquare
        #pawn promotions
        
        #two of the same type of piece moving to the same square, Nbd2 if both knights can move to d2
        
        #adding + for check move, and # for checkmate move
        
        #piece moves
        moveString= self.pieceMoved[1]
        if self.isCapture:
            moveString+='x'
        return moveString+endSquare
    
    
    
    
    
    
    