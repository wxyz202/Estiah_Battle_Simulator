import random
from common.enumtype import PlayerType, EnvioronmentType
import battlelog

class Envioronment(object):
	def __init__(self, attackers, defenders, begin_party=PlayerType.Attacker, begin_player_index=0):
		name_dict = {}
		for player in attackers + defenders:
			if player.name not in name_dict:
				name_dict[player.name] = 1
			else:
				name_dict[player.name] += 1
				player.name = player.name + ' ' + chr(ord('A') + name_dict[player.name] - 1)
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

	def log_state(self):
		battlelog.log("** Battle status **\n")
		for player in self.attackers:
			player.log_state()
		battlelog.log("------\n")
		for player in self.defenders:
			player.log_state()
		battlelog.log("\n")

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

	def check_players_state(self):
		for player in self.attackers + self.defenders:
			if player.is_alive():
				player.check_dead()
			if player.is_alive():
				player.check_out_of_spirit()

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
			self.focus_turn_decrease(enimies)
			self.check_players_state()
			if self.end() or not player.is_alive():
				battlelog.log("\n")
				break
			if player.has_extra_action():
				player.trigger_effects_extra_action(allies, enimies)
			else:
				player.trigger_effects_normal(allies, enimies)
			self.check_players_state()
			if self.end() or not player.is_alive():
				battlelog.log("\n")
				break
			player.reduce_spirit(1)
			self.check_players_state()
			if self.end() or not player.is_alive():
				battlelog.log("\n")
				break
			battlelog.log("\n")
		player.turn_end()
		self.log_state()
		return

	def start(self):
		self.log_state()
		self.play_turn()
		while not self.end():
			self.next_player()
			self.play_turn()
		if self.lose():
			return EnvioronmentType.Lose
		else:
			return EnvioronmentType.Win

	def focus_turn_decrease(self, party):
		for player in party:
			if player.being_target():
				player.being_target_turn_decrease()

