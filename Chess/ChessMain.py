
"""This is our main chess file. Here is where the real-time game will be displayed,
 and it will be responsable for handling the user input"""

import pygame as p

import ChessEngine, ChessAI


BOARD_WIDTH= BOARD_HEIGHT= 512 # resolution of the game on screen
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
dimension=8 # dimension of the board is 8x8
sq_size= BOARD_HEIGHT// dimension
max_fps=15 # for animations later on
images={}

# initialize a global dictionary of images. This will be called once exactly in the main

def loadimages():
    
    pieces=["wR","wN","wB","wQ","wK","wP","bR","bN","bB","bQ","bK","bP"]
    
    for piece in pieces:
        
        images[piece]=p.transform.scale(p.image.load("images/"+ piece + ".png"), (sq_size,sq_size))
    #Note we can access the images by satating "images["wP"]"

def main():
    p.init()
    screen= p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock=  p.time.Clock()
    screen.fill(p.Color("white"))
    gs= ChessEngine.GameState()
    validMoves= gs.getValidMoves()
    moveMade = False # Flag variable for when a move is made
    animate = False  # Flag variable for when we should animate a move
    moveLogFont = p.font.SysFont( "Arial", 14, False, False)
    loadimages()# onlyy do this once before the while loop
    running= True
    sqSelected=() # no square is selected, keep track of the last click of the user(tuple: (row, col))
    playerClicks=[]#keep track of player clicks two tuples([(6,4),(4,4)])
    gameOver = False
    PlayerOne = True # If a Human is playing white, then this will be True. Otherwise, it will be false
    PlayerTwo = False # Save as above but for black

    
    while running:
        humanTurn  =(gs.whiteToMove and PlayerOne) or (not gs.whiteToMove and PlayerTwo)
        for e in p.event.get():
            if e.type== p.QUIT:
                running = False
            
            # Mouse handler
            
            elif e.type==p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location=p.mouse.get_pos() #(x,y) location of the mouse
                    col= location[0]//sq_size
                    row=location[1]//sq_size
                    if sqSelected== (row, col) or col >= 8: #The user click the same square twice
                        sqSelected=()#deselect
                        playerClicks=[] #clear player clicks
                    else:               
                        sqSelected= (row, col)
                        playerClicks.append(sqSelected)# Append for both first and second click
                    if len(playerClicks)==2: #after 2nd click
                       move= ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)     
                       # print(move.getChessNotation( ))
                       
                       for i in range(len(validMoves)):
                           
                           if  move == validMoves[i]:
                               
                           
                               gs.makeMove(validMoves[i])
                               moveMade = True
                               animate=True
                               sqSelected= () #reset user clicks
                               playerClicks= []
                           
                       if not moveMade:
                                playerClicks= [sqSelected]  
                              
                              
                       
                # Key handlers
            elif e.type == p.KEYDOWN:
                    
                    if e.key == p.K_z: # undo when "z" is pressed
                        gs.undoMove()
                        moveMade = True
                        animate = False
                        gameOver = False
                        
                    if e.key==p.K_r: # reset the board when "r" is pressed    
                        gs=ChessEngine.GameState()
                        validMoves= gs.getValidMoves()
                        sqSelected = ()
                        playerClicks= []
                        moveMade = False
                        animate = False
                        gameOver = False
                    
        #AI move finder
        
        
        
        if not gameOver and not humanTurn:
            
           AIMove= ChessAI.findBestMove(gs, validMoves)
           
           if AIMove is None:
                        
                    AIMove = ChessAI.findRandomMove(validMoves)
           gs.makeMove(AIMove)
           moveMade = True
           animate = True            
                
                
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves= gs.getValidMoves()
            moveMade= False
            animate= False
            
        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)     
        
        if gs.checkmate or gs.stalemate:
            gameOver = True
            text = "Stalemate" if gs.stalemate else "Black wins by Checkmate" if gs.whiteToMove else "White wins by Checkmate"
            drawEndGameText(screen,text)
            
        clock.tick(max_fps)
        p.display.flip()
    p.quit()
    
"""
    Highlight squares selected and moves for piece selected
"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    
    if sqSelected != ():
        r,c = sqSelected
        
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"): #sqSelected is a piece that can be moved
        
        #highlight selected square 
            s=p.Surface((sq_size, sq_size))
            s.set_alpha(100) #transparency value -> 0 transparent, 255 opaque
            s.fill(p.Color("dark blue"))
            screen.blit (s,(c*sq_size,r*sq_size ))
            
        #highlight moves from that square
        
            s.fill(p.Color("yellow"))
            
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*sq_size,move.endRow*sq_size))
            
            

def drawGameState(screen, gs, validMoves, sqSelected,moveLogFont):
    drawBoard(screen) # draw the board the screen
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # draw the pieces on top of the squares
    drawMoveLog(screen,gs,moveLogFont)
    
    
def drawBoard(screen):
    global colors
    colors= [p.Color("white"),p.Color("light  gray")]
    for i in range(dimension):
        for j in range(dimension):
            color= colors[((i+j)%2)]
            p.draw.rect(screen,color, p.Rect(j*sq_size, i*sq_size,sq_size,sq_size ))

def drawPieces(screen, board):
    for i in range(dimension):
        for j in range(dimension):
            piece= board[i][j]
            if piece != "--":  
                screen.blit(images[piece],p.Rect(j*sq_size, i*sq_size,sq_size,sq_size ))

"""
Draws the move Log
"""

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color ("black"), moveLogRect )
    moveLog = gs.moveLog
    moveTexts = moveLog # modify this later
    moveTexts = []
   
    for i in range (0, len(moveLog), 2):
        moveString= str(i//2 + 1) + "."+ str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + "  "
        moveTexts.append(moveString)
    
    movesPerRow=3
    
    padding= 5
    lineSpacing= 2
    textY= padding
    
    for i in range(0, len(moveTexts), movesPerRow):
        text= " "
        for j in range(movesPerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True , p.Color("white"))
        textLocation= moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing
    

"""
Animating a move
"""
def animateMove (move, screen, board, clock ):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 # frames to move one per square
    frameCount = (abs(dR) + abs (dC)) * framesPerSquare
    for frame in range (frameCount + 1):
        r,c= (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount )
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color=colors[(move.endRow+move.endCol)%2]
        endSquare = p.Rect(move.endCol * sq_size, move.endRow*sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
        
        #draw capture piece onto rectangle
        
        if move.pieceCaptured != "--":
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0]== "b" else move.endRow -1
                endSquare = p.Rect(move.endCol * sq_size, enPassantRow*sq_size, sq_size, sq_size)
            screen.blit(images[move.pieceCaptured], endSquare)
                
        #draw moving piece
        
        screen.blit(images[move.pieceMoved],p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(0)
        
def drawEndGameText(screen,text):
    
    font = p.font.SysFont( "Helvetica", 32, True, False)
    textObject = font.render(text, 0 , p.Color("Black"))
    textLocation= p.Rect(0,0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2,BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject= font.render(text, 0 , p.Color("Black"))
    screen.blit( textObject, textLocation.move(2,2))
        
    
if __name__== "__main__":
    main()