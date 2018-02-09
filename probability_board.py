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
				print('  ',end=' ')
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
			if board[i][j] > 0:
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

def get_direction(cp): # cp adalah current point
	if cp[0] > 0 and cp[0] < size-1 and cp[1] > 0 and cp[1] < size-1:
		if adj_value(cp,'L') > 0:
			return 'L'
		elif adj_value(cp,'U') > 0:
			return 'U'
		elif adj_value(cp,'R') > 0:
			return 'R'
		elif adj_value(cp,'D') > 0:
			return 'D'
		else:
			return 'E'
	else:
		if cp[0] == 0 and cp[1] == 0:
			if adj_value(cp,'R') > 0:
				return 'R'
			elif adj_value(cp,'D') > 0:
				return 'D'
			else:
				return 'E'
		elif cp[0] == 0 and cp[1] == size-1:
			if adj_value(cp,'L') > 0:
				return 'L'
			elif adj_value(cp,'D') > 0:
				return 'D'
			else:
				return 'E'
		elif cp[0] == size-1 and cp[1] == 0:
			if adj_value(cp,'U') > 0:
				return 'U'
			elif adj_value(cp,'R') > 0:
				return 'R'
			else:
				return 'E'
		elif cp[0] == size-1 and cp[1] == size-1:
			if adj_value(cp,'U') > 0:
				return 'U'
			elif adj_value(cp,'L') > 0:
				return 'L'
			else:
				return 'E'
		elif cp[0] == 0:
			if adj_value(cp,'L') > 0:
				return 'L'
			elif adj_value(cp,'R') > 0:
				return 'R'
			elif adj_value(cp,'D') > 0:
				return 'D'
			else:
				return 'E'
		elif cp[0] == size-1:
			if adj_value(cp,'L') > 0:
				return 'L'
			elif adj_value(cp,'U') > 0:
				return 'U'
			elif adj_value(cp,'R') > 0:
				return 'R'
			else:
				return 'E'
		elif cp[1] == 0:
			print('case ini loh')
			if adj_value(cp,'U') > 0:
				return 'U'
			elif adj_value(cp,'R') > 0:
				return 'R'
			elif adj_value(cp,'D') > 0:
				return 'D'
			else:
				return 'E'
		elif cp[1] == size-1:
			if adj_value(cp,'L') > 0:
				return 'L'
			elif adj_value(cp,'U') > 0:
				return 'U'
			elif adj_value(cp,'D') > 0:
				return 'D'
			else:
				return 'E'
		else:
			return 'E'

def valid_cell (cp):
	return cp[0] >= 0 and cp[1] >= 0 and cp[0] < size and cp[1] < size

win = False
calc_prob()
show_board()
stack_hits = []
while not win:
	found = False
	while not found:
		target = get_target()
		print('Shoot at ',target[0]+1,target[1]+1)
		board[target[0]][target[1]] = -1
		calc_prob()
		show_board()


		print('Found new ships? [Y/N]',end=' ') 
		inp_found = input()
		if inp_found == 'Y':
			found = True

	sunk_all_hits = False
	cposidx = -1
	while not sunk_all_hits:
		stack_hits.append(target)
		cposidx += 1
		sunk_one = False

		while not sunk_one:
			startidx = cposidx
			direction = get_direction(stack_hits[cposidx])

			while direction != 'E' and len(stack_hits)>0 and  valid_cell(adj_cell(stack_hits[cposidx],direction)):
				target = adj_cell(stack_hits[cposidx],direction)
				print('Shoot at ',target[0]+1,target[1]+1)
				board[target[0]][target[1]] = -1
				calc_prob()
				show_board()

				print('Hit a ships? [Y/N]',end=' ') 
				inp_hit = input()
				if inp_hit == 'Y':
					stack_hits.append(target)
					cposidx += 1	

					print('Sunk one ship? [Y/N]',end=' ')
					inp_sunk_one = input()
					if inp_sunk_one == 'Y':
						sunk_one = True
						print('Ship length? ')
						inp_length = int(input())

						for i in range(inp_length):
							x = stack_hits.pop()
							cposidx -= 1
							
				else:
					print('Case not hit ',stack_hits, stack_hits[cposidx], direction)
					direction = get_direction(stack_hits[cposidx])

				#print('Case not sunk_one ',stack_hits, stack_hits[cposidx], direction)

			cposidx = startidx
			#print('Direction = E',stack_hits, stack_hits[cposidx], direction)

		#print('Case not sunk all hit ',stack_hits, stack_hits[cposidx], direction)
		if len(stack_hits) == 0:
			sunk_all_hits = True

	print(stack_hits)
	print('Win? [Y/N]',end=' ') 
	inp_win = input()
	if inp_win == 'Y':
		win = True