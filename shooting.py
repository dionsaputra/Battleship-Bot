# variable global
ourShips = []
Energy = 0

# tambahin ke main
def main():
    global ourShips, energy

    ourShips = state['PlayerMap']['Owner']['Ships']
    energy = int(state['PlayerMap']['Owner']["Energy"])
    print("Chosen weapon : ",chooseWeapon(100))

# membuat list objek weapon
def weaponAvailable():
	weapon = []
	data = ourShips[0]['Weapons'][0]
	data["Destroyed"] = False
	weapon.append(data)

	for ships in ourShips:
		data = ships['Weapons'][1]
		data["Destroyed"] = ships["Destroyed"]
		weapon.append(data)

	return weapon

# memilih senjata
def chooseWeapon(energy, x, y):
	weapon = weaponAvailable()
	print (weapon)
	for i in range(len(weapon)-1, -1, -1):
		print(i)
		if (weapon[i]["Destroyed"] == False):
			if (energy >= weapon[i]["EnergyRequired"]):
				if (weapon[i]["WeaponType"] == "SingleShot":
					return 1
				elif (weapon[i]["WeaponType"] == "DoubleShot"):
					if (spaceAvailable("DoubleShotHorizontal", x, y):
						return 2
					elif (spaceAvailable("DoubleShotVertical", x, y)):
						return 3
				elif (weapon[i]["WeaponType"] == "CornerShot" and spaceAvailable("CornerShot", x)):
					return 4
				elif (weapon[i]["WeaponType"] == "DiagonalCrossShot" and spaceAvailable("DiagonalCrossShot", x, y)):
					return 5
				elif (weapon[i]["WeaponType"] == "CrossShot" and spaceAvailable("CrossShot", x, y)):
					return 6
				elif (weapon[i]["WeaponType"] == "SeekerMissile"):
					return 7
	return 0

def spaceAvailable(shootMethod, x, y):
	cell = state['OpponentMap']['Cells']
	indeks =x*10 + y
	# tengah diasumsikan sudah benar dan bisa ditembah
	# tengah = cell[indeks]["Missed"] or cell[indeks]["Damaged"]

	if (shootMethod == "DoubleShotHorizontal"):
		# tidak di unjung kiri dan kanan
		if (y > 0 and y < 9):
			kanan = cell[indeks+1]["Missed"] or cell[indeks+1]["Damaged"]
			kiri = cell[indeks-1]["Missed"] or cell[indeks-1]["Damaged"]
			return (not kanan and not kiri)

	elif (shootMethod == "DoubleShotVertical"):
		# tidak di paling atas dan paling bawah
		if (x > 0 and x < 9):
			bawah = cell[indeks-10]["Missed"] or cell[indeks-10]["Damaged"]
			atas = cell[indeks+10]["Missed"] or cell[indeks+10]["Damaged"]
			return (not bawah and not atas)

	elif (shootMethod == "CornerShot"):
		if (y > 0 and y < 9 and x > 0 and x < 9):
			paKanan = cell[indeks-9]["Missed"] or cell[indeks-9]["Damaged"]
			paKiri = cell[indeks-11]["Missed"] or cell[indeks-11]["Damaged"]
			pbKanan = cell[indeks+11]["Missed"] or cell[indeks+11]["Damaged"]
			pbKiri = cell[indeks+9]["Missed"] or cell[indeks+9]["Damaged"]
			return (not paKanan and not paKiri and not pbKanan and not pbKiri)

	elif (shootMethod == "DiagonalCrossShot"):
		if (y > 0 and y < 9 and x > 0 and x < 9):
			paKanan = cell[indeks-9]["Missed"] or cell[indeks-9]["Damaged"]
			paKiri = cell[indeks-11]["Missed"] or cell[indeks-11]["Damaged"]
			pbKanan = cell[indeks+11]["Missed"] or cell[indeks+11]["Damaged"]
			pbKiri = cell[indeks+9]["Missed"] or cell[indeks+9]["Damaged"]
			return (not paKanan and not paKiri and not pbKanan and not pbKiri)

	elif (shootMethod == "CrossShot"):
		if (y > 0 and y < 9 and x > 0 and x < 9):
			bawah = cell[indeks-10]["Missed"] or cell[indeks-10]["Damaged"]
			atas = cell[indeks+10]["Missed"] or cell[indeks+10]["Damaged"]
			kanan = cell[indeks+1]["Missed"] or cell[indeks+1]["Damaged"]
			kiri = cell[indeks-1]["Missed"] or cell[indeks-1]["Damaged"]
			return (not kiri and not atas and not bawah and not kanan and not tengah)

	return False

# tambahin ke output_shot
def output_shot(x, y):
    move = chooseWeapon(Energy, x, y)  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass
