from common.enumtype import EffectType
import constants

class Effect(object):
	@staticmethod
	def from_json_obj(obj):
		effect_type = obj['effect_type']
		params = obj['params']
		return globals()[effect_type].from_json_obj(params)


class Damage(Effect):
	def __init__(self, damage, penetrating=0):
		self.damage = damage
		self.penetrating = penetrating

	def cal_damage(self, CPB, NPB, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier):
		booster = int((CPB * CPB_multiplier + NPB * NPB_multiplier) * total_booster_multiplier)
		damage = self.damage * base_multiplier
		penetrating = self.penetrating * 3 * damage / (3 * damage + booster)
		damage += booster
		return damage, penetrating

	@staticmethod
	def cal_real_damage(damage, penetrating, defense):
		if damage <= defense:
			return damage*penetrating/100, defense-damage
		else:
			return (damage-defense + defense*penetrating/100), 0

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'damage': self.damage,
				'penetrating': self.penetrating
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		damage = obj['damage']
		penetrating = obj['penetrating']
		return cls(damage, penetrating)

class Melee(Damage):
	def execute(self, subject, target, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier):
		melee, penetrating = self.cal_damage(subject.get_melee_CPB(), subject.get_melee_NPB(), base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
		armor = target.get_armor()
		melee, armor = cal_real_damage(melee, penetrating, armor)
		target.set_armor(armor)
		subject.duel_melee_damage(melee)
		if subject.NPB_multiplier != 0:
			subject.use_melee_NPB()
		target.take_melee_damage(melee)
		return
		
class MeleeDrain(Melee):
	def execute(self, subject, target, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier):
		total_booster_multiplier *= constants.DRAIN_BOOSTER_MULTIPLIER
		melee, penetrating = self.cal_damage(subject.get_melee_CPB(), subject.get_melee_NPB(), base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
		armor = target.get_armor()
		melee, armor = cal_real_damage(melee, penetrating, armor)
		target.set_armor(armor)
		subject.duel_melee_damage(melee)
		if subject.NPB_multiplier != 0:
			subject.use_melee_NPB()
		target.take_melee_damage(melee)
		subject.increase_hp(melee)
		return

class Magic(Damage):
	def execute(self, subject, target, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier):
		magic, penetrating = self.cal_damage(subject.get_magic_CPB(), subject.get_magic_NPB(), base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
		ward = target.get_ward()
		magic, ward = cal_real_damage(magic, penetrating, ward)
		target.set_ward(ward)
		subject.duel_magic_damage(magic)
		if subject.NPB_multiplier != 0:
			subject.use_magic_NPB()
		target.take_magic_damage(magic)
		return

class MagicDrain(Magic):
	def execute(self, subject, target, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier):
		total_booster_multiplier *= constants.DRAIN_BOOSTER_MULTIPLIER
		magic, penetrating = self.cal_damage(subject.get_magic_CPB(), subject.get_magic_NPB(), base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
		ward = target.get_ward()
		magic, ward = cal_real_damage(magic, penetrating, ward)
		target.set_ward(ward)
		subject.duel_magic_damage(magic)
		if subject.NPB_multiplier != 0:
			subject.use_magic_NPB()
		target.take_magic_damage(magic)
		subject.increase_hp(magic)
		return

class ShiftingDamage(Damage):
	def execute(self, subject, target, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier):
		melee, penetrating = self.cal_damage(subject.get_melee_CPB(), subject.get_melee_NPB(), base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
		armor = target.get_armor()
		melee, armor = cal_real_damage(melee, penetrating, armor)
		magic, penetrating = self.cal_damage(subject.get_magic_CPB(), subject.get_magic_NPB(), base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
		ward = target.get_ward()
		magic, ward = cal_real_damage(magic, penetrating, ward)
		if melee > magic:
			subject.duel_melee_damage(melee)
			if subject.NPB_multiplier != 0:
				subject.use_melee_NPB()
			target.take_melee_damage(melee)
			target.set_armor(armor)
		else:
			subject.duel_magic_damage(magic)
			if subject.NPB_multiplier != 0:
				subject.use_magic_NPB()
			target.take_magic_damage(magic)
			target.set_ward(ward)
		return

class Spirit(Damage):
	def cal_damage(self, CPB_multiplier, NPB_multiplier, total_booster_multiplier):
		if CPB_multiplier != 0:
			CPB_multiplier = 1
		if NPB_multiplier != 0:
			NPB_multiplier = 1
		if total_booster_multiplier != 0:
			total_booster_multiplier = 1
		return Damage.cal_damage(self, CPB_multiplier, NPB_multiplier, total_booster_multiplier) 
	
	def execute(self, subject, target, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier):
		spirit, penetrating = self.cal_damage(subject.get_spirit_CPB(), subject.get_spirit_NPB(), base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
		willpower = target.get_willpower()
		spirit, willpower = cal_real_damage(spirit, penetrating, willpower)
		target.set_willpower(willpower)
		subject.duel_spirit_damage(spirit)
		if subject.NPB_multiplier != 0:
			subject.use_spirit_NPB()
		target.take_spirit_damage(spirit)
		return


class Defense(Effect):
	def __init__(self, defense, is_cumul):
		self.defense = defense
		self.is_cumul = is_cumul

	def cal_defense(self, old_defense, base_multiplier):
		if self.is_cumul:
			return old_defense + self.defense * base_multiplier
		else:
			return max(old_defense, self.defense * base_multiplier)

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'defense': self.defense,
				'is_cumul': self.is_cumul
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		defense = obj['defense']
		is_cumul = obj['is_cumul']
		return cls(defense, is_cumul)


class Armor(Defense):
	def execute(self, subject, target, base_multiplier):
		target.set_armor(self.cal_defense(target.get_armor(), base_multiplier))

class Ward(Defense):
	def execute(self, subject, target, base_multiplier):
		target.set_ward(self.cal_defense(target.get_ward(), base_multiplier))

class ShiftingDefense(Defense):
	def execute(self, subject, target, base_multiplier):
		armor = target.get_armor()
		ward = target.get_ward()
		if armor < ward:
			target.set_armor(self.cal_defense(armor),base_multiplier)
		else:
			target.set_ward(self.cal_defense(ward),base_multiplier)

class Willpower(Defense):
	def execute(self, subject, target, base_multiplier):
		target.set_willpower(self.cal_defense(target.get_willpower(), base_multiplier))


class Projection(Effect):
	def __init__(self, max_damage, damage_type, defense_type):
		self.max_damage = max_damage
		self.damage_type = damage_type
		self.defense_type = defense_type

	def execute(self, subject, target):
		if self.defense_type == EffectType.Armor:
			defense = subject.get_armor()
		elif self.defense_type == EffectType.Ward:
			defense = subject.get_ward()
		else:
			assert False
		damage = max(defense, self.max_damage)
		if self.damage_type == EffectType.Melee:
			armor = target.get_armor()
			melee, armor = Damage.cal_real_damage(damage, 0, armor)
			target.set_armor(armor)
			subject.duel_melee_damage(melee)
			target.take_melee_damage(melee)
		elif self.damage_type == EffectType.Magic:
			ward = target.get_ward()
			magic, ward = Damage.cal_real_damage(damage, 0, ward)
			target.set_ward(ward)
			subject.duel_magic_damage(magic)
			target.take_magic_damage(magic)
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'max_damage': self.max_damage,
				'damage_type': EffectType.reverse(damage_type),
				'defense_type': EffectType.reverse(defense_type)
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		max_damage = obj['max_damage']
		damage_type = getattr(EffectType,obj['damage_type'])
		defense_type = getattr(EffectType,obj['defense_type'])
		return cls(max_damage, damage_type, defense_type)

class Heal(Effect):
	def __init__(self, life):
		self.life = life

	def execute(self, subject, target, base_multiplier):
		target.increase_hp(self.life * base_multiplier)
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'life': self.life
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		life = obj['life']
		return cls(life)

class LifeLose(Effect):
	def __init__(self, life):
		self.life = life

	def execute(self, subject, target, base_multiplier):
		target.reduce_hp(self.life * base_multiplier)
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'life': self.life
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		life = obj['life']
		return cls(life)


class DefenseDestroy(Effect):
	def __init__(self, defense):
		self.defense = defense

	def cal_defense(old_defense, base_multiplier):
		return max(old_defense - self.defense * base_multiplier, 0)

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'defense': self.defense
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		defense = obj['defense']
		return cls(defense)

class ArmorDestroy(DefenseDestroy):
	def execute(self, subject, target, base_multiplier):
		target.set_ward(self.cal_defense(target.get_armor(), base_multiplier))
		return

class WardDestroy(DefenseDestroy):
	def execute(self, subject, target, base_multiplier):
		target.set_ward(self.cal_defense(target.get_ward(), base_multiplier))
		return

class WillpowerDestroy(DefenseDestroy):
	def execute(self, subject, target, base_multiplier):
		target.set_willpower(self.cal_defense(target.get_willpower(), base_multiplier))
		return

class ExtraAction(Effect):
	def __init__(self, turn):
		self.turn = turn

	def execute(self, subject, target, base_multiplier):
		target.gain_extra_action(self.turn * base_multiplier)
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'turn': self.turn
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		turn = obj['turn']
		return cls(turn)

class FocusProtect(Effect):
	def __init__(self, turn, is_cumul):
		self.turn = turn
		self.is_cumul = is_cumul

	def execute(self, subject, target, allies, enimies):
		if target in allies:
			target_party = allies
		else:
			target_party = enimies
		target.gain_being_target(self.turn, self.is_cumul)
		for player in target_party:
			if player is not target:
				player.clear_being_target()
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'turn': self.turn,
				'is_cumul': self.is_cumul
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		turn = obj['turn']
		is_cumul = obj['is_cumul']
		return cls(turn, is_cumul)

class BreakFocus(Effect):
	def __init__(self):
		pass

	def execute(self, subject, target):
		#TODO
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		return cls()

class Vanish(Effect):
	def __init__(self):
		pass

	def execute(self, subject, target):
		target.clear_being_target()
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		return cls()

class Stun(Effect):
	def __init__(self, turn):
		self.turn = turn

	def execute(self, subject, target):
		target.gain_stun(self.turn)
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'turn': self.turn
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		turn = obj['turn']
		return cls(turn)


class Booster(Effect):
	def __init__(self, boost):
		self.boost = boost

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'boost': self.boost
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		boost = obj['boost']
		return cls(boost)


class NextMelee(Booster):
	def execute(self, subject, target):
		target.gain_melee_NPB(self.boost)
		return

class NextMagic(Booster):
	def execute(self, subject, target):
		target.gain_magic_NPB(self.boost)
		return

class NextSpirit(Booster):
	def execute(self, subject, target):
		target.gain_spirit_NPB(self.boost)
		return

class OngoingMelee(Booster):
	def execute(self, subject, target):
		target.gain_melee_CPB(self.boost)
		return

class OngoingMagic(Booster):
	def execute(self, subject, target):
		target.gain_magic_CPB(self.boost)
		return

class OngoingSpirit(Booster):
	def execute(self, subject, target):
		target.gain_spirit_CPB(self.boost)
		return


class Cleanse(Effect):
	def __init__(self):
		pass

	def execute(self, subject, target):
		target.cleanse()
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		return cls()

class Purge(Effect):
	def __init__(self):
		pass

	def execute(self, subject, target):
		target.purge()
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		return cls()

class Normalize(Effect):
	def __init__(self):
		pass

	def execute(self, subject, target):
		target.normalize()
		return

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		return cls()


class Attach(Effect):
	def __init__(self, long_time_effect):
		self.long_time_effect = long_time_effect

	def execute(self, subject, target):
		long_time_effect = copy.deepcopy(self.long_time_effect)
		long_time_effect.subject = subject
		long_time_effect.target = target
		target.attach(long_time_effect)

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'long_time_effect': self.long_time_effect.to_json_obj()
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		long_time_effect = Effect.from_json_obj(obj['long_time_effect'])
		return cls(long_time_effect)

class LongTimeEffect(Effect):
	def __init__(self, turn, long_time_type, attach_charm):
		self.turn = turn
		self.long_time_type = long_time_type
		self.attach_charm = attach_charm
		self.attach_charm.source = self

	def end(self):
		return self.turn == 0

	def is_affect_attach_target(self):
		return isinstance(self, Bane) or isinstance(self, Curse)

	def trigger(self, allies, enimies):
		if self.long_time_type == EffectType.AttachmentDuring:
			self.attach_charm.execute(self.subject, allies, enimies)
		elif self.long_time_type == EffectType.AttachmentAfter:
			if self.turn == 0:
				self.attach_charm.execute(self.subject, allies, enimies)
		else:
			assert False

	def trigger_normal(self, allies, enimies):
		self.turn -= 1
		self.trigger(self, allies, enimies)

	def to_json_obj(self):
		obj = {
			'effect_type': self.__class__.__name__,
			'params': {
				'turn': self.turn,
				'long_time_type': EffectType.reverse(self.long_time_type),
				'attach_charm': self.attach_charm.to_json_obj()
			}
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		turn = obj['turn']
		long_time_type = getattr(EffectType,obj['long_time_type'])
		from charm import AttachCharm
		attach_charm = AttachCharm.from_json_obj(obj['attach_charm'])
		return cls(turn, long_time_type, attach_charm)

class Aura(LongTimeEffect):
	def trigger_stun(self, allies, enimies):
		self.turn -= 1
		self.trigger(self, allies, enimies)

	def trigger_extra_action(self, allies, enimies):
		pass

class Bane(LongTimeEffect):
	def trigger_stun(self, allies, enimies):
		pass

	def trigger_extra_action(self, allies, enimies):
		if self.long_time_effect == EffectType.AttachmentAfter:
			self.turn -= 1
		self.trigger(self, allies, enimies)

class Curse(LongTimeEffect):
	def trigger_stun(self, allies, enimies):
		self.turn -= 1
		self.trigger(self, allies, enimies)

	def trigger_extra_action(self, allies, enimies):
		self.turn -= 1
		self.trigger(self, allies, enimies)

class Summon(LongTimeEffect):
	def trigger_stun(self, allies, enimies):
		self.turn -= 1
		self.trigger(self, allies, enimies)

	def trigger_extra_action(self, allies, enimies):
		pass
