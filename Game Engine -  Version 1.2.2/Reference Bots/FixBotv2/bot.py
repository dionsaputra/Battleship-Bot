import argparse
import json
import os
from random import randint

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0

def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    opponent_map = state['OpponentMap']['Cells']
    opponent_ships = state['OpponentMap']['Ships']

    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(opponent_map,opponent_ships)


def output_shot(x, y):
    move = 1  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def ship_length(ship_type):
    if ship_type == "Submarine":
        return 3
    elif ship_type == "Battleship":
        return 4
    elif ship_type == "Destroyer":
        return 2
    elif ship_type == "Cruiser":
        return 5
    elif ship_type == "Carrier":
        return 3


def huntingMode(opponent_map,opponent_ships):
    totalStar = 0
    for cell in opponent_map:
        if cell['Damaged']:
            totalStar += 1

    totalShipLength = 0
    for ship in opponent_ships:
        totalShipLength += ship_length(ship['ShipType'])

    return totalStar == 17 - totalShipLength

def get_last_hit(opponent_map):
    cur_cell_idx = (map_size*map_size) - 1
    
    while cur_cell_idx >= 0 and not opponent_map[cur_cell_idx]['Damaged']:
        cur_cell_idx -= 1

    return opponent_map[cur_cell_idx]

def fill_probability(board,ship,orient_const,start,end,orient_stat):
    cur_ship_length = ship_length(ship['ShipType'])
    if end-start+1 >= cur_ship_length:
        for i in range(start,end-cur_ship_length+2):
            for j in range(cur_ship_length):
                if orient_stat == "horizontal" and board[orient_const][i+j] >= 0:
                    board[orient_const][i+j] += 1
                elif orient_stat == "vertical" and board[i+j][orient_const] >= 0:
                    board[i+j][orient_const] += 1

def get_max_length_ship(opponent_ships):
    max_length = 0
    for ship in opponent_ships:
        if ship_length(ship['ShipType']) > max_length:
            max_length = ship_length(ship['ShipType'])
    return max_length

def calculate_probability(board,mode,opponent_map,opponent_ships):

    if mode == "hunting":
        for cell in opponent_map:
            if cell['Damaged'] or cell['Missed']:
                board[cell['X']][cell['Y']] = -1

        # arah horizontal
        for i in range(map_size):
            j = 0
            while j<map_size:
                end = j
                while end < map_size and board[i][end] != -1:
                    end += 1
                end -= 1
                for ship in opponent_ships:
                    fill_probability(board,ship,i,j,end,"horizontal")
                j = end+2
        
        # arah vertikal
        for i in range(map_size):
            j = 0      
            while j<map_size:
                end = j
                while end < map_size and board[end][i] != -1:
                    end += 1
                end -= 1
                for ship in opponent_ships:
                    fill_probability(board,ship,i,j,end,"vertical")
                j = end+2
        target = get_target(board,opponent_map)

    else: # mode == "destroy"
        max_length = get_max_length_ship(opponent_ships)
        for cell in opponent_map:
            if cell['Missed']:
                board[cell['X']][cell['Y']] = -1

        target = [0,0]
        value = board[target[0]][target[1]]
        for cell in opponent_map:
            if cell['Damaged']:
                ref_cell = cell    
                
                # arah horizontal dari ref_cell
                start = ref_cell['Y']
                step = 0
                while start >= 0 and step <= max_length and board[ref_cell['X']][start] != -1:
                    start -= 1 
                start += 1

                end = ref_cell['Y']
                step = 0
                while end < map_size and step <= max_length and board[ref_cell['X']][end] != -1:
                    end += 1
                end -= 1
                for ship in opponent_ships:
                    fill_probability(board,ship,ref_cell['X'],start,end,"horizontal")

                # arah vertical dar ref_cell
                start = ref_cell['X']
                step = 0
                while start >= 0 and step <= max_length and board[start][ref_cell['Y']] != -1:
                    start -= 1 
                start += 1

                end = ref_cell['X']
                step = 0
                while end < map_size and step <= max_length and board[end][ref_cell['Y']] != -1:
                    end += 1
                end -= 1
                for ship in opponent_ships:
                    fill_probability(board,ship,ref_cell['Y'],start,end,"vertical")

                candidattarget = get_target(board,opponent_map)
                if board[candidattarget[0]][candidattarget[1]] > value:
                	target = candidattarget
                	value = board[candidattarget[0]][candidattarget[1]]

               	for newcell in opponent_map:
               		if newcell['Missed']:
               			board[newcell['X']][newcell['Y']] = -1
               		else:
               			board[newcell['X']][newcell['Y']] = 0

    return target

def get_target(board,opponent_map):
    maxRow = 0
    maxCol = 0
    for i in range(map_size):
        for j in range(map_size):
            idxcell = i*map_size + j
            if board[i][j] > board[maxRow][maxCol] and not opponent_map[idxcell]['Damaged']:
                maxRow = i
                maxCol = j

    return [maxRow,maxCol]

def show_board(board):
    for i in range(map_size):
        for j in range(map_size):
            if board[i][j] == -1:
                print('-1',end=' ')
            else:
                val = str(board[i][j])
                if len(val) == 1:
                    val = '0'+val
                
                print(val,end=' ')
        print()
    print()

def fire_shot(opponent_map,opponent_ships):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)

    board = [[0 for j in range(map_size)] for i in range(map_size)]
    
    if huntingMode(opponent_map,opponent_ships):
        target = calculate_probability(board,"hunting",opponent_map,opponent_ships)
    else: # in destroy mode
        target = calculate_probability(board,"destroy",opponent_map,opponent_ships)                

 
    output_shot(*target)
    return

def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    ships = ['Battleship 1 0 north',
             'Carrier 3 1 East',
             'Cruiser 4 2 north',
             'Destroyer 7 3 north',
             'Submarine 1 8 East'
             ]

    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
