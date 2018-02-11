import random

map_size = 14

def createConfShips(size):
    # meng-generate posisi kapal berdasarkan list yang tersedia
    confLarge = [["6 4 East", "12 6 north", "5 8 north", "3 2 East", "0 13 East"],["1 2 East","4 7 East", "0 10 East", "12 10 north", "10 2 north"],["11 8 north", "4 5 East", "1 10 north", "8 6 East", "5 0 East"],["12 8 north", "9 4 north", "5 1 East", "0 1 north", "1 7 East"], ["5 12 east", "12 0 north", "3 7 north", "1 1 East", "9 8 north"]]
    confMed = [[],[],[],[],[]]
    confSmall = [[],[],[],[],[]]
    useConf = []
    retConf = []
    if (size == 7):
        useConf = random.choice(confSmall)
    elif (size == 10):
        useConf = random.choice(confMed)
    elif (size == 14):
        useConf = random.choice(confLarge)

    retConf.append("Battleship "+ useConf[0])
    retConf.append("Carrier "+ useConf[1])
    retConf.append("Cruiser "+ useConf[2])
    retConf.append("Destroyer "+ useConf[3])
    retConf.append("Submarine "+ useConf[4])

    return retConf

def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    ships = createConfShips(map_size)

    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


print (createConfShips(14))
