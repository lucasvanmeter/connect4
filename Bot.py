#Auxillary functions
def print_board(board):
	for row in board:
		print(row)

def aux_streak(board,row,col,dir,sym):
	if (0 <= row + dir[0] <= len(board) - 1) and (0 <= col + dir[1] <= len(board[0])-1):
		if board[row+dir[0]][col+dir[1]] == sym:
			return 1 + aux_streak(board,row+dir[0],col+dir[1],dir,sym)
		else:
			return 0
	else:
		return 0

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

# board = [["1","*","*","*"],["1","1","*","*"],["2","1","*","*"],["1","1","*","*"],["2","2","2","*"]]

# class Position(object):
# 	def __init__(self, row, col, sym):
# 		self.row = row
# 		self.col = col
# 		self.sym = sym

# class board(object):
# 	def __init__(self, num_rows, num_cols, empty_sym)

# all_pos = [[Position(board, i, j) for j in range(len(board[0]))] for i in range(len(board))]
# for row in all_pos:
# 	for pos in row:
# 		print [pos.row, pos.col] 

class Bot(object):
# The robot will have a player number and a difficulty
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
		# print_board(strange_board)
		# print(" ")
		# print_board(board)
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
		#print "Possible plays", pos_play
		print(pos_play)
		# First the bot gathers information about streaks
		my_moves = {col : pot_str(board,pos_play[col],col,self.sym) for col in pos_play}
		#print "My streaks", my_moves
		other_moves = {col: pot_str(board,pos_play[col],col,self.other) for col in pos_play}
		#print "Enemy streaks", other_moves
		
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
		#print "scores for each col", scores
		for col in pos_play:
			if scores[col] == max_score:
				return col

# strange_board = [[1,1,0,0,0],[0,0,0,0,0],[1,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

# test_bot = Bot(2,1)

# print(test_bot.play(strange_board))
