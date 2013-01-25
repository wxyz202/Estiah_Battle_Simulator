import json

def load_charms():
	f = open('data/charms.json')
	charms = json.load(f)
	f.close()
	return charms

def save_charms(charms):
	f = open('data/charms.json', 'w')
	json.dump(charms, f, indent=4, sort_keys=True)
	f.close()
	return

def load_charm_from_id(charm_id):
	charms = load_charms()
	from battle.charm import Charm
	return Charm.from_json_obj(charms[charm_id])


def load_gears():
	f = open('data/gears.json')
	gears = json.load(f)
	f.close()
	return gears

def save_gears(gears):
	f = open('data/gears.json', 'w')
	json.dump(gears, f, indent=4, sort_keys=True)
	f.close()
	return

def load_gear_from_id(gear_id):
	gears = loadGears()
	from battle.gear import Gear
	return Gear.from_json_obj(gears[gear_id])


def load_players():
	f = open('data/players.json')
	players = json.load(f)
	f.close()
	return players

def save_players(players):
	f = open('data/players.json', 'w')
	json.dump(players, f, indent=4, sort_keys=True)
	f.close()
	return

def load_player_from_id(player_id):
	players = loadPlyers()
	from battle.player import Player
	return Plyaer.from_json_obj(players[player_id])
