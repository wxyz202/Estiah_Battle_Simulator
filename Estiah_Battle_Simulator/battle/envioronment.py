import random
from common.alltype import PlayerType
import targeting

class Envioronment(object):
	def __init__(self, attacker, defender, first_turn_party=PlayerType.Attacker, first_turn_player=0):
		self.attacker = attacker
		self.defender = defender
		if first_turn_party == PlayerType.Random:
			self.turn_party = random.choice([PlayerType.Attacker, PlayerType.Defender])
		else:
			self.turn_party = first_turn_party
		if first_turn_player == PlayerType.Random:
			if self.turn_party == PlayerType.Attacker:
				self.turn_player = random.randint(len(attacker))
			else:
				self.turn_player = random.randint(len(defender))
		else:
			self.turn_player = first_turn_player
		self.turn = 0

	def lose(self):
		count = 0
		for p in self.attacker:
			if p.isAlive():
				count += 1
		return count == 0

	def win(self):
		count = 0
		for p in self.defender:
			if p.isAlive():
				count += 1
		return count == 0

	def end(self):
		return lose() or win()

	def nextPlayer(self):
		while True:
			self.turn_player += 1
			if self.turn_party == PlayerType.Attacker:
				if self.turn_player >= len(self.attacker):
					self.turn_party = PlayerType.Defender
					self.turn_player = 0
			else:
				if self.turn_player >= len(self.defender):
					self.turn_party = PlayerType.Attacker
					self.turn_player = 0
			if self.turn_party == PlayerType.Attacker:
				if self.attacker[self.turn_player].isAlive():
					break
			else:
				if self.defender[self.turn_player].isAlive():
					break
		return

	def playTurn(self):
		self.turn += 1
		if self.turn_party == PlayerType.Attacker:
			player = self.attacker[self.turn_player]
			allies = self.attacker
			enimies = self.defender
		else:
			player = self.defender[self.turn_player]
			allies = self.defender
			enimies = self.attacker
		charm_in_turn = 0
		has_action = True
		while charm_in_turn < player.max_dizzy_turn and has_action:
			enimy = targeting.chooseRandomEnimy(enimies)
			self.focusTurnDecrease(enimy)
			is_EA = player.playCharm(allies, enimy, enimies, self.turn)
			self.focusTurnCheck()
			has_action = False
			charm_in_turn += 1
			if self.end():
				break
			player.triggerEffects(allies, enimies, is_EA)
			self.focusTurnCheck()
			if self.end():
				break
			if is_EA:
				has_action = True
		return

	def focusTurnDecrease(self, player):
		player.is_being_target_turn -= 1

	def focusTurnCheck(self):
		players = [p for p in self.attacker if p.isAlive()]
		if len(players) == 1:
			players[0].is_being_target_turn = 0
		players = [p for p in self.defender if p.isAlive()]
		if len(players) == 1:
			players[0].is_being_target_turn = 0
		return