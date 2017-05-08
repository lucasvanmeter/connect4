#Auxillary functions used for testing.
def print_board(board):
	for row in board:
		print(row)

#The main method we will use to find good plays is to measure the "streaks" on the board. That is how long of a chain does a player have going through a given position on the board.
def aux_streak(board,row,col,dir,sym):
	if (0 <= row + dir[0] <= len(board) - 1) and (0 <= col + dir[1] <= len(board[0])-1):
		if board[row+dir[0]][col+dir[1]] == sym:
			return 1 + aux_streak(board,row+dir[0],col+dir[1],dir,sym)
		else:
			return 0
	else:
		return 0

#We name the directions for readability.
def pot_str(board,row,col,key):
	n = aux_streak(board, row, col, [-1,0], key)
	s = aux_streak(board, row, col, [1,0], key)
	e = aux_streak(board, row, col, [0,1], key)
	w = aux_streak(board, row, col, [0,-1], key)
	ne = aux_streak(board, row, col, [-1,1], key)
	sw = aux_streak(board, row, col, [1,-1], key)
	se = aux_streak(board, row, col, [1,1], key)
	nw = aux_streak(board, row, col, [-1,-1], key)
	return [n + s, ne + sw, e + w, se + nw]

class Bot(object):
# The robot will have a player number and also knows the number of its opponent.
	def __init__(self, sym, other):
		self.sym = sym
		self.other = other
# The play method will make a single move
	def play(self, strange_board):
		# First the bot identifies the squares it could play in. This will
		# be stored as a dictonary in the form (col:row)
		board = [\
			[strange_board[x][y] \
			for x in range(len(strange_board))] \
			for y in reversed(range(len(strange_board[0]))) \
			]
		num_cols = range(len(board[0]))
		list_cols = [[row[i] for row in board]for i in num_cols]
		pos_play = {}
		for i in num_cols:
			if 0 not in list_cols[i]:
				pass
			elif self.sym not in list_cols[i] and self.other not in list_cols[i]:
				pos_play[i] = len(board) - 1
			else:
				for row in range(len(board)):
					if 	board[row][i] != 0 and board[row -1][i] == 0:
						pos_play[i] = row - 1
		# Now the bot gathers information about streaks for both players.
		my_moves = {col : pot_str(board,pos_play[col],col,self.sym) for col in pos_play}
		other_moves = {col: pot_str(board,pos_play[col],col,self.other) for col in pos_play}
	
		# Next the bot will evaluate if it can win in the next move
		for col in my_moves:
			if 3 in my_moves[col]:
				return col
		
		# If it can't win it will next make sure to stop opponent
		for col in other_moves:
			if 3 in other_moves[col]:
				return col
		
		# Now comes the tricky part. The strategy for now is as follows:
		# For each move we add up all of the streaks in any direction for both players
		# and use this to pick our next move
		scores = {col:sum(my_moves[col]) + sum(other_moves[col]) for col in pos_play}
		max_score = max(scores.values())
		for col in pos_play:
			if scores[col] == max_score:
				return col
				
		#Currently the main mistake the bot makes is to play a move that allows the other player to win on their next turn. Future work should fix this, possibly by just looking forward a couple of turns.