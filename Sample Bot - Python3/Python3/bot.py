import argparse
import json
import os
from random import choice

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0
state = {}

def main(player_key):
    global map_size
    global state
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(state['OpponentMap']['Cells'])


def output_shot(x, y):
    move = 1  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def fill_prob(ship,pos,start,end,hor):
    if end-start+1 >= ship['Length']:
        for i in range(start,end-ship['Length']+2):
            for j in range(ship['Length']):
                if hor == 1 and board[pos][i+j] >= 0:
                    board[pos][i+j] += 1
                elif hor == 0 and board[i+j][pos] >= 0:
                    board[i+j][pos] += 1

def calc_prob(board,size,ships):
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

def get_target(board,size):
    maxRow = 0
    maxCol = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] > board[maxRow][maxCol]:
                maxRow = i
                maxCol = j

    return [maxRow,maxCol]

def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)
    targets = []

    # inisialisasi board value dengan 0
    board = [[0 for j in range(map_size)] for i in range(map_size)]

    # inisialisasi board value dengan state opponent map saat ini
    for cell in opponent_map:
        if not cell['Damaged'] and not cell['Missed']:
            board[cell['X']][cell['Y']] = 0
        else:
            board[cell['X']][cell['Y']] = -1

    opponent_ships = state['OpponentMap']['Ships']
    for ship in opponent_ships:
        if ship['ShipType'] == "Submarine":
            ship['Length'] = 3
        elif ship['ShipType'] == "Battleship":
            ship['Length'] = 4
        elif ship['ShipType'] == "Destroyer":
            ship['Length'] = 2
        elif ship['ShipType'] == "Cruiser":
            ship['Length'] = 5
        elif ship['ShipType'] == "Carrier":
            ship['Length'] = 3

    calc_prob(board,map_size,oppenent_ships)

    target = get_target(board,map_size)
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
