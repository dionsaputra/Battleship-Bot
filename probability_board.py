import sys

size = 10
board = [[0 for j in range(size)] for i in range(size)]
ships=[['k1',2],['k2',3],['k3',3],['k4',4],['k5',5]]

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
					val = '00'+val
				elif len(val) == 2:
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

def update_prob_hunt():
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


def update_prob_dest(point):
	for i in range(size):
		for j in range(size):
			if board[i][j] != -1:
				board[i][j] = 0
	for ship in ships:
		shipLen = ship[1]
		limStartHor = point[1]-shipLen+1 if point[1]-shipLen+1 >= 0 else 0
		limEndHor = point[1]+shipLen-1 if point[1]+shipLen-1 <= size-1 else size-1
		limStartVer = point[0]-shipLen+1 if point[0]-shipLen+1 >= 0 else 0
		limEndVer = point[0]+shipLen-1 if point[0]+shipLen-1 <= size-1 else size-1

		startHor = point[1]-1
		while startHor >= limStartHor and board[point[0]][startHor] != -1:
			startHor -= 1
		startHor += 1
	
		endHor = point[1]+1
		while endHor <= limEndHor and board[point[0]][endHor] != -1:
			endHor += 1
		endHor -= 1

		startVer = point[0]-1
		while startVer >= limStartVer and board[startVer][point[1]] != -1:
			startVer -= 1
		startVer += 1

		endVer = point[0]+1
		while endVer <= limEndVer and board[endVer][point[1]] != -1:
			endVer += 1
		endVer -= 1

		fill_prob(ship,point[0],startHor,endHor,1)
		fill_prob(ship,point[1],startVer,endVer,0)

update_prob_hunt()
while True:
	rowmax = 0
	colmax = 0
	maxval = board[rowmax][colmax]
	for i in range(size):
		for j in range(size):
			if board[i][j] > maxval:
				rowmax,colmax,maxval = i,j,board[i][j]
	print("Shoot at ",[rowmax+1,colmax+1])
	hit = input()
	board[rowmax][colmax] = -1
	if hit=='1':
		print('hit')
		update_prob_dest([rowmax,colmax])
		show_board()
	else:
		print('miss')
		update_prob_hunt()
		show_board()
