"""Class stores all information about the current chess game.
    And checking for valid moves for current GameState, and move log.
"""
class GameState():
    def __init__(self):
        # board 8x8 2D list, 2 characters, 1st char color of piece, 2nd char is type of piece
        # '--' is empty space with no piece
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','bR','wR','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']]
        self.whiteToMove= True
        self.moveLog=[]
        self.moveFunctions={'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                            'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]= '--'
        self.board[move.endRow][move.endCol]= move.pieceMoved
        self.moveLog.append(move)# log the move for undo purposes or history
        self.whiteToMove= not self.whiteToMove # swap players
        """
        Undo the last move made
        """
    def undoMove(self):
        if len(self.moveLog) != 0: #check if there are moves
            move= self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove= not self.whiteToMove
    
    
    
    #all moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
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
            if c+1 <=7: # captures to the right 
                if self.board[r-1][c+1][0] == 'b':#enemy piece to captre
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        else:
            if self.board[r+1][c]== '--':#1 square advance for black
                moves.append(Move((r,c),(r+1,c), self.board))
                if r==1 and self.board[r+2][c]== '--':#2 square pawn advance for black
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >=0: #capture to the left
                if self.board[r+1][c-1][0] == 'w':
                    
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <=7: # capture to the right?
                if self.board[r+1][c+1][0]=='w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                    
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
        pass
    def getBishopMoves(self,r,c,moves):
        pass
    def getQueenMoves(self,r,c,moves):
        pass
    def getKingMoves(self,r,c,moves):
        pass
class Move():
    # maps keys to values
    #key : value
    ranksToRows= {'1':7,'2':6,'3':5,'4':4,
                '5':3,'6':2,'7':1,'8':0 }
    rowsToRanks= {v:k for k, v in ranksToRows.items()}
    filesToCols={'a':0,'b':1,'c':2,'d':3,
                'e':4,'f':5,'g':6,'h':7}
    colsToFiles= {v:k for k,v in filesToCols.items()}
    
    
    
    def __init__(self,startSq,endSq,board):
        self.startRow= startSq[0]
        self.startCol= startSq[1]
        self.endRow= endSq[0]
        self.endCol= endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.moveID=self.startRow*1000 + self.startCol*100+self.endRow*10+self.endCol
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
    
    
    
    
    
    
    
    
    
    