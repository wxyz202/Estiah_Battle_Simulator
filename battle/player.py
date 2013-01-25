import random
import sys
from common.enumtype import PlayerType

class Player(object):
	def __init__(self, id, name, level, max_hp, is_no_dizzy=False):
		self.id = id
		self.name = name
		self.level = level
		self.max_hp = max_hp
		self.hp = self.max_hp
		self.charm_used_each_turn = {}
		self.charm_thrown_each_turn = {}
		self.is_no_dizzy = is_no_dizzy
		if is_no_dizzy:
			self.max_dizzy_turn = sys.maxint
		else:
			self.max_dizzy_turn = 4
		self.alive_state = PlayerType.Alive
		self.reset()

	def reset(self):
		self.melee_CPB = 0
		self.melee_NPB = 0
		self.magic_CPB = 0
		self.magic_NPB = 0
		self.spirit_CPB = 0
		self.spirit_NPB = 0
		self.armor = 0
		self.ward = 0
		self.willpower = 0
		self.long_time_effect_list = []
		self.being_target_turn = 0
		self.stun_turn = 0
		self.extra_actions = 0

	def import_gear(gear):
		self.charm_list, self.max_spirit = gear.generate_charm_list()
		self.spirit = self.max_spirit

	def cleanse(self):
		self.long_time_effect_list = [effect for effect in self.long_time_effect_list if not isinstance(effect, Bane)]
		self.melee_CPB = max(0, self.melee_CPB)
		self.melee_NPB = max(0, self.melee_NPB)
		self.magic_CPB = max(0, self.magic_CPB)
		self.magic_NPB = max(0, self.magic_NPB)
		self.spirit_CPB = max(0, self.spirit_CPB)
		self.spirit_NPB = max(0, self.spirit_NPB)
		return

	def purge(self):
		self.long_time_effect_list = [effect for effect in self.long_time_effect_list if not isinstance(effect, Aura)]
		self.melee_CPB = min(0, self.melee_CPB)
		self.melee_NPB = min(0, self.melee_NPB)
		self.magic_CPB = min(0, self.magic_CPB)
		self.magic_NPB = min(0, self.magic_NPB)
		self.spirit_CPB = min(0, self.spirit_CPB)
		self.spirit_NPB = min(0, self.spirit_NPB)
		return

	def normalize(self):
		self.melee_CPB = 0
		self.melee_NPB = 0
		self.magic_CPB = 0
		self.magic_NPB = 0
		self.spirit_CPB = 0
		self.spirit_NPB = 0
		return

	def die(self):
		self.alive_state = PlayerType.Dead
		self.reset()

	def out_of_spirit(self):
		self.alive_state = PlayerType.Out_of_Spirit
		self.reset()

	def check_out_of_spirit(self):
		if self.spirit <= 0:
			self.out_of_spirit()

	def turn_begin(self):
		self.actions = 0
		self._use_melee_NPB = False
		self._use_magic_NPB = False
		self._use_spirit_NPB = False

	def turn_end(self):
		self.extra_actions = 0

	def is_alive(self):
		return self.alive_state == PlayerType.Alive

	def is_stun(self):
		return self.stun_turn > 0

	def gain_stun(self, turn):
		self.stun_turn = max(self.stun_turn, turn)

	def being_target(self):
		return self.being_target_turn > 0

	def gain_being_target(self, turn, is_cumul):
		if is_cumul:
			self.being_target_turn += turn
		else:
			self.being_target_turn = max(self.being_target_turn, turn)

	def clear_being_target(self):
		self.being_target_turn = 0

	def has_action(self):
		return (self.actions < self.extra_actions + 1) and (self.actions < self.max_dizzy_turn)

	def has_extra_action(self):
		return self.actions < self.extra_actions + 1

	def gain_extra_action(self, turn):
		self.extra_actions += turn

	def get_armor(self):
		return self.armor

	def set_armor(self, armor):
		self.armor = armor

	def get_ward(self):
		return self.ward

	def set_ward(self, ward):
		self.ward = ward

	def get_willpower(self):
		return self.willpower

	def set_willpower(self, willpower):
		self.willpower = willpower

	def get_melee_NPB(self):
		return self.melee_NPB

	def get_magic_NPB(self):
		return self.magic_NPB

	def get_spirit_NPB(self):
		return self.spirit_NPB

	def get_melee_CPB(self):
		return self.melee_CPB

	def get_magic_CPB(self):
		return self.magic_CPB

	def get_spirit_CPB(self):
		return self.spirit_CPB

	def gain_melee_NPB(self, boost):
		self.melee_NPB += boost

	def gain_magic_NPB(self, boost):
		self.magic_NPB += boost

	def gain_spirit_NPB(self, boost):
		self.spirit_NPB += boost

	def gain_melee_CPB(self, boost):
		self.melee_CPB += boost

	def gain_magic_CPB(self, boost):
		self.magic_CPB += boost

	def gain_spirit_CPB(self, boost):
		self.spirit_CPB += boost

	def use_melee_NPB(self):
		self._use_melee_NPB = True

	def use_magic_NPB(self):
		self._use_magic_NPB = True

	def use_spirit_NPB(self):
		self._use_spirit_NPB = True

	def check_melee_NPB(self):
		if self._use_melee_NPB:
			self._use_melee_NPB = False
			self.melee_NPB = 0

	def check_magic_NPB(self):
		if self._use_magic_NPB:
			self._use_magic_NPB = False
			self.magic_NPB = 0

	def check_spirit_NPB(self):
		if self._use_spirit_NPB:
			self._use_spirit_NPB = False
			self.spirit_NPB = 0

	def take_melee_damage(self, melee):
		self.reduce_hp(melee)

	def take_magic_damage(self, magic):
		self.reduce_hp(magic)

	def take_spirit_damage(self, spirit):
		self.reduce_spirit(spirit)
		while spirit > 0:
			spirit -= 1
			self.charm_thrown_each_turn.append(self.charm_list.next())

	def duel_melee_damage(self, melee):
		pass #TODO: use to make statistics

	def duel_magic_damage(self, melee):
		pass #TODO: use to make statistics

	def duel_spirit_damage(self, melee):
		pass #TODO: use to make statistics

	def get_hp(self):
		return self.hp

	def reduce_hp(self, hp):
		if self.hp > hp:
			self.hp -= hp
		else:
			self.hp = 0
			self.die()

	def increase_hp(self, hp):
		self.hp = max(self.hp+hp, self.max_hp)

	def reduce_spirit(self, spirit):
		if self.spirit > spirit:
			self.spirit -= spirit
		else:
			self.spirit = 0
		self.check_out_of_spirit()

	def play_stun(self, turn_num):
		self.stun_turn -= 1
		if turn_num not in self.charm_used_each_turn:
			self.charm_used_each_turn[turn_num] = []

	def attach(self, long_time_effect):
		self.long_time_effect_list.append(long_time_effect)

	def play_charm(self, allies, enimies, turn_num):
		self.actions += 1
		charm = self.charm_list.next()
		if turn_num not in self.charm_used_each_turn:
			self.charm_used_each_turn[turn_num] = []
		self.charm_used_each_turn[turn_num].append(charm)
		charm.execute(self, allies, enimies)

	def trigger_effects_normal(self, allies, enimies):
		for effect in self.long_time_effect_list:
			effect.trigger_normal(self, allies, enimies)
			if effect.end():
				self.long_time_effect_list.remove(effect)

	def trigger_effects_stun(self, allies, enimies):
		for effect in self.long_time_effect_list:
			effect.trigger_stun(self, allies, enimies)
			if effect.end():
				self.long_time_effect_list.remove(effect)

	def trigger_effects_extra_action(self, allies, enimies):
		for effect in self.long_time_effect_list:
			effect.trigger_extra_action(self, allies, enimies)
			if effect.end():
				self.long_time_effect_list.remove(effect)

	def to_json_obj(self):
		obj = {
			'id': self.id,
			'name': self.name,
			'level': self.level,
			'max_hp': self.max_hp,
			'is_no_dizzy': self.is_no_dizzy
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		id = obj['id']
		name = obj['name']
		level = obj['level']
		max_hp = obj['max_hp']
		is_no_dizzy = obj['is_no_dizzy']
		return cls(id, name, level, max_hp, is_no_dizzy)
