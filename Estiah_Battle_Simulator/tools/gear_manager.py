from battle.gear import Gear
from common.datahandler import *

if __name__ == '__main__':
	
	def testAddGear():
		gears = loadGears()
		def addGear(gear):
			if gear.id not in gears:
				gears[gear.id] = gear.toJsonObj()
			return
		addGear(Gear('Hamster Gear', [(loadCharmFromId('287'), 7)], False))
		addGear(Gear('Mouse Gear', [(loadCharmFromId('287'), 2), (loadCharmFromId('288'), 3)], False))
		saveGears(gears)


	testAddGear()
