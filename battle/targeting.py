import random

def choose_enimy(enimies):
	target = None
	for player in enimies:
		if player.being_target():
			target = player
			break
	if target is None:
		target = random.choice([player for player in enimies if player.is_alive()])
	return target

def choose_lowest_hp(players):
	target = None
	for player in players:
		if player.is_alive():
			if target is None or player.get_hp() < target.get_hp():
				target = player
	return player
