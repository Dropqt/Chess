"""Class stores all information about the current chess game.
    And checking for valid moves for current GameState, and move log.
"""
class GameState():
    def __init__(self):
        # board 8x8 2D list, 2 characters, 1st char color of peace, 2nd char is type of piece
        # '--' is empty space with no piece
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']]
        self.whiteToMove= True
        self.moveLog=[]
        
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
        moves=[Move((6,4),(4,4),self.board)]
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn =='b' and not self.whiteToMove):
                    piece= self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)
        return moves
        """ 
        Get all the pawn moves for the pawn located at row,col and add these moves to the list
        
        """
    def getPawnMoves(self,r,c,moves):
        pass
        """ 
        Get all the pawn moves for the pawn located at row,col and add these moves to the list
        
        """
    def getRookMoves(self,r,c,moves):
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
        print(self.moveID)
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
    
    
    
    
    
    
    
    
    
    