import json

class DataHandler(object):
	_charms = None
	_gears = None
	_players = None

	@classmethod
	def load_charms(cls):
		if cls._charms is None:
			f = open('data/charms.json')
			cls._charms = json.load(f)
			f.close()
		return cls._charms

	@classmethod
	def save_charms(cls, charms):
		cls._charms = charms
		f = open('data/charms.json', 'w')
		json.dump(charms, f, indent=4, sort_keys=True)
		f.close()
		return

	@classmethod
	def load_charm_from_id(cls, charm_id):
		charms = cls.load_charms()
		from battle.charm import Charm
		return Charm.from_json_obj(charms[charm_id])

	@classmethod
	def load_gears(cls):
		if cls._gears is None:
			f = open('data/gears.json')
			cls._gears = json.load(f)
			f.close()
		return cls._gears

	@classmethod
	def save_gears(cls, gears):
		cls._gears = gear
		f = open('data/gears.json', 'w')
		json.dump(gears, f, indent=4, sort_keys=True)
		f.close()
		return

	@classmethod
	def load_gear_from_id(cls, gear_id):
		gears = cls.load_gears()
		from battle.gear import Gear
		return Gear.from_json_obj(gears[gear_id])

	@classmethod
	def load_players(cls):
		if cls._players is None:
			f = open('data/players.json')
			cls._players = json.load(f)
			f.close()
		return cls._players

	@classmethod
	def save_players(cls, players):
		cls._players = players
		f = open('data/players.json', 'w')
		json.dump(players, f, indent=4, sort_keys=True)
		f.close()
		return

	@classmethod
	def load_player_from_id(cls, player_id):
		players = cls.load_players()
		from battle.player import Player
		return Player.from_json_obj(players[player_id])
