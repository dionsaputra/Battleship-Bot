
def searchShipRemaining():
	for i in range(0, 100):
		if (state["PlayerMap"]["Cells"][i]["Occupied"] and not state["PlayerMap"]["Cells"][i]["Hit"]):
			return (int(i/10), i%10)

def output_shot(x, y, weapon):
    if (state["PlayerMap"]["Owner"]["ShipsRemaining"] == 1 and not state["PlayerMap"]["Owner"]["Shield"]["Active"]):
    	x, y = searchShipRemaining()
        move = 8
    elif:
        move = weapon  # 1=fire shot command code

    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass
