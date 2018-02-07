import sys

size = 10
ships=[['k1',2],['k2',3],['k3',3],['k4',4],['k5',5]]
board = [[0 for j in range(size)] for i in range(size)]

def delay():
	for i in range(20000000):
		k = 1

def show_board():
	for i in range(size):
		for j in range(size):
			if board[i][j] == -1:
				print('   ',end=' ')
			else:
				val = str(board[i][j])
				if len(val) == 1:
					val = '0'+val
				
				print(val,end=' ')
		print()
	print()

def fill_prob(ship,pos,start,end,hor):
	if end-start+1 >= ship[1]:
		for i in range(start,end-ship[1]+2):
			for j in range(ship[1]):
				if hor == 1 and board[pos][i+j] >= 0:
					board[pos][i+j] += 1
				elif hor == 0 and board[i+j][pos] >= 0:
					board[i+j][pos] += 1

def calc_prob():
	for i in range(size):
		for j in range(size):
			if board[i][j] != -1:
				board[i][j] = 0	

	# arah horizontal
	for i in range(size):
		j = 0
		while j<size:
			end = j
			while end < size and board[i][end] != -1:
				end += 1
			end -= 1
			for ship in ships:
				fill_prob(ship,i,j,end,1)
			j = end+2
	# arah vertikal
	for i in range(size):
		j = 0
		while j<size:
			end = j
			while end < size and board[end][i] != -1:
				end += 1
			end -= 1
			for ship in ships:
				fill_prob(ship,i,j,end,0)
			j = end+2

def get_target():
	maxRow = 0
	maxCol = 0
	for i in range(size):
		for j in range(size):
			if board[i][j] > board[maxRow][maxCol]:
				maxRow = i
				maxCol = j

	return [maxRow,maxCol]

def adj_cell(cp,direction):
	if direction == 'L':
		return [cp[0],cp[1]-1]
	elif direction == 'U':
		return [cp[0]-1,cp[1]]
	elif direction == 'R':
		return [cp[0],cp[1]+1]
	else:
		return [cp[0]+1,cp[1]]

def adj_value(cp,direction):
	if direction == 'L':
		return board[cp[0]][cp[1]-1]
	elif direction == 'U':
		return board[cp[0]-1][cp[1]]
	elif direction == 'R':
		return board[cp[0]][cp[1]+1]
	else:
		return board[cp[0]+1][cp[1]]

def get_target_adj(cp): # cp adalah current point
	if cp[0] == 0:
		if cp[1] == 0:
			if adj_value(cp,'D') > adj_value(cp,'R'):
				return [adj_cell(cp,'D'),'D']
			else:
				return [adj_cell(cp,'R'),'R']
		elif curPoint[1] == size-1:
			if adj_value(cp,'L') > adj_value(cp,'D'):
				return [adj_cell(cp,'L'),'L']
			else:
				return [adj_cell(cp,'D'),'D']
		else:
			if adj_value(cp,'L') > adj_value(cp,'D') and adj_value(cp,'L') > adj_value(cp,'R'):
				return [adj_cell(cp,'L'),'L']
			elif adj_value(cp,'D') > adj_value(cp,'L') and adj_value(cp,'D') > adj_value(cp,'R'):
				return [adj_cell(cp,'D'),'D']
			else:
				return [adj_cell(cp,'R'),'R']
	elif cp[0] == size-1:
		if cp[1] == 0:
			if adj_value(cp,'U') > adj_value(cp,'R'):
				return [adj_cell(cp,'U'),'U']
			else:
				return [adj_cell(cp,'R'),'R']
		elif cp[1] == size-1:
			if adj_value(cp,'U') > adj_value(cp,'L'):
				return [adj_cell(cp,'U'),'U']
			else:
				return [adj_cell(cp,'L'),'L']
		else:
			if adj_value(cp,'L') > adj_value(cp,'U') and adj_value(cp,'L') > adj_value(cp,'R'):
				return [adj_cell(cp,'L'),'L']
			elif adj_value(cp,'U') > adj_value(cp,'L') and adj_value(cp,'U') > adj_value(cp,'R'):
				return [adj_cell(cp,'U'),'U']
			else:
				return [adj_cell(cp,'R'),'R']
	else:
		if cp[1] == 0:
			if adj_value(cp,'D') > adj_value(cp,'U') and adj_value(cp,'D') > adj_value(cp,'R'):
				return [adj_cell(cp,'D'),'D']
			elif adj_value(cp,'U') > adj_value(cp,'D') and adj_value(cp,'U') > adj_value(cp,'R'):
				return [adj_cell(cp,'U'),'U']
			else:
				return [adj_cell(cp,'R'),'R']
		elif cp[1] == size-1:
			if adj_value(cp,'L') > adj_value(cp,'U') and adj_value(cp,'L') > adj_value(cp,'D'):
				return [adj_cell(cp,'L'),'L']
			elif adj_value(cp,'U') > adj_value(cp,'L') and adj_value(cp,'U') > adj_value(cp,'D'):
				return [adj_cell(cp,'U'),'U']
			else:
				return [adj_cell(cp,'D'),'D']			
		else:
			if adj_value(cp,'L')>adj_value(cp,'U') and adj_value(cp,'L')>adj_value(cp,'R') and adj_value(cp,'L')>adj_value(cp,'D'):
				return [adj_cell(cp,'L'),'L']
			elif adj_value(cp,'U')>adj_value(cp,'L') and adj_value(cp,'U')>adj_value(cp,'R') and adj_value(cp,'U')>adj_value(cp,'D'):
				return [adj_cell(cp,'U'),'U']
			elif adj_value(cp,'R')>adj_value(cp,'L') and adj_value(cp,'R')>adj_value(cp,'U') and adj_value(cp,'R')>adj_value(cp,'D'):
				return [adj_cell(cp,'R'),'R']
			else:
				return [adj_cell(cp,'D'),'D']

calc_prob()
win = False
while not win:
	show_board()
	target = get_target()
	print("Shoot at ",[target[0]+1,target[1]+1])
	print("Input status [0. hit, 1. miss]", end=' ')
	status_hit = input()
	if status_hit == '0':
		status_sunk = '3'
		while status_sunk != '2':
			board[target[0]][target[1]] = -1
			calc_prob()
			print('Destroy mode active')
			
			
			target = get_target_adj(target)
			print("Shoot at ",[target[0]+1,target[1]+1])
			print("Input status [2. sunk, 3. not sunk]", end=' ')
			status_sunk = input()
	else:
		board[target[0]][target[1]] = -1
		calc_prob()