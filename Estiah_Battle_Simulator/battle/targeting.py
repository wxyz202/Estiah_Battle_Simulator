def chooseRandomEnimy(enimies):
	target = None
	for player in enimies:
		if player.is_being_target_turn > 0:
			target = player
			break
	if target is None:
		target = random.choice([e for e in enimies if e.isAlive()])
	return target

def chooseLowestHpEnimy(enimies):
	target = None
	for player in enimies:
		if player.isAlive():
			if target is None or player.hp < target.hp:
				target = player
	return player