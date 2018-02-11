# variable global
ourShips = []
Energy = 0

output_path = '.'

# tambahin ke main
def main():
    global ourShips, energy
    with open(os.path.join(output_path, 'state.json'), 'r') as f_in:
        state = json.load(f_in)
    
    ourShips = state['PlayerMap']['Owner']['Ships']
    energy = state['PlayerMap']['Owner']["Energy"]
    

# membuat list objek weapon
def weaponAvailable():
	weapon = []
	data = ourShips[0]['Weapons'][0]
	data["Destroyed"] = ourShips[0]["Destroyed"]
	weapon.append(data)

	for ships in ourShips:
		data = ships['Weapons'][1]
		data["Destroyed"] = ships["Destroyed"]
		weapon.append(data)

	return weapon

# memilih senjata
def chooseWeapon(energy):
	weapon = weaponAvailable()
	print (weapon)
	for i in range(len(weapon)-1, -1, -1):
		print(i)
		if (weapon[i]["Destroyed"] == False):
			if (energy >= weapon[i]["EnergyRequired"]):
				if (weapon[i]["WeaponType"] == "SingleShot"):
					return 1
				elif (weapon[i]["WeaponType"] == "DoubleShot"):
					return 2
				elif (weapon[i]["WeaponType"] == "CornerShot"):
					return 3
				elif (weapon[i]["WeaponType"] == "DiagonalCrossShot"):
					return 4
				elif (weapon[i]["WeaponType"] == "CrossShot"):
					return 5
				elif (weapon[i]["WeaponType"] == "SeekerMissile"):
					return 6
	return 0

# tambahin ke output_shot
def output_shot(x, y):
    move = chooseWeapon(Energy)  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

if __name__ == '__main__':
	print("Chosen weapon : ",chooseWeapon(100))