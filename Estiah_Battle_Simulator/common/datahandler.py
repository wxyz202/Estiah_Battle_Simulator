import json

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

def loadCharmFromId(charm_id):
	charms = loadCharms()
	from battle.charm import Charm
	return Charm.fromJsonObj(charms[charm_id])


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

def loadGearFromId(gear_id):
	gears = loadGears()
	from battle.gear import Gear
	return Gear.fromJsonObj(gears[gear_id])


def loadPlayers():
	f = open('data/players.json')
	players = json.load(f)
	f.close()
	return players

def savePlayers(players):
	f = open('data/players.json', 'w')
	json.dump(players, f, indent=4, sort_keys=True)
	f.close()
	return

def loadPlayerFromId(player_id):
	players = loadPlyers()
	from battle.player import Player
	return Plyaer.fromJsonObj(players[player_id])
