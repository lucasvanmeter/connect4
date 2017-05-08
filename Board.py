#!/usr/bin/python3
from functools import reduce
from itertools import product
from copy import deepcopy

#When moves would fall out of the board we call an exception.
class InvalidMove(Exception):
	pass

class Board(list):
	
	#The Board will contain all the information about the game state.
	#USES PLANAR COORDINATES (EMBED IN R^n IN THE USUAL WAY)
	#
	def __init__(self,dimensions=[7,6],win=4,symbols={0:' ',1:'O',2:'X'}):
		super().__init__(
			reduce(lambda x,y: [deepcopy(x) for i in range(y)],[0]+[d for d in reversed(dimensions)])
		)
		self.symbols = symbols #a dictonary associating each player number with a symbol. Player zero is by default the empty string. The other player symbols are by defualt "O" and "X".
		self.dimensions = dimensions #The size of the board. Usually 7 by 6. Note that the board can be more than two-dimensional but the player classes might not be able to handle this yet.
		self.win = win #This sets the number of pieces in a row needed to win.
		self.directions = self.getDirections(len(self.dimensions)) #See getDirections below.
		
	#getSymbol returns the symbol associated to a player.
	def getSymbol(self,player_number):
			if player_number in self.symbols:
				return self.symbols[player_number]
			else:
				return str(player_number)
  
  #The following two methods will allow us to call locations on the board easily.
	def __getitem__(self,key):
		if type(key) is int:
			key = (key,)
		v = list(key)
		return reduce(lambda x,y: x.__getitem__(y), [super()] + v)
	
	def __setitem__(self,key,value):
		reduce(lambda x,y: x.__getitem__(y), [super()] + list(key[:-1]))[key[-1]] = value
	
	#gives list of all projective coordinates in base 3
	#using -1,0,1 in dimension n
	def getDirections(self,n):
		if n <= 1:
			return [[1]]
		else:
			return [[1] + list(x) for x in product(*[deepcopy([-1,0,1]) for i in range(n-1)])] + [[0] + x for x in self.getDirections(n-1) if sum([abs(c) for c in x]) is not 0]
	
	#The insert method will modify the board and returns true if winning play was made and false otherwise.
	def insert(self,player,position):
		if type(player) is not int or player is 0:
			raise InvalidMove('player must be non-negative integer')
		if type(position) is int:
			position = [position]
		else:
			position = list(position)
		try:
			i = self[position].index(0)
		except ValueError:
			raise InvalidMove('no position available there')
		except IndexError:
			raise InvalidMove('position does not exist')
		
		#If no exceptions are raised we will look where they want to play and change the player symbol for that position on the board.
		key = position+[i]
		try:
			self[key] = player
		except IndexError:
			raise InvalidMove('can not play there')
		#Finally we check if that player won. Since the player could only have won with their last move we simply add the longest string in each direction going out from that play.
		add = lambda x,y: [x[i]+y[i] for i in range(len(x))]
		#We iterate over all directions
		for d in self.directions:
			test = []
			for i in range(-self.win+1,self.win):
				try:
					test.append(str(self[add(key,[i*v for v in d])]))
				except IndexError:
					pass
			s = ''.join(test)
			if ''.join([str(player)]*self.win) in s:
				return True
		return False
	
	#When the board is called it will print itself.
	def __str__(self):
		if len(self.dimensions) is 2:
			M = [[self.getSymbol(self[x,self.dimensions[1]-1 - y]) for x in range(self.dimensions[0])] for y in range(self.dimensions[1])]
			horLine = '+' + '-+'*len(M[0])+'\n'
			newM = ['|'+'|'.join(row)+'|'+'\n' for row in M]
			return horLine+horLine.join(newM)+horLine
		else:
			return super().__str__()