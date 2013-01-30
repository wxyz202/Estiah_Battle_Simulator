import random
from common.enumtype import PlayerType, EnvioronmentType

class Envioronment(object):
	def __init__(self, attackers, defenders, begin_party=PlayerType.Attacker, begin_player_index=0):
		if begin_party == PlayerType.Random:
			begin_party = random.choice([PlayerType.Attacker, PlayerType.Defender])
			if begin_party == PlayerType.Attacker:
				begin_player_index = random.randint(len(attackers))
			else:
				begin_player_index = random.randint(len(defenders))
		self.attackers = attackers
		self.defenders = defenders
		if begin_party == PlayerType.Attacker:
			self.action_party = self.attackers
		else:
			self.action_party = self.defenders
		self.action_player = self.action_party[begin_player_index]
		self.turn_num = 0

	def win(self):
		count = 0
		for player in self.defenders:
			if player.is_alive():
				count += 1
		return count == 0

	def lose(self):
		count = 0
		for player in self.attackers:
			if player.is_alive():
				count += 1
		return count == 0

	def end(self):
		return self.lose() or self.win()

	def opposite_party(self, party):
		if self.attackers == party:
			return self.defenders
		else:
			return self.attackers

	def next_player(self):
		while True:
			if self.action_player == self.action_party[-1]:
				self.action_party = self.opposite_party(self.action_party)
				self.action_player = self.action_party[0]
			else:
				action_player_index = self.action_party.index(self.action_player)
				self.action_player = self.action_party[action_player_index + 1]
			if self.action_player.is_alive():
				break
		return self.action_player

	def play_turn(self):
		self.turn_num += 1
		player = self.action_player
		allies = self.action_party
		enimies = self.opposite_party(allies)
		if player.is_stun():
			player.play_stun(self.turn_num)
			self.focus_turn_decrease(enimies)
			player.trigger_effects_stun(allies, enimies)
			return
		player.turn_begin()
		while player.has_action():
			player.play_charm(allies, enimies, self.turn_num)
			self.focus_turn_decrease(enimy)
			if self.end() or not player.is_alive():
				break
			if player.has_extra_action():
				player.trigger_effects_extra_action(allies, enimies)
			else:
				player.trigger_effects_normal(allies, enimies)
			if self.end() or not player.is_alive():
				break
			player.reduce_spirit(1)
			if self.end() or not player.is_alive():
				break
		player.turn_end()
		return

	def start(self):
		while not self.end():
			self.play_turn()
			self.next_player()
		if self.lose():
			return EnvioronmentType.Lose
		else:
			return EnvioronmentType.Win

	def focus_turn_decrease(self, party):
		for player in party:
			if player.being_target():
				player.being_target_turn_decrease()

