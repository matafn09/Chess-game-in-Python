class GameState():
        def __init__(self):
            #Board is a 8x8 2D list, each element on the list has 2 characters.
            #The fist character represent the color of the piece ("b","w") 
            #The second character represent the type of the piece("P","R","B","N","Q","K")
            # "--" Represent the empty spaces without a piece
            self.board=[
                ["bR","bN","bB","bQ","bK","bB","bN","bR"],
                ["bP","bP","bP","bP","bP","bP","bP","bP"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["wP","wP","wP","wP","wP","wP","wP","wP"],
                ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
            self.moveFunctions= {"P": self.getPawnMoves, "R":self.getRookMoves,"N":self.getKnightMoves,
                                 "B":self.getBishopMoves,"Q":self.getQueenMoves,"K":self.getKingMoves}
            self.whiteToMove= True
            self.moveLog=[]
            self.whiteKingLocation =(7,4)
            self.blackKingLocation =(0,4)
            self.pins =[]
            self.checks = []
            self.checkmate= False
            self.stalemate= False
            self.enpassantPossible = () # Coordinates for the square where enpassant capture is possible
            self.enpassantPossibleLog =[self.enpassantPossible]
            self.currentCastlingRight = CastleRights(True, True, True, True)
            self.CastleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs )]
            
            
            
            
        """ Takes a Move as a parameter and executes it (this will not work for castling,pawn promotion, and en-passant"""
        
        def makeMove(self, move):
            self.board[move.startRow][move.startCol]= "--"
            self.board[move.endRow][move.endCol]= move.pieceMoved
            self.moveLog.append(move) #log the move so we can undo it later
            self.whiteToMove= not self.whiteToMove #swap players
            #update the king's location if moved
            if move.pieceMoved == "wK":
                self.whiteKingLocation= (move.endRow, move.endCol)
            
            elif move.pieceMoved =="bK":
                self.blackKingLocation = (move.endRow, move.endCol)
            #Pawn promotion
            
            if move.isPawnPromotion:
                self.board[move.endRow][move.endCol]=  move.pieceMoved[0]  + "Q"
                
            #enpassant move
            
            if move.isEnpassantMove:
                self.board[move.startRow][move.endCol]= "--" #capturing the pawn
                
            #update enpassantPossible variable
            
            if move.pieceMoved[1]== "P" and abs(move.startRow - move.endRow) == 2: #only on 2 squares pawn advances
                self.enpassantPossible= ((move.startRow + move. endRow)//2, move.startCol)
            
            else:
                self.enpassantPossible = ()
                
            # undo castle move
            
            if move.isCastleMove:
                
                if move.endCol - move.startCol == 2: #kingside Castle move
                    self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol + 1] #moves the rook
                    self.board[move.endRow][move.endCol+1] = "--" # erase old rook
                    
                else: #queenside castle move
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] # moves the rook
                    self.board[move.endRow][move.endCol- 2] = "--" # erase old rook
                    
                    
            # update castling rights - whenever it's a king or a rook move
            self.updateCastleRights(move)
            self.CastleRightsLog.append (CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs ))
            
            
            self.enpassantPossibleLog.append(self.enpassantPossible)
            
            
            
          
            
        """Undo the last move made"""
        
        def undoMove(self):
            if len(self.moveLog)!=0: #make sure that there is a move to undo
                move= self.moveLog.pop()
                self.board[move.startRow][move.startCol]=move.pieceMoved
                self.board[move.endRow][move.endCol]=move.pieceCaptured
                self.whiteToMove= not self.whiteToMove #switch turns back
                
                # update the king's position if needed
                
                if move.pieceMoved == "wK":
                    self.whiteKingLocation= (move.startRow, move.startCol)
                elif move.pieceMoved =="bK":
                    self.blackKingLocation = (move.startRow, move.startCol)
                
                #undo enpasant move
                
                if move.isEnpassantMove:
                    self.board[move.endRow][move.endCol] = "--" #leave landing square blank
                    self.board[move.startRow][move.endCol] = move.pieceCaptured
                    
                self.enpassantPossibleLog.pop()
                self.enpassantPossible= self.enpassantPossibleLog[-1]
                    
                # undo castling rights
                
                self.CastleRightsLog.pop() # get rid of the new castle rights from the move we are undoing
                newRights = self.CastleRightsLog[-1] # set the current castle rights to the last one in the list
                self.currentCastlingRight= CastleRights (newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
                
                #undo castle move
                
                if move.isCastleMove:
                    if move.endCol - move.startCol == 2: #Kingside
                        self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                        self.board[move.endRow][move.endCol-1] = "--"
                    
                    else:   #queenside
                    
                        self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                        self.board[move.endRow][move.endCol+1] = "--"
                        
                # add these
                self.checkmate = False
                self.stalemate = False
                
                        
                
                
                    
        """ Update the castle rights given the move
        """             
        def updateCastleRights (self, move):
            
            if move.pieceMoved == "wK":
                self.currentCastlingRight.wks = False
                self.currentCastlingRight.wqs = False
                
            elif move.pieceMoved == "bK":
                self.currentCastlingRight.bks = False
                self.currentCastlingRight.bqs = False
                
                # White side castle
            elif  move.pieceMoved == "wR":
                if move.startRow  == 7:
                    if move.startCol == 0: # left rook
                        self.currentCastlingRight.wqs = False
                    if move.startCol == 7: # right rook
                        self.currentCastlingRight.wks = False
                        
                # Black side castle
            elif  move.pieceMoved == "bR":
                    if move.startRow  == 0:
                        if move.startCol == 0: # left rook
                            self.currentCastlingRight.bqs = False
                        if move.startCol == 7: # right rook
                            self.currentCastlingRight.bks = False
                            
              #if a rook is captured
            if move.pieceCaptured == 'wR':
                if move.endRow == 7:
                    if move.endCol == 0:
                        self.currentCastlingRight.wqs = False
                    elif move.endCol == 7:
                        self.currentCastlingRight.wks = False
            elif move.pieceCaptured == 'bR':
                if move.endRow == 0:
                    if move.endCol == 0:
                        self.currentCastlingRight.bqs = False
                    elif move.endCol == 7:
                        self.currentCastlingRight.bks = False
            
        """ All moves considering checks"""
        def getValidMoves(self):
            tempEnpassantPossible= self.enpassantPossible
            tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) #copy the current castling rights
            #1) generate all possible moves
            moves = self.getAllPossibleMoves()
            if self.whiteToMove:
                
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
                
            #2) for each move, make the move
            for i in range(len(moves)-1,-1,-1): # when removing from a list go backwards through the list
                
                self.makeMove(moves[i])
                #3) generate all opponent's moves (def squareUnderAttack)
            
                #4) for each of your opponent's moves, see if they attack your king
                self.whiteToMove = not self.whiteToMove
                if self.inCheck():
                    moves.remove(moves[i])  #5) if they attack your king, not a valid move
                self.whiteToMove = not self.whiteToMove
                self.undoMove()
                
            if len(moves)==0: # either checkmate or stalemate
                if self.inCheck():
                    self.checkmate =True
                else:
                    self.stalemate =True
                
            self.enpassantPossible = tempEnpassantPossible
            self.currentCastlingRight = tempCastleRights
            return moves
        
        '''
        Determine if the current player is in check
        '''
        
        def inCheck(self):
            if self.whiteToMove:
                return self.squareUnderAttack(self.whiteKingLocation[0], self. whiteKingLocation[1])
            else:
                return self.squareUnderAttack(self.blackKingLocation[0], self. blackKingLocation[1])
        """
        Determine if the enemy can attack the square r,c
        
        """
        def squareUnderAttack(self, r, c):
            self.whiteToMove = not self.whiteToMove # switch to opponent's turn
            
            OpponentMoves = self.getAllPossibleMoves()
                        
            self.whiteToMove = not self.whiteToMove # switch turns back
            
            for move in OpponentMoves:
                if move.endRow == r and move.endCol == c: # square is under attack
                   
                    return True
            return False
            
            
        
        
        
        """All moves without considering checks"""
        
        
        def getAllPossibleMoves(self):
            
            moves=[]
            
            for r in range(len(self.board)): # num of rows
                for c in range(len(self.board[r])): # num of cols in given row
                    turn= self.board[r][c][0]
                    if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                            piece = self.board [r][c][1]
                            self.moveFunctions[piece](r,c,moves)  #calls the appropiate move function based on piece type
            return moves
        
        
        """Get all the moves for the pawn" located at row,col and add these moves to the list"""       
    
        def getPawnMoves(self,r,c,moves):
            if self.whiteToMove: #White pawn moves
                if self.board[r-1][c] == "--": #1 square pawn advance
                    moves.append(Move((r,c), (r-1,c), self.board))
                    if r==6 and self.board[r-2][c] == "--": #2 square pawn advance
                        moves.append(Move((r,c), (r-2,c), self.board))
                    
                if c-1>= 0:#captures to the left
                    if self.board[r-1][c-1][0]== "b":# enemy piece to capture
                        moves.append(Move((r,c),(r-1,c-1),self.board))
                    elif (r-1,c-1)== self.enpassantPossible:
                        moves.append(Move((r,c),(r-1,c-1),self.board, isEnpassantMove= True))
                        
                if c+1<= 7: #captures to the right
                     if self.board[r-1][c+1][0]== "b":# enemy piece to capture
                         moves.append(Move((r,c),(r-1,c+1),self.board))
                         
                     elif (r-1,c+1)== self.enpassantPossible:
                          moves.append(Move((r,c),(r-1,c+1),self.board, isEnpassantMove= True))
            else: # black pawn moves
                    
                    if self.board[r+1][c] == "--": #1 square pawn advance
                        moves.append(Move((r,c), (r+1,c), self.board))
                        if r==1 and self.board[r+2][c] == "--": #2 square pawn advance
                            moves.append(Move((r,c), (r+2,c), self.board))  
                    #captures
                    
                    if c-1 >= 0:#captures to the left
                    
                        if self.board[r+1][c-1][0]== "w":# enemy piece to capture
                            moves.append(Move((r,c),(r+1,c-1),self.board))
                            
                        elif (r+1,c-1)== self.enpassantPossible:
                             moves.append(Move((r,c),(r+1,c-1),self.board, isEnpassantMove= True))
                             
                    if c+1 <= 7: #captures to the right
                    
                         if self.board[r+1][c+1][0]== "w":# enemy piece to capture
                             moves.append(Move((r,c),(r+1,c+1),self.board))
                             
                         elif (r+1,c+1)== self.enpassantPossible:
                              moves.append(Move((r,c),(r+1,c+1),self.board, isEnpassantMove= True))
                
                
        """ Get all the rook moves for the rook located at row, col and add these moves to the list"""        
        
        def getRookMoves(self, r,c,moves):
            directions= ((-1,0), (0,-1) ,(1,0),(0,1)) #up, left, down, right
            enemyColor= "b" if self.whiteToMove else"w"
            if self.whiteToMove:
                enemyColor = "b"
            else:
                enemyColor = "w"
            
            for i in directions:
                for j in range(1,8):
                    
                    endRow = r + i[0] *j
                    endCol= c + i[1]* j
                    
                    if 0 <= endRow <8 and 0 <= endCol <8: # on board
                        endPiece = self.board[endRow][endCol]
                        
                        if endPiece == "--": # empty space valid
                            moves.append(Move((r,c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #enemy piece valid
                            moves.append(Move((r,c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break 
                    else: # off board
                        break
        """ Get all the bishop moves for the rook located at row, col and add these moves to the list"""
    
        def getBishopMoves(self, r,c,moves):
            directions= ((-1,-1), (-1,1) ,(1,-1),(1 ,1)) # 4 diagonals
            enemyColor= "b" if self.whiteToMove else"w"
            if self.whiteToMove:
                enemyColor = "b"
            else:
                enemyColor = "w"
            
            for i in directions:
                for j in range(1,8): # Bishop can move a max of 7 squares
                    
                    endRow = r + i[0] *j
                    endCol= c + i[1]* j
                    
                    if 0 <= endRow <8 and 0 <= endCol <8: # on board
                        endPiece = self.board[endRow][endCol]
                        
                        if endPiece == "--": # empty space valid
                            moves.append(Move((r,c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #enemy piece valid
                            moves.append(Move((r,c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break 
                    else: # off board
                        break
        """ Get all the knight moves for the rook located at row, col and add these moves to the list"""
    
        def getKnightMoves(self, r,c,moves):
            knightMoves = ((-1,-2),(1,-2), (-1,2),(-2,-1), (2,-1), (-2, 1), (1,2),(2,1))
            allyColor ="w" if self.whiteToMove else "b"
            for m in knightMoves:
                endRow = r + m[0]
                endCol = c + m[1]
                if 0 <= endRow <8 and 0 <=endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        
                        
        """ Get all the Queen moves for the rook located at row, col and add these moves to the list"""

        def getQueenMoves(self, r,c,moves):
            self.getRookMoves(r,c, moves)
            self.getBishopMoves(r,c, moves)
        
        """ Get all the King moves for the rook located at row, col and add these moves to the list"""
    
        def getKingMoves(self, r,c,moves):
            kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
            allyColor = "w" if self.whiteToMove else "b"
            
            for i in range(8):
                endRow = r + kingMoves[i][0]
                endCol = c + kingMoves [i][1]
                if 0 <= endRow <8 and 0 <=endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                        moves.append(Move((r,c), (endRow, endCol), self.board))
            
        
        """
        Generate all valid castle moves for the king
        """
        def getCastleMoves (self, r, c, moves):
            if self.squareUnderAttack(r,c):
                return # can't castle while we're in check
            if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
                self.getKingsideCastleMoves(r, c, moves)
            if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
                self.getQueensideCastleMoves(r, c, moves)
                
                
        
        def getKingsideCastleMoves (self, r, c, moves):
            
            if self.board[r][c+1] == "--" and  self.board[r][c+2] == "--":
                if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                    moves.append(Move((r,c),(r, c+2), self.board, isCastleMove = True))
                    
                    
            
        def getQueensideCastleMoves (self, r, c,moves):
            
            if self.board[r][c-1] == "--" and  self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
                if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                    moves.append(Move((r,c),(r, c-2), self.board, isCastleMove = True))
            

class CastleRights():
    
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
        
        # maps keys to values
        # key: value
        
        ranksToRows ={"1":7,"2":6, "3":5, "4":4,
                      "5":3, "6":2, "7":1, "8":0}
        rowsToRanks={v:k for k,v in ranksToRows.items()}
        filesToCols={"a": 0, "b":1, "c":2, "d":3,
                     "e": 4, "f": 5, "g":6, "h":7 }
        colsToFiles= {v:k for k,v in filesToCols.items()}
        
        def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
            
            self.startRow= startSq[0]
            self.startCol= startSq[1]
            self.endRow= endSq[0]
            self.endCol= endSq[1]
            self.pieceMoved= board[self.startRow][self.startCol]
            self.pieceCaptured= board[self.endRow][self.endCol]
            self.isCapture = self.pieceCaptured != "--"
            
            #Pawn promotion
            
            self.isPawnPromotion= (self.pieceMoved== "wP" and self.endRow == 0) or (self.pieceMoved== "bP" and self.endRow == 7)
        
            #Enpassant move
            self.isEnpassantMove= isEnpassantMove
            
            if isEnpassantMove:
                self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"
            
            # castle move
            
            self.isCastleMove = isCastleMove


                
            self.moveID= self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
            print(self.moveID)
        """ Overriding the equals method"""
        
        def __eq__(self,other):
            
            if isinstance(other, Move):
                return self.moveID == other.moveID
            
            return False
            
        def getChessNotation(self):
            #you  can add to make this like real chess notation
             return self.getRankFile(self.startRow, self.startCol)+ self.getRankFile(self.endRow, self.endCol)
             
        def getRankFile(self, r, c):
             return self.colsToFiles[c]+ self.rowsToRanks[r]
         
         # overriding the str () function
        def __str__(self):
            #castle move
            if self.isCastleMove:
                return "O-O" if self.endCol == 6 else"O-O-O"
            
                    # "O-O"   # King side castle
                    # "O-O-O" # Queen side castle
            endSquare = self.getRankFile(self.endRow, self.endCol)
            if self.pieceMoved[1] == "P":
                if self.isCapture:
                    return self.colsToFiles[self.startCol] + "x" + endSquare
                else:
                    return endSquare                    
            
        # pieces move
            moveString= self.pieceMoved[1]
            if self.isCapture:
                moveString+= "x"
            return moveString + endSquare
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
            