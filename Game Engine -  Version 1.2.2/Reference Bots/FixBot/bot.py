import argparse
import json
import os
from random import choice

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0

####################### FUNGSI PENGHITUNG PROBABILITAS  #########################

# input tipe kapal, otput panjang kapal dengan tipe tersebut
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

# mendapatkan ukuran kapal terpanjang dalam list kapal
def get_max_length_ship(opponent_ships):
    max_length = 0
    for ship in opponent_ships:
        if ship_length(ship['ShipType']) > max_length:
            max_length = ship_length(ship['ShipType'])
    return max_length

# true jika state sekarang adalah state hunting
def huntingMode(opponent_map,opponent_ships):
    totalStar = 0
    for cell in opponent_map:
        if cell['Damaged']:
            totalStar += 1

    totalShipLength = 0
    for ship in opponent_ships:
        totalShipLength += ship_length(ship['ShipType'])

    return totalStar == 17 - totalShipLength

# mengisi sebuah space (row atau column) dengan nilai probabilitasnya
def fill_probability(board,ship,orient_const,start,end,orient_stat):
    cur_ship_length = ship_length(ship['ShipType'])
    if end-start+1 >= cur_ship_length:
        for i in range(start,end-cur_ship_length+2):
            for j in range(cur_ship_length):
                if orient_stat == "horizontal" and board[orient_const][i+j] >= 0:
                    board[orient_const][i+j] += 1
                elif orient_stat == "vertical" and board[i+j][orient_const] >= 0:
                    board[i+j][orient_const] += 1

# menhitung matriks kerapatan peluang
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

    else: # mode == "destroy"
        max_length = get_max_length_ship(opponent_ships)
        for cell in opponent_map:
            if cell['Missed']:
                board[cell['X']][cell['Y']] = -1

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

    return board

# mendapatkan cell dengan probabilitas tertinggi
def get_target(board,opponent_map):
    maxval = 0
    for i in range(map_size):
        for j in range(map_size):
            idxcell = i*map_size + j
            if board[i][j] > maxval and not opponent_map[idxcell]['Damaged']:
                maxval = board[i][j]

    targets = []
    for i in range(map_size):
        for j in range(map_size):
            idxcell = i*map_size + j
            if board[i][j] == maxval and not opponent_map[idxcell]['Damaged']:
                valid_cell = [i,j]
                targets.append(valid_cell)

    target = choice(targets)
    return target

# menampilkan matriks kerapatan peluang
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


####################### PENGATURAN SENJATA    #########################
# membuat list objek weapon
def weaponAvailable(ourShips):
    weapon = []
    data = ourShips[0]['Weapons'][0]
    data["Destroyed"] = ourShips[0]["Destroyed"]
    weapon.append(data)

    for ships in ourShips:
        data = ships['Weapons'][1]
        data["Destroyed"] = ships["Destroyed"]
        weapon.append(data)

    return weapon

def weapon_energy(weapon_type):
    if weapon_type == 'DoubleShot':
        scale = 8
    elif weapon_type == 'CornerShot':
        scale = 10
    elif weapon_type == 'DiagonalCrossShot':
        scale = 12
    elif weapon_type == 'CrossShot':
        scale = 14
    elif weapon_type == 'SeekerMissile':
        scale = 10
    return scale * (1 + (map_size/4))

def check_energy(energy,weapon_type):
    return energy >= weapon_energy(weapon_type)

def spesific_weapon_available(weapons,weapon_type):
    for weapon in weapons:
        if weapon['WeaponType'] == weapon_type:
            return True
    return False

def move_code(weapon_type):
    if weapon_type == 'DoubleShot':
        return 2
    elif weapon_type == 'CornerShot':
        return 4
    elif weapon_type == 'DiagonalCrossShot':
        return 5
    elif weapon_type == 'CrossShot':
        return 6
    elif weapon_type == 'SeekerMissile':
        return 7

def chooseWeapon(ourShips,energy,mode):
    weapons = weaponAvailable(ourShips)
    weapon_choose = 1
    if mode == 'hunting':
        hunting_prior = ['SeekerMissile','DiagonalCrossShot','CornerShot','CrossShot','DoubleShot']
        for weapon_type in hunting_prior:
            if spesific_weapon_available(weapons,weapon_type) and check_energy(energy,weapon_type):
                weapon_choose = move_code(weapon_type)
                break
    elif mode == 'destroy':
        destroy_prior = ['CrossShot','DiagonalCrossShot','CornerShot','DoubleShot','SeekerMissile']
        for weapon_type in destroy_prior:
            if spesific_weapon_available(weapons,weapon_type) and check_energy(energy,weapon_type):
                weapon_choose = move_code(weapon_type)
                break

    return weapon_choose

def adj_cell(cp,direction):
    if direction == 'L':
        return [cp[0],cp[1]-1]
    elif direction == 'U':
        return [cp[0]-1,cp[1]]
    elif direction == 'R':
        return [cp[0],cp[1]+1]
    else:
        return [cp[0]+1,cp[1]]

def adj_value(board,cp,direction):
    if direction == 'L':
        return board[cp[0]][cp[1]-1]
    elif direction == 'U':
        return board[cp[0]-1][cp[1]]
    elif direction == 'R':
        return board[cp[0]][cp[1]+1]
    else:
        return board[cp[0]+1][cp[1]]

def valid_config(move_code,target,no_conf):
    if move_code == 2:
        if no_conf == 1:
            return target[1] >= 2
        elif no_conf == 2:
            return target[1] <= map_size-3
    elif move_code == 3:
        if no_conf == 1:
            return target[0] >= 2
        elif no_conf == 2:
            return target[0] <= map_size-3
    elif move_code == 4:
        if no_conf == 1:
            return target[0] >= 2 and target[1] >= 2
        elif no_conf == 2:
            return target[0] >= 2 and target[1] <= map_size-3
        elif no_conf == 3:
            return target[0] <= map_size-3 and target[1] <= map_size-3
        elif no_conf == 4:
            return target[0] <= map_size-3 and target[1] >= 2
    elif move_code == 5:
        if no_conf == 1:
            return target[0] >= 2 and target[1] >= 2
        elif no_conf == 2:
            return target[0] >= 2 and target[1] <= map_size-3
        elif no_conf == 3:
            return target[0] <= map_size-3 and target[1] <= map_size-3
        elif no_conf == 4:
            return target[0] <= map_size-3 and target[1] >= 2
        elif no_conf == 5:
            return target[0] >= 1 and target[0] <= map_size-2 and target[1] >= 1 and target[1] <= map_size-2
    elif move_code == 6:
        if no_conf == 1:
            return target[0] >= 2 and target[1] >= 1 and target[1] <= map_size-2
        elif no_conf == 2:
            return target[1] <= map_size-3 and target[0] >= 1 and target[0] <= map_size-2
        elif no_conf == 3:
            return target[0] <= map_size-3 and target[1] >= 1 and target[1] <= map_size-2
        elif no_conf == 4:
            return target[1] >= 2 and target[0] >= 1 and target[0] <= map_size-2
        elif no_conf == 5:
            return target[0] >= 1 and target[0] <= map_size-2 and target[1] >= 1 and target[1] <= map_size-2
    elif move_code == 7:
        return True

def is_max_4_value(testee,tester1,tester2,tester3):
    return testee >= tester1 and testee >= tester2 and testee >= tester3

def is_max_5_value(testee,tester1,tester2,tester3,tester4):
    return testee >= tester1 and testee >= tester2 and testee >= tester3 and testee >= tester4

def best_config(board,move_code,target):
    min_inf = -1000000
    x = target[0]
    y = target[1]
    if move_code == 1:
        return [move_code,[x,y]]
    elif move_code == 2:
        sum_conf_2_1 = board[x][y] + board[x][y-2] if valid_config(2,target,1) else min_inf
        sum_conf_2_2 = board[x][y] + board[x][y+2] if valid_config(2,target,2) else min_inf
        sum_conf_3_1 = board[x][y] + board[x-2][y] if valid_config(3,target,1) else min_inf
        sum_conf_3_2 = board[x][y] + board[x+2][y] if valid_config(3,target,2) else min_inf

        if is_max_4_value(sum_conf_2_1,sum_conf_2_2,sum_conf_3_1,sum_conf_3_2):
            return [2,[x,y-1]]
        elif is_max_4_value(sum_conf_2_2,sum_conf_2_1,sum_conf_3_1,sum_conf_3_2):
            return [2,[x,y+1]]
        elif is_max_4_value(sum_conf_3_1,sum_conf_2_1,sum_conf_2_2,sum_conf_3_2):
            return [3,[x-1,y]]
        elif is_max_4_value(sum_conf_3_2,sum_conf_2_1,sum_conf_2_2,sum_conf_3_1):
            return [3,[x+1,y]]
        
    elif move_code == 4:
        sum_conf_1 = board[x][y] + board[x-2][y-2] + board[x-2][y] + board[x][y-2] if valid_config(move_code,target,1) else min_inf
        sum_conf_2 = board[x][y] + board[x-2][y] + board[x-2][y+2] + board[x][y+2] if valid_config(move_code,target,2) else min_inf
        sum_conf_3 = board[x][y] + board[x][y+2] + board[x+2][y+2] + board[x+2][y] if valid_config(move_code,target,3) else min_inf
        sum_conf_4 = board[x][y] + board[x][y-2] + board[x+2][y] + board[x+2][y-2] if valid_config(move_code,target,4) else min_inf

        if is_max_4_value(sum_conf_1,sum_conf_2,sum_conf_3,sum_conf_4):
            return [move_code,[x-1,y-1]]
        elif is_max_4_value(sum_conf_2,sum_conf_1,sum_conf_3,sum_conf_4):
            return [move_code,[x-1,y+1]]
        elif is_max_4_value(sum_conf_3,sum_conf_2,sum_conf_1,sum_conf_4):
            return [move_code,[x+1,y+1]]
        elif is_max_4_value(sum_conf_4,sum_conf_2,sum_conf_3,sum_conf_1):
            return [move_code,[x+1,y-1]]

    elif move_code == 5:
        sum_conf_1 = board[x][y] + board[x-2][y-2] + board[x-2][y] + board[x][y-2] + board[x-1][y-1] if valid_config(move_code,target,1) else min_inf
        sum_conf_2 = board[x][y] + board[x-2][y] + board[x-2][y+2] + board[x][y+2] + board[x-1][y+1] if valid_config(move_code,target,2) else min_inf
        sum_conf_3 = board[x][y] + board[x][y+2] + board[x+2][y+2] + board[x+2][y] + board[x+1][y+1] if valid_config(move_code,target,3) else min_inf
        sum_conf_4 = board[x][y] + board[x][y-2] + board[x+2][y] + board[x+2][y-2] + board[x+1][y-1] if valid_config(move_code,target,4) else min_inf
        sum_conf_5 = board[x][y] + board[x-1][y-1] + board[x-1][y+1] + board[x+1][y+1] + board[x+1][y-1] if valid_config(move_code,target,5) else min_inf

        if is_max_5_value(sum_conf_1,sum_conf_2,sum_conf_3,sum_conf_4,sum_conf_5):
            return [move_code,[x-1,y-1]]
        elif is_max_5_value(sum_conf_2,sum_conf_1,sum_conf_3,sum_conf_4,sum_conf_5):
            return [move_code,[x-1,y+1]]
        elif is_max_5_value(sum_conf_3,sum_conf_2,sum_conf_1,sum_conf_4,sum_conf_5):
            return [move_code,[x+1,y+1]]
        elif is_max_5_value(sum_conf_4,sum_conf_2,sum_conf_3,sum_conf_1,sum_conf_5):
            return [move_code,[x+1,y-1]]
        elif is_max_5_value(sum_conf_5,sum_conf_2,sum_conf_3,sum_conf_4,sum_conf_1):
            return [move_code,[x,y]]

    elif move_code == 6:
        sum_conf_1 = board[x][y] + board[x-2][y] + board[x-1][y-1] + board[x-1][y] + board[x-1][y+1] if valid_config(move_code,target,1) else min_inf
        sum_conf_2 = board[x][y] + board[x-1][y+1] + board[x][y+2] + board[x][y+1] + board[x+1][y+1] if valid_config(move_code,target,2) else min_inf
        sum_conf_3 = board[x][y] + board[x+1][y-1] + board[x+1][y] + board[x+1][y+1] + board[x+2][y] if valid_config(move_code,target,3) else min_inf
        sum_conf_4 = board[x][y] + board[x-1][y-1] + board[x][y-2] + board[x][y-1] + board[x+1][y-1] if valid_config(move_code,target,4) else min_inf
        sum_conf_5 = board[x][y] + board[x-1][y] + board[x][y-1] + board[x][y+1] + board[x+1][y] if valid_config(move_code,target,5) else min_inf

        if is_max_5_value(sum_conf_1,sum_conf_2,sum_conf_3,sum_conf_4,sum_conf_5):
            return [move_code,[x-1,y]]
        elif is_max_5_value(sum_conf_2,sum_conf_1,sum_conf_3,sum_conf_4,sum_conf_5):
            return [move_code,[x,y+1]]
        elif is_max_5_value(sum_conf_3,sum_conf_2,sum_conf_1,sum_conf_4,sum_conf_5):
            return [move_code,[x+1,y]]
        elif is_max_5_value(sum_conf_4,sum_conf_2,sum_conf_3,sum_conf_1,sum_conf_5):
            return [move_code,[x,y-1]]
        elif is_max_5_value(sum_conf_5,sum_conf_2,sum_conf_3,sum_conf_4,sum_conf_1):
            return [move_code,[x,y]]
    elif move_code == 7:
        return [move_code,[x,y]]

####################### PROGRAM UTAMA DARI BOT  #########################
def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    
    map_size = state['MapDimension']
    opponent_map = state['OpponentMap']['Cells']
    opponent_ships = state['OpponentMap']['Ships']
    ourShips = state['PlayerMap']['Owner']['Ships']
    energy = state['PlayerMap']['Owner']["Energy"]

    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(opponent_map,opponent_ships,ourShips,energy)

def output_shot(move,x,y):
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def fire_shot(opponent_map,opponent_ships,ourShips,energy):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)

    board = [[0 for j in range(map_size)] for i in range(map_size)]
    
    if huntingMode(opponent_map,opponent_ships):
        board = calculate_probability(board,"hunting",opponent_map,opponent_ships)
        move = chooseWeapon(ourShips,energy,"hunting")
    else: # in destroy mode
        board = calculate_probability(board,"destroy",opponent_map,opponent_ships)                
        move = chooseWeapon(ourShips,energy,"destroy")

    target = get_target(board,opponent_map)
    take_config = best_config(board,move,target)
    output_shot(take_config[0],take_config[1][0],take_config[1][1])
    return

def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    ships = ['Battleship 0 0 north',
             'Carrier 5 0 East',
             'Cruiser 6 4 north',
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
