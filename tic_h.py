# coding=UTF8
from copy import deepcopy
import serial
import syslog
import time

    
move_count=0

class Board:
 
  def __init__(self,other=None):
    self.player = 'X'
    self.opponent = 'O'
    self.empty = '.'
    self.size = 3
    self.fields = {}
    for y in range(self.size):
      for x in range(self.size):
        self.fields[x,y] = self.empty
    # copy constructor
    if other:
      self.__dict__ = deepcopy(other.__dict__)

  def reset_board():
    move_count=0
       self.fields = {}
    for y in range(self.size):
      for x in range(self.size):
        self.fields[x,y] = self.empty
  
  def move(self,x,y):
    board=Board(self)
    board.fields[x,y] = self.player
    (board.player,board.opponent) = (board.opponent,board.player)
    return board
  
  
  def __minimax(self, player):
    if self.won():
      if player:
        return (-1,None)
      else:
        return (+1,None)
    elif self.tied():
      return (0,None)
    elif player:
      best = (-2,None)
      for x,y in self.fields:
        if self.fields[x,y]==self.empty:
          value = self.move(x,y).__minimax(not player)[0]
          if value>best[0]:
            best = (value,(x,y))
      return best
    else:
      best = (+2,None)
      for x,y in self.fields:
        if self.fields[x,y]==self.empty:
          value = self.move(x,y).__minimax(not player)[0]
          if value<best[0]:
            best = (value,(x,y))
      return best
 
  def best(self):
    return self.__minimax(True)[1]
 
  def tied(self):
    for (x,y) in self.fields:
      if self.fields[x,y]==self.empty:
        return False
    return True
 
  def won(self):
    # horizontal
    for y in range(self.size):
      winning = []
      for x in range(self.size):
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
      if len(winning) == self.size:
        return winning
    # vertical
    for x in range(self.size):
      winning = []
      for y in range(self.size):
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
      if len(winning) == self.size:
        return winning
    # diagonal
    winning = []
    for y in range(self.size):
      x = y
      if self.fields[x,y] == self.opponent:
        winning.append((x,y))
    if len(winning) == self.size:
      return winning
    # other diagonal
    winning = []
    for y in range(self.size):
      x = self.size-1-y
      if self.fields[x,y] == self.opponent:
        winning.append((x,y))
    if len(winning) == self.size:
      return winning
    # default
    return None
 
  def __str__(self):
    string = ''
    for y in range(self.size):
      for x in range(self.size):
        string+=self.fields[x,y]
      string+="\n"
    return string


def data_in(board,ard_data):
    x=-1
    y=-1
    if(ard_data=='1'):
       x=0
       y=0
    elif(ard_data=='2'):
        x=1
        y=0
    elif(ard_data=='3'):
        x=2
        y=0
    elif(ard_data=='4'):
        x=0
        y=1
    elif(ard_data=='5'):
        x=1
        y=1
    elif(ard_data=='6'):
        x=2
        y=1
    elif(ard_data=='7'):
        x=0
        y=2
    elif(ard_data=='8'):
        x=1
        y=2
    elif(ard_data=='9'):
        x=2
        y=2
    
    print(x)
    print(y)
    board=board.move(x,y)
    return board


def send_data(board,ardui,ard2):
    [x,y]=board.best()
    if(x==0 and y==0):
       sd='1'
    elif(x==1 and y==0):
        sd='2'

    elif(x==2 and y==0):
        sd='3'
        
    elif(x==0 and y==1):
        sd='4'
        
    elif(x==1 and y==1):
        sd='5'
        
    elif(x==2 and y==1):
        sd='6'
        
    elif(x==0 and y==2):
        sd='7'
        
    elif(x==1 and y==2 ):
        sd='8'
    elif(x==2 and y==2):
        sd='9'
    ardui.write(sd)
    time.sleep(0.1)
    ard2.write(sd)
    print(sd)
    board=board.move(x,y)
    return board

  
def check(board):
  if board.won() :
    return 1
  if board.tied() :
    return 2

  return 0

  
if __name__ == '__main__':
    ch=0;
    board=Board()
#Start connection with arduino
    port = '/dev/ttyACM0'
    port2 = '/dev/ttyACM1'
    ard = serial.Serial(port,9600,timeout=5)
    ard2 = serial.Serial(port2,9600,timeout=5)
    time.sleep(2)
    i=0
    msg="0"
    pre_msg="0"
    ard2.write("s")
    while msg !="g":
        print ("pi:connection request sent")
        ard.write("s")
        msg= ard.read()
        print(msg)

    
    print("pi: connection established")
    ard.flushInput()
    done=1
    while 1:
         ard.flushInput()
         msg=pre_msg=msg= ard.read()
         while(pre_msg==msg):
           ard.write("t")
           msg= ard.read()
           print(msg)
           if msg !='1' and msg !='2' and msg !='3' and msg !='4' and msg !='5' and msg !='6' and msg !='7' and msg !='8' and msg !='9' :
              msg=pre_msg
           print("sssss")
           
         
         ard.write("r")
         board=data_in(board,msg)
         ch=check(board)
         print(board)
         if ch==1 :
           print("player won")
           time.sleep(10)
         elif ch==2 :
           print("tied")
           ard.write('a')
           ard2.write('a')
           time.sleep(10)
           ard.write('w')
           ard2.write('w')
           time.sleep(5)
           board.reset_board()

         
         if ch==0 and move_count==1:
           board=send_data(board,ard,ard2)
           ch=check(board)
           if ch==1 :
             print("computer won")
             ard.write('l')
             ard2.write('l')
             time.sleep(10)
             ard.write('w')
             ard2.write('w')
             time.sleep(5)
             board.reset_board()
           elif ch==2 :
             print("tied")
             ard.write('a')
             ard2.write('a')
             time.sleep(10)
             ard.write('w')
             ard2.write('w')
             time.sleep(5)
             board.reset_board()
             
 
          
         if move_count==0:
           if msg=='5':
             board=board.move(0,0)
             ard.write('1')
             time.sleep(1)
             ard2.write('1')
             move_count=1
           else :
             board=board.move(1,1)
             ard.write('5')
             time.sleep(1)
             ard2.write('5')
             move_count=1
             
           
         print (board)
          


















 

 
      
