#TODO
#1)player have property - whether he is II or human or other
#2)player have method of doing his turn
#3)game class have method of calling turn methods of all players
#4)fix win condition bug for j in range (0,self.numTurns // 2):  print((i + j)  % self.numTurns + 1,end=' ')
               

# cmd format: 0 param = python; 1st = script file path; 2..n - turns names; 
import sys
import binascii
import random
import hmac
import secrets
from hashlib import sha224 
from sys import getdefaultencoding

class Player:
    def __init__(self):
        self.turn = None    
    #def get_turn(self):
    #    return self.turn
    #def _set_turn(self, turn):
    #    self.turn = turn
    #turn = property(get_turn,_set_turn)
    
class Game:
    KEY_SIZE = 128
    TRUST_MODE_ACTIVATION_KEY = "t"
    BASIC_TURNS = ['stone', 'paper', 'scissors']
    END_GAME_KEY = -1
    def __init__(self, turns = BASIC_TURNS, isTrustMode = False):
        self.turns = turns
        self.numTurns = len(turns)
        self.players = [ Player(), Player() ] #player 0 is II
        self.isGameOver = False
        self.isTrustMode = isTrustMode
        self.hmac = None #uselles to store hmac object
        self.key = None
    def play(self):
        self.printRules()
        while not self.isGameOver:
            self.doIITurn()
            userTurn = self.askTurn()
            if userTurn == self.END_GAME_KEY:
                self.endGame()
            else:
                self.roundResult()
    def doIITurn(self):
        iiTurn = random.randint(0 ,self.numTurns - 1)
        self.players[0].turn = iiTurn #_set_turn(iiTurn)
        if not self.isTrustMode:
            self.generateAndPrintHMAC()
    def printRules(self):
        print('Rules:')
        print('If player and his opponent make the same turn round ends with draw.')
        print('Available turns are represented in first column. Turns of opponent in case of wich player wins are listed after colons:')
        for i in range(0, self.numTurns):
            print(i+1,') ',self.turns[i],': ', sep ='',end='')
            for j in range (0,self.numTurns // 2): 
                print(self.turns[(i + j + 1)  % self.numTurns],end=' ')
            print()
        print(end='\n\n')
    def askTurn(self):
        isValidTurn = False
        while not isValidTurn:
            print('Enter urs turn:',end=' ')
            turn = input() 
            try:
                turn = int(turn) - 1
                if turn < self.END_GAME_KEY or turn > self.numTurns - 1:
                    raise ValueError()
                isValidTurn = True
                self.players[1].turn = turn
            except:
                self.printHelp()
        return turn
    def endGame(self):
        print('Good bye!')
        self.isGameOver=True
    def printHelp(self):
        print('Available turns are: ', end='')
        for i in range(1, self.numTurns + 1):
            print(i,end=' ')
        print()
        print('For exit enter 0.')
    def roundResult(self):
        print("II turn is",self.turns[self.players[0].turn],'; user turn is',self.turns[self.players[1].turn])
        delta =  self.players[1].turn - self.players[0].turn #get_turn()
        II = self.players[0].turn
        User = self.players[1].turn
        half =  self.numTurns // 2
        if (delta) == 0:
            print ('draw')
        elif ((II + half > self.numTurns) and ((II + half) % self.numTurns >= User)) or ((II + half <= self.numTurns) and (II + half >= User) and (User>=II)):
            print ('II win')
        else:
            print ('user win')
        if not self.isTrustMode:
            self.provideComputerHonestyProof()
        print(end='\n\n')
    def generateAndPrintHMAC(self):
        self.key = secrets.token_hex(Game.KEY_SIZE) #token_hex token_bytes
        #h = hashlib.sha1() 
        #h.update(bytes(self.players[0].turn))
        self.hmac = hmac.new(binascii.unhexlify(self.key),digestmod=sha224) #player 0 is II  self.players[0].turn
        self.hmac.update(bytes(self.players[0].turn))
        print("II turn hmac:",self.hmac.hexdigest())
    def provideComputerHonestyProof(self):
        print("Key for HMAC was:",self.key) #self.key.decode('cp437')
   
try: 
    turns = sys.argv[1:len(sys.argv)]   #1 for exe/ 0 for debug
    numTurns = int(len(turns))
    if not numTurns % 2:
        raise ValueError() 
except:
    print("Number of turns must be uneven.")
    exit()
isTrustMode = True #trust mode disabled (False for enable)
for param in sys.argv:
    if param.lower() == Game.TRUST_MODE_ACTIVATION_KEY:
        isTrustMode = True  
theGame = Game(turns)
theGame.play()
