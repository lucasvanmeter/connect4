#!/usr/bin/python3
from tabulate import tabulate
from functools import reduce
from itertools import product
from copy import deepcopy

class InvalidMove(Exception):
	pass

class Board(list):
	
	#
	#USES PLANAR COORDINATES (EMBED IN R^n IN THE USUAL WAY)
	#
	def __init__(self,dimensions=[5,5],win=4,symbols={0:' ',1:'O',2:'X'}):
		super().__init__(
			reduce(lambda x,y: [deepcopy(x) for i in range(y)],[0]+[d for d in reversed(dimensions)])
		)
		self.symbols = symbols
		self.dimensions = dimensions
		self.win = win
		self.directions = self.getDirections(len(self.dimensions)) #precomputed for speed
		
	def getSymbol(self,player_number):
			if player_number in self.symbols:
				return self.symbols[player_number]
			else:
				return str(player_number)

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
	
	#returns true if winning play
	#false otherwise
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
			raise InvalidMove('position doesnt exist')
		key = position+[i]
		try:
			self[key] = player
		except IndexError:
			raise InvalidMove('can not play there')
		#check if win
		add = lambda x,y: [x[i]+y[i] for i in range(len(x))]
		#iterate over all directions
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
	
	def __str__(self):
		if len(self.dimensions) is 2:
			return tabulate([[self.getSymbol(self[x,self.dimensions[1]-1 - y]) for x in range(self.dimensions[0])] for y in range(self.dimensions[1])],tablefmt='grid')
		else:
			return super().__str__()