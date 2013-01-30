from battle.gear import Gear
from common.datahandler import *

if __name__ == '__main__':
	
	def test_add_gear(gear):
		gears = load_gears()
		if gear.id not in gears:
			gears[gear.id] = gear.to_json_obj()
		save_gears(gears)


	gear1 = Gear.from_string("zgreee - auto magic#5x668 3x610 5x968 5x973 5x1057 5x1077 5x1108 5x1221 5x1496")
	gear2 = Gear.from_string("zgreee3 - auto#5x668 5x940 5x1074 5x1221 5x344 5x947 5x1078 5x942")

	test_add_gear(gear1)
	test_add_gear(gear2)
