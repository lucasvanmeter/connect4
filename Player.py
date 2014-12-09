#!/usr/bin/python3

class Player:
	
	def __init__(self):
		pass
	
	#should return key for where to play
	def play(self,board):
		raise Exception('Unimplemented')

#example
class Human(Player):
	
	def getInput(self):
		try:
			return int(input('Where to play ---> '))
		except ValueError:
			print("I didn't catch that, try again:")
			return self.getInput()
	
	def play(self,board):
		print("The board looks like \n %s" % board)
		return self.getInput()
			