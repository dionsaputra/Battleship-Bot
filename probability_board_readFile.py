import sys, random
import json, os

size = 0
board = [[0 for j in range(size)] for i in range(size)]
ships=[['k1',2],['k2',3],['k3',3],['k4',4],['k5',5]]
curPoint = 0;
game_state_file = "state.json"
output_path = '.'
# phase = 0
ronde = 0
enemyShips = {};
state = {}

def main():
	global size, phase, state, enemyShips
	with open(os.path.join(output_path, game_state_file), 'r') as f_in:
		state = json.load(f_in)
	size = state['MapDimension']
	# phase = int(state['Phase'])
	ronde = int(state['Round'])
	enemyShips = state['OpponentMap']['Ships']
	print(size)
	# print(phase)
	print(ronde)
	# print(state['OpponentMap']['Ships'])
	# print (state)

def sumEnemyShips():
	i = 0
	for ships in enemyShips:
		if (ships['Destroyed'] == False):
			i += 1
		print (ships)
	return i

def delEnemyShips():
	i = 0
	step = 0
	for ships in enemyShips:
		if (ships['Destroyed'] == True):
			if (ships['ShipType'] == "Submarine"):
				step = 3
			elif (ships['ShipType'] == "Battleship"):
				step = 4
			elif (ships['ShipType'] == "Destroyer"):
				step = 2
			elif (ships['ShipType'] == "Cruiser"):
				step = 5
			elif (ships['ShipType'] == "Carrier"):
				step = 3
			del enemyShips[i]
		i += 1
	return step
main()
print(sumEnemyShips())
print("Popped ", delEnemyShips(), " times")
print(sumEnemyShips())
