#!/usr/bin/python3

from Board import Board
from Board import InvalidMove
from Player import Human
	
'''
Game script
'''

#initialize board
board = Board(dimensions=[5,5], win=4)

#initialize players
players = [Human(), Human()]

#start turn
turn = 0

def play():
	try:
		return board.insert(turn+1,players[turn].play(board))
	except InvalidMove as e:
		print(e)
		return play()

while True:
	print('Player %s turn:' % (turn+1))
	if play():
		print('Player %s wins!' % (turn+1))
		break
	turn = (turn + 1) % len(players)