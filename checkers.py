import random
from copy import deepcopy

BOARD_SIZE = 8
NUM_PLAYERS = 12
DEPTH_LIMIT = 10

PLAYERS = ["Black", "White"]

class Game:
    def __init__(self, player=0):
        self.board = Board()
        
        self.remaining = [NUM_PLAYERS, NUM_PLAYERS]
        
        self.player = player
        self.turn = 0
    def run(self):
        while not (self.gameOver(self.board)):
            self.board.drawBoardState()
            print("Current Player: "+PLAYERS[self.turn])
            if (self.turn == self.player):
                
                legal = self.board.calcLegalMoves(self.turn)
                if (len(legal) > 0):
            
                    move = self.getMove(legal)
                    self.makeMove(move)
                else:
                    print("No legal moves available, skipping turn...")
            else:
                legal = self.board.calcLegalMoves(self.turn)
                print("Valid Moves: ")
                for i in range(len(legal)):
                    print(str(i+1)+": ",end='')
                    print(str(legal[i].start)+" "+str(legal[i].end))
                if (len(legal)>0):
                    
                    if (len(legal)==1):
                        choice = legal[0]
                    else:
                        state = AB_State(self.board, self.turn, self.turn)
                        choice = self.alpha_beta(state)
            

                    self.makeMove(choice)
                    print("Computer chooses ("+str(choice.start)+", "+str(choice.end)+")")
           
            self.turn = 1-self.turn
        print("Game OVER")
        print("Black Captured: "+str(NUM_PLAYERS-self.remaining[1]))
        print("White Captured: "+str(NUM_PLAYERS-self.remaining[0]))
        score = self.calcScore(self.board)
        print("Black Score: "+str(score[0]))
        print("White Score: "+str(score[1]))
        if (score[0] > score[1]):
              print("Black wins!")
        elif (score[1] > score[0]):
              print("White wins!")
        else:
            print("It's a tie!")
        self.board.drawBoardState()

    def makeMove(self, move):

        self.board.boardMove(move, self.turn)
        if move.jump:
            
            self.remaining[1-self.turn] -= len(move.jumpOver)
            print("Removed "+str(len(move.jumpOver))+" "+PLAYERS[1-self.turn]+" pieces")
  
    def getMove(self, legal):
        move = -1
        
        while move not in range(len(legal)):
            
            print("Valid Moves: ")
            for i in range(len(legal)):
                print(str(i+1)+": ",end='')
                print(str(legal[i].start)+" "+str(legal[i].end))
            usr_input = input("Pick a move: ")
            
            move = -1 if (usr_input == '')  else (int(usr_input)-1)
            if move not in range(len(legal)):
                print("Illegal move")
        print("Legal move")
        return (legal[move])
        
    
    def gameOver(self, board):
        
        if (len(board.currPos[0]) == 0 or len(board.currPos[1]) == 0):
            return True
        
        elif (len(board.calcLegalMoves(0)) == 0 and len(board.calcLegalMoves(1)) == 0):
            return True
        else:
            
            return False
            
    
    def calcScore(self, board):
        score = [0,0]
        
        for cell in range(len(board.currPos[0])):
            
            if (board.currPos[0][cell][0] == 0):
                score[0] += 2
            
            else:
                score[0] += 1
        
        for cell in range(len(board.currPos[1])):
           
            if (board.currPos[1][cell][0] == BOARD_SIZE-1):
                score[1] += 2
            
            else:
                score[1] += 1
        return score
        
    
    def alpha_beta(self, state):
        result = self.max_value(state, -999, 999, 0)
        print("Total nodes generated: "+str(result.nodes))
        print("Max depth: "+str(result.max_depth))
        print("Max Val Cutoffs: "+str(result.max_cutoff))
        print("Min Val Cutoffs: "+str(result.min_cutoff))
        return result.move
   
   
    def max_value(self, state, alpha, beta, node):
      
      actions = state.board.calcLegalMoves(state.player)
      num_act = len(actions)
      
      v = AB_Value(-999, None, node, 1, 0, 0)
      
      if (node == DEPTH_LIMIT):
         v.move_value = self.evaluation_function(state.board, state.origPlayer)
   
         return v      
      if (len(actions)==0):
         
         score = self.calcScore(state.board)
         if (score[state.origPlayer] > score[1-state.origPlayer]):
            v.move_value = 100 + (2*score[state.origPlayer]-score[1-state.origPlayer])
  
         else:
            v.move_value = -100 + (2*score[state.origPlayer]-score[1-state.origPlayer])
          
         return v
      for a in actions:
         newState = AB_State(deepcopy(state.board), 1-state.player, state.origPlayer)
         
         newState.board.boardMove(a, state.player)
         new_v = self.min_value(newState, alpha, beta, node+1)
         
         if (new_v.max_depth > v.max_depth):
             v.max_depth = new_v.max_depth         
         v.nodes += new_v.nodes
         v.max_cutoff += new_v.max_cutoff
         v.min_cutoff += new_v.min_cutoff
         
         if (new_v.move_value > v.move_value):
            v.move_value = new_v.move_value
            v.move = a
         if (v.move_value >= beta):
            v.max_cutoff += 1
            return v
         if (v.move_value > alpha):
            alpha = v.move_value
      return v

  
    def min_value(self, state, alpha, beta, node):
      
      actions = state.board.calcLegalMoves(state.player)
      num_act = len(actions)
      
      v = AB_Value(999, None, node, 1, 0, 0)
      
      if (node == DEPTH_LIMIT):
         v.move_value = self.evaluation_function(state.board, state.player)
   
         return v
      if (len(actions)==0):
         
         score = self.calcScore(state.board)
         if (score[state.origPlayer] > score[1-state.origPlayer]):
            v.move_value = 100 + (2*score[state.origPlayer]-score[1-state.origPlayer])
             
         else:
            v.move_value = -100 + (2*score[state.origPlayer]-score[1-state.origPlayer])
    
         return v     
      for a in actions:
         newState = AB_State(deepcopy(state.board), 1-state.player, state.origPlayer)
         eval = self.evaluation_function(self.board, self.turn)
   
         newState.board.boardMove(a, state.player)
         new_v = self.max_value(newState, alpha, beta, node+1)
         
         if (new_v.max_depth > v.max_depth):
             v.max_depth = new_v.max_depth
         v.nodes += new_v.nodes
         v.max_cutoff += new_v.max_cutoff
         v.min_cutoff += new_v.min_cutoff
         
         if (new_v.move_value < v.move_value):
            v.move_value = new_v.move_value
            v.move = a
         if (v.move_value <= alpha):
            v.min_cutoff += 1
            return v
         if (v.move_value < beta):
            beta = v.move_value
      return v

    
    def evaluation_function(self, board, currPlayer):
        blk_far, blk_home_half, blk_opp_half = 0,0,0
        wt_far, wt_home_half, wt_opp_half = 0,0,0 
        
        for cell in range(len(board.currPos[0])):
            
            if (board.currPos[0][cell][0] == BOARD_SIZE-1):
                blk_far += 1
            
            elif (BOARD_SIZE/2 <= board.currPos[0][cell][0] < BOARD_SIZE):
                blk_opp_half += 1
            else:
                blk_home_half += 1
       
        for cell in range(len(board.currPos[1])):
            
            if (board.currPos[1][cell][0] == 0):
                wt_far += 1
           
            elif (0 <= board.currPos[1][cell][0] < BOARD_SIZE/2):
                wt_opp_half += 1
            else:
                wt_home_half += 1
        white_score = (7 * wt_far) + (5 * wt_opp_half)+ (3 * wt_home_half)
        black_score = (7 * blk_far) + (5 * blk_opp_half)+ (3 * blk_home_half)
        if (currPlayer == 0):
            return (black_score - white_score)
        else:
            return (white_score - black_score)       
                 

class AB_Value:
    def __init__(self, move_value, move, max_depth, child_nodes, max_cutoff, min_cutoff):
        self.move_value = move_value
        self.move = move
        self.max_depth = max_depth
        self.nodes = child_nodes
        self.max_cutoff = max_cutoff
        self.min_cutoff = min_cutoff
         


class AB_State:
   def __init__(self, boardState, currPlayer, originalPlayer):
      self.board = boardState
      self.player = currPlayer
      self.origPlayer = originalPlayer
      
class Move:
    def __init__(self, start, end, jump=False):
            self.start = start
            self.end = end 
            self.jump = jump 
            self.jumpOver = [] 
    
class Board:
    def __init__(self, board=[], currBlack=[], currWhite=[]):
        if (board!=[]):
            self.boardState = board     
        else:
            self.setDefaultBoard()
        self.currPos = [[],[]]
        if (currBlack != []):
            self.currPos[0] = currBlack
        else:
            self.currPos[0] = self.calcPos(0)
        if (currWhite != []):
            self.currPos[1] = currWhite
        else:
            self.currPos[1] = self.calcPos(1)            
    def boardMove(self, move_info, currPlayer):
        move = [move_info.start, move_info.end]
  
        remove = move_info.jumpOver
        jump = move_info.jump      
        
        self.boardState[move[0][0]][move[0][1]] = -1
        
        self.boardState[move[1][0]][move[1][1]] = currPlayer
        if jump:
            
            for enemy in move_info.jumpOver:
                self.boardState[enemy[0]][enemy[1]] = -1
       
        if jump:
            self.currPos[0] = self.calcPos(0)
            self.currPos[1] = self.calcPos(1)
        
        else:
            self.currPos[currPlayer].remove((move[0][0], move[0][1]))
            self.currPos[currPlayer].append((move[1][0], move[1][1]))
  

    def calcLegalMoves(self, player): 
        legalMoves = []
        hasJumps = False
        
        next = -1 if player == 0 else 1
        boardLimit = 0 if player == 0 else BOARD_SIZE-1
        
        for cell in self.currPos[player]:
            if (cell[0] == boardLimit):
                continue
           
            if (cell[1]!=BOARD_SIZE-1):
                
                if (self.boardState[cell[0]+next][cell[1]+1]==-1 and not hasJumps):
                    temp = Move((cell[0],cell[1]),(cell[0]+next,cell[1]+1)) 
                    legalMoves.append(temp)
                
                elif(self.boardState[cell[0]+next][cell[1]+1]==1-player):
                    jumps = self.checkJump((cell[0],cell[1]), False, player)
                    if (len(jumps)!=0):
                        
                        if not hasJumps:
                            hasJumps = True
                            legalMoves = []
                        legalMoves.extend(jumps)
            
            if (cell[1]!=0):
                if(self.boardState[cell[0]+next][cell[1]-1]==-1 and not hasJumps):
                    temp = Move((cell[0],cell[1]),(cell[0]+next,cell[1]-1)) 
                    legalMoves.append(temp)                    
                elif(self.boardState[cell[0]+next][cell[1]-1]==1-player):
                    jumps = self.checkJump((cell[0],cell[1]), True, player)
                    if (len(jumps)!=0):
                        if not hasJumps:
                            hasJumps = True
                            legalMoves = []                        
                        legalMoves.extend(jumps)
                        
        return legalMoves

    
    def checkJump(self, cell, isLeft, player):
        jumps = []
        next = -1 if player == 0 else 1
        
        if (cell[0]+next == 0 or cell[0]+next == BOARD_SIZE-1):
            return jumps
        
        if (isLeft):
            if (cell[1]>1 and self.boardState[cell[0]+next+next][cell[1]-2]==-1):
                temp = Move(cell, (cell[0]+next+next, cell[1]-2), True)
                temp.jumpOver = [(cell[0]+next,cell[1]-1)]
                
                helper = temp.end
                if (temp.end[0]+next > 0 and temp.end[0]+next < BOARD_SIZE-1):
                	
                	if (temp.end[1]>1 and self.boardState[temp.end[0]+next][temp.end[1]-1]==(1-player)):
                		test = self.checkJump(temp.end, True, player)
                		if (test != []):
                			dbl_temp = deepcopy(temp) 
                			dbl_temp.end = test[0].end 
                			dbl_temp.jumpOver.extend(test[0].jumpOver)
                			jumps.append(dbl_temp)                		
                	
                	if (temp.end[1]<BOARD_SIZE-2 and self.boardState[temp.end[0]+next][temp.end[1]+1]==(1-player)):
                		test = self.checkJump(temp.end, False, player)                	
                		if (test != []):
                			dbl_temp = deepcopy(temp) 
                			dbl_temp.end = test[0].end 
                			dbl_temp.jumpOver.extend(test[0].jumpOver)
                			jumps.append(dbl_temp)                     			
                jumps.append(temp)
        else:
        
            if (cell[1]<BOARD_SIZE-2 and self.boardState[cell[0]+next+next][cell[1]+2]==-1):
                
                temp = Move(cell, (cell[0]+next+next, cell[1]+2), True)
                temp.jumpOver = [(cell[0]+next,cell[1]+1)]
                
                if (temp.end[0]+next > 0 and temp.end[0]+next < BOARD_SIZE-1):
                	
                	if (temp.end[1]>1 and self.boardState[temp.end[0]+next][temp.end[1]-1]==(1-player)):
                		test = self.checkJump(temp.end, True, player)
                		if (test != []):
                			dbl_temp = deepcopy(temp) 
                			dbl_temp.end = test[0].end 
                			dbl_temp.jumpOver.extend(test[0].jumpOver)
                			jumps.append(dbl_temp)                     			
                	
                	if (temp.end[1]<BOARD_SIZE-2 and self.boardState[temp.end[0]+next][temp.end[1]+1]==(1-player)):
                		test = self.checkJump(temp.end, False, player) 
                		if (test != []):
                			dbl_temp = deepcopy(temp) 
                			dbl_temp.end = test[0].end 
                			dbl_temp.jumpOver.extend(test[0].jumpOver)
                			jumps.append(dbl_temp)                  			
                jumps.append(temp)                
    
        return jumps
    
    def calcPos(self, player):
        pos = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (self.boardState[row][col]==player):
                    pos.append((row,col))
        return pos
         
    def drawBoardState(self):
        for colnum in range(BOARD_SIZE):
            print(str(colnum)+" ",end="")
        print("")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (self.boardState[row][col] == -1):
                    print("+ ",end='')
                elif (self.boardState[row][col] == 1):
                    print("W ",end='')
                elif (self.boardState[row][col] == 0):
                    print("B ",end='')
            print(str(row))

    def setDefaultBoard(self):
        
        self.boardState = [
            [-1,1,-1,1,-1,1,-1,1],
            [1,-1,1,-1,1,-1,1,-1],
            [-1,1,-1,1,-1,1,-1,1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [0,-1,0,-1,0,-1,0,-1],
            [-1,0,-1,0,-1,0,-1,0],
            [0,-1,0,-1,0,-1,0,-1]
        ]



def main():
    print("Play as: ")
    print("(0) Black")
    print("(1) White")
    playr = int(input("Enter 0 or 1:"))
    while not (playr == 0 or playr == 1):
        playr = int(input("Invalid Choice, please try again: "))
    test = Game(playr)
    test.run()
    
main()
