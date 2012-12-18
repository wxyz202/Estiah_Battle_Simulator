import json
from common.alltype import TargetType, RuneType, LineType, EffectType
from battle.charms import Charm, RandomEffectLine
from battle.conditions import Condition
from battle.effect import *

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


def loadCharm(charm_id):
	charms = loadCharms()
	return Charm.fromJsonObj(charms[charm_id])


if __name__ == '__main__':

	def testAddCharm():
		charms = loadCharms()
		def addCharm(charm):
			if charm.id not in charms:
				charms[charm.id] = charm.toJsonObj()
			return

		addCharm(Charm(id = '102', name = 'Wooden Sword', rune1 = RuneType.Sword, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Melee(5, 20), TargetType.Enimy)])]))
		addCharm(Charm(id = '103', name = 'Small Ice Wand', rune1 = RuneType.Frost, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Magic(4, 25), TargetType.Enimy)])]))
		addCharm(Charm(id = '104', name = 'Worn Leather Chest', rune1 = RuneType.Armor, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Armor(8, False), TargetType.Self)])]))
		addCharm(Charm(id = '287', name = 'Squeek!', rune1 = RuneType.Tech, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([])]))
		addCharm(Charm(id = '288', name = 'Look Around', rune1 = RuneType.Tech, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([])]))
		addCharm(Charm(id = '289', name = 'Finger Bite', rune1 = RuneType.Tech, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Melee(2, 0), TargetType.Enimy)])]))
		addCharm(Charm(id = '290', name = 'Tiny Claws', rune1 = RuneType.Tech, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Melee(3, 0), TargetType.Enimy)])]))
		addCharm(Charm(id = '291', name = 'Harden Fur', rune1 = RuneType.Armor, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Armor(4, False), TargetType.Self)])]))
		addCharm(Charm(id = '292', name = 'Rat Slash', rune1 = RuneType.Tech, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Melee(4, 0), TargetType.Enimy)])]))
		addCharm(Charm(id = '293', name = 'Evil Look', rune1 = RuneType.Tech, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([])]))
		addCharm(Charm(id = '294', name = 'Eat Dirt', rune1 = RuneType.Tech, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([])]))
		saveCharms(charms)



	testAddCharm()

	"""
	charm = Charm(id = '102', name = 'Wooden Sword', rune1 = RuneType.Sword, rune2 = RuneType.Null, is_attachment = False, lines = [RandomEffectLine([(Melee(5, 20), TargetType.Enimy)])])
	x=charm.toJsonObj()
	y=Charm.fromJsonObj(x)
	z=y.toJsonObj()
	print x==z
	"""


	
