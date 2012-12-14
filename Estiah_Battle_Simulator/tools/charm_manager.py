import json
from common.alltype import TargetType, RuneType, LineType, EffectType
from battle.charms import Charm, RandomEffectLine
from battle.conditions import Condition
from battle.effect import Melee

def loadCharms():
	f = open('data/charms.json')
	charms = json.load(f)
	f.close()
	return charms

def saveCharms(charms):
	f = open('data/charms.json', 'w')
	json.dump(charms, f, indent=4, sort_keys=True)
	f.close()
	return

if __name__ == '__main__':
	def testAddCharm():
		charms = loadCharms()
		charm = Charm(id = '102', name = 'Wooden Sword', rune_type1 = RuneType.Sword, rune_type2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Melee(5, 20), TargetType.Enimy)])])
		if charm.id not in charms:
			charms[charm.id] = charm.toJsonObj()
		saveCharms(charms)

	testAddCharm()

	"""
	charm = Charm(id = '102', name = 'Wooden Sword', rune_type1 = RuneType.Sword, rune_type2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Melee(5, 20), TargetType.Enimy)])])
	x=charm.toJsonObj()
	y=Charm.fromJsonObj(x)
	z=y.toJsonObj()
	print x==z
	"""