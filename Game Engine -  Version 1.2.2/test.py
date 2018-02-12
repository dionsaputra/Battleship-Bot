with open('last_shot.txt', 'r') as f_in:
    cell = f_in.read()
    cell = cell.split(',')
    print(cell)
    y = [int(cell[0]),int(cell[1])]
    print(y[0]+1,y[1]+1)
    print()
pass
