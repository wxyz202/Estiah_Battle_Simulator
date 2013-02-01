import random
import sys
from common.enumtype import PlayerType
import battlelog

class Player(object):
	def __init__(self, id, name, level, max_hp, is_no_dizzy=False):
		self.id = id
		self.name = name
		self.level = level
		self.max_hp = max_hp
		self.hp = self.max_hp
		self.charm_used_each_turn = {}
		self.charm_thrown_each_turn = []
		self.is_no_dizzy = is_no_dizzy
		if is_no_dizzy:
			self.max_dizzy_turn = sys.maxint
		else:
			self.max_dizzy_turn = 4
		self.alive_state = PlayerType.Alive
		self.reset()

	def log_state(self):
		battlelog.log("%s : %d/%d HP, %d armor, %d ward, %d willpower, %d/%d Charm(s) left, Melee CPB/Next: %d/%d, Magic CPB/Next: %d/%d, Spirit CPB/Next: %d/%d\n" %(self.name, self.hp, self.max_hp, self.armor, self.ward, self.willpower, self.spirit, self.max_spirit, self.melee_CPB, self.melee_NPB, self.magic_CPB, self.magic_NPB, self.spirit_CPB, self.spirit_NPB))

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

	def import_gear(self, gear):
		self.charm_list, self.max_spirit = gear.generate_charm_list()
		self.spirit = self.max_spirit

	def cleanse(self):
		battlelog.log("%s is cleansed\n" %(self.name))
		from effect import Bane
		for long_time_effect in self.long_time_effect_list[:]:
			if isinstance(long_time_effect, Bane):
				battlelog.log("%s disappears\n" %(long_time_effect.attach_charm.name))
				self.long_time_effect_list.remove(long_time_effect)
		self.melee_CPB = max(0, self.melee_CPB)
		self.melee_NPB = max(0, self.melee_NPB)
		self.magic_CPB = max(0, self.magic_CPB)
		self.magic_NPB = max(0, self.magic_NPB)
		self.spirit_CPB = max(0, self.spirit_CPB)
		self.spirit_NPB = max(0, self.spirit_NPB)
		return

	def purge(self):
		battlelog.log("%s is purged\n" %(self.name))
		from effect import Aura
		for long_time_effect in self.long_time_effect_list[:]:
			if isinstance(long_time_effect, Aura):
				battlelog.log("%s disappears\n" %(long_time_effect.attach_charm.name))
				self.long_time_effect_list.remove(long_time_effect)
		self.melee_CPB = min(0, self.melee_CPB)
		self.melee_NPB = min(0, self.melee_NPB)
		self.magic_CPB = min(0, self.magic_CPB)
		self.magic_NPB = min(0, self.magic_NPB)
		self.spirit_CPB = min(0, self.spirit_CPB)
		self.spirit_NPB = min(0, self.spirit_NPB)
		return

	def normalize(self):
		battlelog.log("%s is normalized\n" %(self.name))
		self.melee_CPB = 0
		self.melee_NPB = 0
		self.magic_CPB = 0
		self.magic_NPB = 0
		self.spirit_CPB = 0
		self.spirit_NPB = 0
		return

	def die(self):
		battlelog.log("\n%s is defeated.\n" %(self.name))
		self.alive_state = PlayerType.Dead
		self.reset()

	def check_dead(self):
		if self.hp <= 0:
			self.die()

	def out_of_spirit(self):
		battlelog.log("\n%s collapses of exhaustion.\n" %(self.name))
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
		battlelog.log("%s is delayed for %d turn\n" %(self.name, turn))
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
		battlelog.log("%s gains %d extra action\n" %(self.name, turn))

	def get_armor(self):
		return self.armor

	def gain_armor(self, armor, is_cumul):
		current_armor = self.armor
		if is_cumul:
			self.armor += armor
		else:
			self.armor = max(self.armor, armor)
		if current_armor < self.armor:
			battlelog.log("%s's armor raises to %d\n" %(self.name, self.armor))
		else:
			battlelog.log("%s's armor remains at %d\n" %(self.name, self.armor))

	def lose_armor(self, armor):
		self.armor = max(0, self.armor - armor)
		battlelog.log("%s's armor drops to %d\n" %(self.name, self.armor))

	def get_ward(self):
		return self.ward

	def gain_ward(self, ward, is_cumul):
		current_ward = self.ward
		if is_cumul:
			self.ward += ward
		else:
			self.ward = max(self.ward, ward)
		if current_ward < self.ward:
			battlelog.log("%s's ward raises to %d\n" %(self.name, self.ward))
		else:
			battlelog.log("%s's ward remains at %d\n" %(self.name, self.ward))

	def lose_ward(self, ward):
		self.ward = max(0, self.ward - ward)
		battlelog.log("%s's ward drops to %d\n" %(self.name, self.ward))

	def get_willpower(self):
		return self.willpower

	def gain_willpower(self, willpower, is_cumul):
		current_willpower = self.willpower
		if is_cumul:
			self.willpower += willpower
		else:
			self.willpower = max(self.willpower, willpower)
		if current_willpower < self.willpower:
			battlelog.log("%s's willpower raises to %d\n" %(self.name, self.willpower))
		else:
			battlelog.log("%s's willpower remains at %d\n" %(self.name, self.willpower))

	def lose_willpower(self, willpower):
		self.willpower = max(0, self.willpower - willpower)
		battlelog.log("%s's willpower drops to %d\n" %(self.name, self.willpower))

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
		battlelog.log("%s's next melee attack is increase by up to %d\n" %(self.name, boost))

	def gain_magic_NPB(self, boost):
		self.magic_NPB += boost
		battlelog.log("%s's next magic attack is increase by up to %d\n" %(self.name, boost))

	def gain_spirit_NPB(self, boost):
		self.spirit_NPB += boost
		battlelog.log("%s's next spirit attack is increase by up to %d\n" %(self.name, boost))

	def gain_melee_CPB(self, boost):
		self.melee_CPB += boost
		battlelog.log("%s's ongoing melee attack is increase by up to %d\n" %(self.name, boost))

	def gain_magic_CPB(self, boost):
		self.magic_CPB += boost
		battlelog.log("%s's ongoing magic attack is increase by up to %d\n" %(self.name, boost))

	def gain_spirit_CPB(self, boost):
		self.spirit_CPB += boost
		battlelog.log("%s's ongoing spirit attack is increase by up to %d\n" %(self.name, boost))

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

	def take_melee_damage(self, melee, penetrating):
		if melee > self.armor:
			pierced = self.armor * penetrating / 100
			absorbed = self.armor - pierced
			damage = melee - self.armor + pierced
			self.armor = 0
		else:
			pierced = melee * penetrating / 100
			absorbed = melee - pierced
			damage = pierced
			self.armor -= melee
		if pierced > 0:
			battlelog.log("%s takes %d melee damage (%d absorbed, %d pierced)\n" %(self.name, damage, absorbed, pierced))
		elif absorbed > 0:
			battlelog.log("%s takes %d melee damage (%d absorbed)\n" %(self.name, damage, absorbed))
		else:
			battlelog.log("%s takes %d melee damage\n" %(self.name, damage))
		self.reduce_hp(damage)
		return damage, absorbed, pierced

	def take_magic_damage(self, magic, penetrating):
		if magic > self.ward:
			pierced = self.ward * penetrating / 100
			absorbed = self.ward - pierced
			damage = magic - self.ward + pierced
			self.ward = 0
		else:
			pierced = magic * penetrating / 100
			absorbed = magic - pierced
			damage = pierced
			self.ward -= magic
		if pierced > 0:
			battlelog.log("%s takes %d magic damage (%d absorbed, %d pierced)\n" %(self.name, damage, absorbed, pierced))
		elif absorbed > 0:
			battlelog.log("%s takes %d magic damage (%d absorbed)\n" %(self.name, damage, absorbed))
		else:
			battlelog.log("%s takes %d magic damage\n" %(self.name, damage))
		self.reduce_hp(damage)
		return damage, absorbed, pierced

	def take_spirit_damage(self, spirit, penetrating):
		if spirit > self.willpower:
			pierced = self.willpower * penetrating / 100
			absorbed = self.willpower - pierced
			damage = spirit - self.willpower + pierced
			self.willpower = 0
		else:
			pierced = spirit * penetrating / 100
			absorbed = spirit - pierced
			damage = pierced
			self.willpower -= spirit
		if pierced > 0:
			battlelog.log("%s takes %d spirit damage (%d absorbed, %d pierced)\n" %(self.name, damage, absorbed, pierced))
		elif absorbed > 0:
			battlelog.log("%s takes %d spirit damage (%d absorbed)\n" %(self.name, damage, absorbed))
		else:
			battlelog.log("%s takes %d spirit damage\n" %(self.name, damage))
		while damage > 0 and self.spirit > 0:
			damage -= 1
			self.spirit -= 1
			self.charm_thrown_each_turn.append(self.charm_list.next())
		return damage, absorbed, pierced

	def get_hp(self):
		return self.hp

	def life_lose(self, hp):
		battlelog.log("%s lose %d life\n" %(self.name, hp))
		self.reduce_hp(hp)

	def reduce_hp(self, hp):
		if self.hp > hp:
			self.hp -= hp
		else:
			self.hp = 0

	def heal(self, hp):
		battlelog.log("%s heals %d damage\n" %(self.name, hp))
		self.increase_hp(hp)

	def increase_hp(self, hp):
		self.hp = max(self.hp+hp, self.max_hp)

	def reduce_spirit(self, spirit):
		if self.spirit > spirit:
			self.spirit -= spirit
		else:
			self.spirit = 0

	def play_stun(self, turn_num):
		self.stun_turn -= 1
		battlelog.log("%s is stunned\n" %(self.name))
		if turn_num not in self.charm_used_each_turn:
			self.charm_used_each_turn[turn_num] = []

	def attach(self, long_time_effect):
		long_time_effect.attach_log(self.name)
		self.long_time_effect_list.append(long_time_effect)

	def play_charm(self, allies, enimies, turn_num):
		self.actions += 1
		charm = self.charm_list.next()
		if turn_num not in self.charm_used_each_turn:
			self.charm_used_each_turn[turn_num] = []
		self.charm_used_each_turn[turn_num].append(charm)
		battlelog.log("%s uses [%s]\n" %(self.name, charm.name))
		charm.execute(self, allies, enimies)

	def trigger_effects_normal(self, allies, enimies):
		for effect in self.long_time_effect_list[:]:
			effect.trigger_normal(allies, enimies)
		for effect in self.long_time_effect_list[:]:
			if effect.end():
				self.long_time_effect_list.remove(effect)

	def trigger_effects_stun(self, allies, enimies):
		for effect in self.long_time_effect_list[:]:
			effect.trigger_stun(allies, enimies)
		for effect in self.long_time_effect_list[:]:
			if effect.end():
				self.long_time_effect_list.remove(effect)

	def trigger_effects_extra_action(self, allies, enimies):
		for effect in self.long_time_effect_list[:]:
			effect.trigger_extra_action(allies, enimies)
		for effect in self.long_time_effect_list[:]:
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
