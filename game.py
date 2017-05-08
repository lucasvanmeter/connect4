#!/usr/bin/python3

from Board import Board
from Board import InvalidMove
from Player import Human
from Bot import *
	
'''
Game script
'''

#initialize board
board = Board(dimensions=[7,6], win=4)

#initialize players
players = [Human(), Bot(2,1)]

#start turn
turn = 0

#playTurn asks the next player to make a move. board.insert modifies the board at each step and will check to see if someone has won.
def playTurn():
	try:
		return board.insert(turn+1,players[turn].play(board))
	except InvalidMove as e:
		print(e)
		return playTurn()

#Finally we run the game, letting each player know whose turn it is, incrementing the turn number, and printing the board after each play. The game ends when board.instert returns true.
while True:
	print('Player %s turn:' % (turn+1))
	print(board)
	if playTurn():
		print('Player %s wins!' % (turn+1))
		print(board)
		break
	turn = (turn + 1) % len(players)