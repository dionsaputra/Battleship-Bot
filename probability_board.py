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
	if cp[1] > 0 and adj_value(cp,'L') > 0:
		return 'L'
	elif cp[0] > 0 and adj_value(cp,'U') > 0:
		return 'U'
	elif cp[1] < size-1 and adj_value(cp,'R') > 0:
		return 'R'
	elif cp[0] < size-1 and adj_value(cp,'D') > 0:
		return 'D'

# INI BOARD
calc_prob()
show_board()
win_state = 'N'
stackHitPoint = []

# WIN == NO
while win_state != 'Y':
	calc_prob()
	show_board()
	target = get_target()
	print("Shoot at ",[target[0]+1,target[1]+1])
	board[target[0]][target[1]] = -1

	print("Hit? [Y/N]")
	status_hit = input()

	if status_hit == 'Y':
		calc_prob()
		show_board()
		
		sunk_all_hit = False
		change_direction = False
		cur_direction = get_direction(stackHitPoint[len(stackHitPoint)-1])
		while not sunk_all_hit:
			status_hit_dest = 'Y'
			if change_direction:
				cur_direction = get_direction(stackHitPoint[len(stackHitPoint)-1])

			while status_hit_dest == 'Y':
				stackHitPoint.append(target)
				cur_direction = get_direction(stackHitPoint[len(stackHitPoint)-1])
			
				target = adj_cell(stackHitPoint[len(stackHitPoint)-1],cur_direction)
				print("Shoot at ",[target[0]+1,target[1]+1])
				board[target[0]][target[1]] = -1

				print("Hit? [Y/N]")
				status_hit_dest = input()

				print("Sunk particular? [Y/N]")
				sunk_particular = input()

				if sunk_particular == 'Y':
					print("Legth of sunk ship? ")
					sunk_length = int(input())
					x = []
					for i in range(sunk_length):
						x = stackHitPoint.pop()
					change_direction = True
				else:
					change_direction = False

			if len(stackHitPoint) == 0:
				sunk_all_hit = True
			
	print('Win? [Y/N]: ',end='')
	win_state = input()