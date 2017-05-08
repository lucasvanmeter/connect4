#!/usr/bin/python3

#We want a generic class of players to play the game. We will implement both a human and bot to play.
class Player:
	
	def __init__(self):
		pass
	
	#should return key for where to play
	def play(self,board):
		raise Exception('Unimplemented')

#Human players will be asked to make a move when it is their turn to play.
class Human(Player):
	
	def getInput(self):
		try:
			return int(input('Where do you want to play? ---> '))
		except ValueError:
			print("I didn't catch that, try again:")
			return self.getInput()
	
	def play(self,board):
		return self.getInput()
			