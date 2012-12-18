import json
from battle.gear import Gear
from tools.charm_manager import loadCharm

def loadGears():
	f = open('data/gears.json')
	gears = json.load(f)
	f.close()
	return gears

def saveGears(gears):
	f = open('data/gears.json', 'w')
	json.dump(gears, f, indent=4, sort_keys=True)
	f.close()
	return

def loadGears(gear_id):
	gears = loadGears()
	return Gear.fromJsonObj(gears[gear_id])

if __name__ == '__main__':
	
	def testAddGear():
		gears = loadGears()
		def addGear(gear):
			if gear.id not in gears:
				gears[gear.id] = gear.toJsonObj()
			return
		addGear(Gear('Hamster Gear', [(loadCharm('287'), 7)], False))
		addGear(Gear('Mouse Gear', [(loadCharm('287'), 2), (loadCharm('288'), 3)], False))
		saveGears(gears)


	testAddGear()
