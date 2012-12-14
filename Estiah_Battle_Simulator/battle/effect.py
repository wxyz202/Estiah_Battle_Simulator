import copy
from common.alltype import EffectType

class Effect(object):
	@staticmethod
	def fromJsonObj(obj):
		effect_type = obj['effect_type']
		params = obj['params']
		return globals()[effect_type].fromJsonObj(params)


def damagedecorator(cls):
	def __init__(self, damage, p=0):
		super(cls, self).__init__(damage, p)

	def toJsonObj(self):
		return {'effect_type': cls.__name__, 'params': {'damage': self.damage, 'p': self.p}}

	@staticmethod
	def fromJsonObj(obj):
		damage = obj['damage']
		p = obj['p']
		return cls(damage, p)

	cls.__init__ = __init__
	cls.toJsonObj = toJsonObj
	cls.fromJsonObj = fromJsonObj
	return cls

class Damage(Effect):
	def __init__(self, damage, p):
		self.damage = damage
		self.p = p

	def calDamage(self, CPB=0, NPB=0, is_EA=False, AOE_players=None):
		booster = CPB
		if is_EA and not isinstance(self, Spirit):
			booster += CPB/5
		booster += NPB
		if AOE_players is not None and not isinstance(self, Spirit):
			booster = int(round(booster*4/3.0/AOE_players))
		damage = self.damage + booster
		p = int(self.p*(3*self.damage/(3*self.damage+booster)))
		return damage, p

	@staticmethod
	def calRealDamage(damage, p, defense):
		if damage <= defense:
			return damage*p/100, defense-damage
		else:
			return damage-defense + defense*p/100, 0

@damagedecorator
class Melee(Damage):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if is_attachment:
			melee, melee_p = self.calDamage(0, 0, is_EA, AOE_players)
		else:
			melee, melee_p = self.calDamage(subject.Melee_CPB, subject.Melee_NPB, is_EA, AOE_players)
		armor = target.Armor
		melee, armor = calRealDamage(melee, melee_p, armor)
		target.Armor = armor
		target.reduceHp(melee)
		return

@damagedecorator
class MeleeDrain(Melee):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if is_attachment:
			melee, melee_p = self.calDamage(0, 0, is_EA, AOE_players)
		else:
			melee, melee_p = self.calDamage(subject.Melee_CPB, subject.Melee_NPB, is_EA, AOE_players)
		armor = target.Armor
		melee, armor = calRealDamage(melee, melee_p, armor)
		target.Armor = armor
		target.reduceHp(melee)
		if is_attachment:
			subject.increaseHp(int(melee*0.65))
		else:
			subject.increaseHp(melee)
		return

@damagedecorator
class Magic(Damage):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if is_attachment:
			magic, magic_p = self.calDamage(0, 0, is_EA, AOE_players)
		else:
			magic, magic_p = self.calDamage(subject.Magic_CPB, subject.Magic_NPB, is_EA, AOE_players)
		ward = target.Ward
		magic, ward = calRealDamage(magic, magic_p, ward)
		target.Ward = ward
		target.reduceHp(magic)
		return

@damagedecorator
class MagicDrain(Magic):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if is_attachment:
			magic, magic_p = self.calDamage(0, 0, is_EA, AOE_players)
		else:
			magic, magic_p = self.calDamage(subject.Magic_CPB, subject.Magic_NPB, is_EA, AOE_players)
		ward = target.Ward
		magic, ward = calRealDamage(magic, magic_p, ward)
		target.Ward = ward
		target.reduceHp(magic)
		if is_attachment:
			subject.increaseHp(int(magic*0.65))
		else:
			subject.increaseHp(magic)
		return

@damagedecorator
class ShiftingDamage(Damage):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if is_attachment:
			melee, melee_p = self.calDamage(0, 0, is_EA, AOE_players)
			magic, magic_p = self.calDamage(0, 0, is_EA, AOE_players)
		else:
			melee, melee_p = self.calDamage(subject.Melee_CPB, subject.Melee_NPB, is_EA, AOE_players)
			magic, magic_p = self.calDamage(subject.Magic_CPB, subject.Magic_NPB, is_EA, AOE_players)
		armor = target.Armor
		melee, armor = calRealDamage(melee, melee_p, armor)
		ward = target.Ward
		magic, ward = calRealDamage(magic, magic_p, ward)
		if melee > magic:
			target.Armor = armor
			target.reduceHp(melee)
		else:
			target.Ward = ward
			target.reduceHp(magic)
		return

@damagedecorator
class Spirit(Damage):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if is_attachment:
			spirit, spirit_p = self.calDamage(0, 0, is_EA, AOE_players)
		else:
			spirit, spirit_p = self.calDamage(subject.Spirit_CPB, subject.Spirit_NPB, is_EA, AOE_players)
		willpower = target.Willpower
		spirit, willpower = calRealDamage(spirit, spirit_p, willpower)
		target.willpower = willpower
		target.reduceSpirit(spirit)
		return


def defensedecorator(cls):
	def __init__(self, defense, is_cumul):
		super(cls, self).__init__(defense, is_cumul)

	def toJsonObj(self):
		return {'effect_type': cls.__name__, 'params': {'defense': self.defense, 'is_cumul': self.is_cumul}}

	@staticmethod
	def fromJsonObj(obj):
		defense = obj['defense']
		is_cumul = obj['is_cumul']
		return cls(defense, is_cumul)

	cls.__init__ = __init__
	cls.toJsonObj = toJsonObj
	cls.fromJsonObj = fromJsonObj
	return cls

class Defense(Effect):
	def __init__(self, defense, is_cumul):
		self.defense = defense
		self.is_cumul = is_cumul

	def calDefense(self, old_defense):
		if self.is_cumul:
			return old_defense + self.defense
		else:
			return max(old_defense, self.defense)

@defensedecorator
class Armor(Defense):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Armor = self.calDefense(target.Armor)

@defensedecorator
class Ward(Defense):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Ward = self.calDefense(target.Ward)

@defensedecorator
class ShiftingDefense(Defense):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if armor < ward:
			armor = self.calDefense(target.Armor)
		else:
			ward = self.calDefense(target.Ward)

@defensedecorator
class Willpower(Defense):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Willpower = self.calDefense(target.Willpower)


class Projection(Effect):
	def __init__(self, max_damage, damage_type, defense_type):
		self.max_damage = max_damage
		self.damage_type = damage_type
		self.defense_type = defense_type

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if self.defense_type == EffectType.Armor:
			defense = subject.Armor
		elif self.defense_type == EffectType.Ward:
			defense = subject.Ward
		else:
			assert False
		damage = max(defense, self.max_damage)
		if self.damage_type == EffectType.Melee:
			effect_obj = Melee(damage, 0)
		elif self.damage_type == EffectType.Magic:
			effect_obj = Magic(damage, 0)
		effect_obj.run(subject, target, is_EA=False, is_attachment=True, AOE_players=None)
		return

	def toJsonObj(self):
		return {'effect_type': 'Projection', 'params': {'max_damage': self.max_damage, 'damage_type': EffectType.reverse(damage_type), 'defense_type': EffectType.reverse(defense_type)}}

	@staticmethod
	def fromJsonObj(obj):
		max_damage = obj['max_damage']
		damage_type = getattr(EffectType,obj['damage_type'])
		defense_type = getattr(EffectType,obj['defense_type'])
		return Projection(max_damage, damage_type, defense_type)

class Heal(Effect):
	def __init__(self, life):
		self.life = life

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.increaseHp(self.life)
		return

	def toJsonObj(self):
		return {'effect_type': 'Heal', 'params': {'life': self.life}}

	@staticmethod
	def fromJsonObj(obj):
		life = obj['life']
		return Heal(life)

class LifeLose(Effect):
	def __init__(self, life):
		self.life = life

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.reduceHp(self.life)
		return

	def toJsonObj(self):
		return {'effect_type': 'LifeLose', 'params': {'life': self.life}}

	@staticmethod
	def fromJsonObj(obj):
		life = obj['life']
		return LifeLose(life)


def defensedestroydecorator(cls):
	def __init__(self, defense):
		super(cls, self).__init__(defense)

	def toJsonObj(self):
		return {'effect_type': cls.__name__, 'params': {'defense': self.defense}}

	@staticmethod
	def fromJsonObj(obj):
		defense = obj['defense']
		return cls(defense)

	cls.__init__ = __init__
	cls.toJsonObj = toJsonObj
	cls.fromJsonObj = fromJsonObj
	return cls

class DefenseDestroy(Effect):
	def __init__(self, defense):
		self.defense = defense

	def calDefense(old_defense):
		return max(old_defense - self.defense, 0)

@defensedestroydecorator
class ArmorDestroy(Effect):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Armor = self.calDefense(target.Armor)
		return

@defensedestroydecorator
class WardDestroy(Effect):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Ward = self.calDefense(target.Ward)
		return

@defensedestroydecorator
class WillpowerDestroy(Effect):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Willpower = self.calDefense(target.Willpower)
		return

class ExtraAction(Effect):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		pass
		return

class FocusOrProtect(Effect):
	def __init__(self, turn, is_cumul):
		self.turn = turn
		self.is_cumul = is_cumul

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if self.is_cumul:
			target.is_being_target_turn += self.turn
		else:
			target.is_being_target_turn = max(target.is_being_target_turn, self.turn)
		return

	def toJsonObj(self):
		return {'effect_type': 'FocusOrProtect', 'params': {'turn': self.turn, 'is_cumul': self.is_cumul}}

	@staticmethod
	def fromJsonObj(obj):
		turn = obj['turn']
		is_cumul = obj['is_cumul']
		return FocusOrProtect(turn, is_cumul)

class Stun(Effect):
	def __init__(self, turn):
		self.turn = turn

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.stun_turn = max(target.stun_turn, self.turn)
		return

	def toJsonObj(self):
		return {'effect_type': 'Stun', 'params': {'turn': self.turn}}

	@staticmethod
	def fromJsonObj(obj):
		turn = obj['turn']
		return Stun(turn)


def boosterdecorator(cls):
	def __init__(self, boost):
		super(cls, self).__init__(boost)

	def toJsonObj(self):
		return {'effect_type': cls.__name__, 'params': {'boost': self.boost}}

	@staticmethod
	def fromJsonObj(obj):
		boost = obj['boost']
		return cls(boost)

	cls.__init__ = __init__
	cls.toJsonObj = toJsonObj
	cls.fromJsonObj = fromJsonObj
	return cls

class Booster(Effect):
	def __init__(self, boost):
		self.boost = boost

@boosterdecorator
class NextMelee(Booster):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Melee_NPB += self.boost
		return

@boosterdecorator
class NextMagic(Booster):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Magic_NPB += self.boost
		return

@boosterdecorator
class OngoingMelee(Booster):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Melee_CPB += self.boost
		return

@boosterdecorator
class OngoingMagic(Booster):
	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Magic_CPB += self.boost
		return


class Cleanse(Effect):
	def __init__(self):
		pass

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.cleanse()
		return

	def toJsonObj(self):
		return {'effect_type': 'Cleanse', 'params': {}}

	@staticmethod
	def fromJsonObj(obj):
		return Cleanse()

class Purge(Effect):
	def __init__(self):
		pass

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.purge()
		return

	def toJsonObj(self):
		return {'effect_type': 'Purge', 'params': {}}

	@staticmethod
	def fromJsonObj(obj):
		return Purge()

class Normalize(Effect):
	def __init__(self):
		pass

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.normalize()
		return

	def toJsonObj(self):
		return {'effect_type': 'Normalize', 'params': {}}

	@staticmethod
	def fromJsonObj(obj):
		return Normalize()


def longtimeeffectdecorator(cls):
	def __init__(self, turn, long_time_type, attach_charm):
		super(cls, self).__init__(turn, long_time_type, attach_charm)

	def toJsonObj(self):
		return {'effect_type': cls.__name__, 'params': {'turn': self.turn, 'long_time_type': EffectType.reverse(self.long_time_type), 'attach_charm': self.attach_charm.id}}

	@staticmethod
	def fromJsonObj(obj):
		turn = obj['turn']
		long_time_type = getattr(EffectType,obj['long_time_type'])
		attach_charm = Charm.loadFromId(obj['attach_charm'])
		return cls(turn, long_time_type, attach_charm)

	cls.__init__ = __init__
	cls.toJsonObj = toJsonObj
	cls.fromJsonObj = fromJsonObj
	return cls

class LongTimeEffect(Effect):
	def __init__(self, turn, long_time_type, attach_charm):
		self.turn = turn
		self.long_time_type = long_time_type
		self.attach_charm = attach_charm

@longtimeeffectdecorator
class Aura(LongTimeEffect):
	def run(self, subject, allies, enimies, is_EA):
		if is_EA:
			pass
		else:
			if self.long_time_type == EffectType.Effect_After:
				if self.turn == 1:
					self.attach_charm.run(subject, allies, enimies)
				self.turn -= 1
			elif self.long_time_type == EffectType.Effect_Duration:
				self.attach_charm.run(subject, allies, enimies)
				self.turn -= 1
			else:
				assert False

@longtimeeffectdecorator
class Bane(LongTimeEffect):
	def run(self, subject, allies, enimies, is_EA):
		if self.long_time_type == EffectType.Effect_After:
			if self.turn == 1:
				self.attach_charm.run(subject, allies, enimies)
			self.turn -= 1
		elif self.long_time_type == EffectType.Effect_Duration:
			self.attach_charm.run(subject, allies, enimies)
			if not is_EA:
				self.turn -= 1
		else:
			assert False

@longtimeeffectdecorator
class Curse(LongTimeEffect):
	def run(self, subject, allies, enimies, is_EA):
		if self.long_time_type == EffectType.Effect_After:
			if self.turn == 1:
				self.attach_charm.run(subject, allies, enimies)
			self.turn -= 1
		elif self.long_time_type == EffectType.Effect_Duration:
			self.attach_charm.run(subject, allies, enimies)
			self.turn -= 1
		else:
			assert False

@longtimeeffectdecorator
class Summon(LongTimeEffect):
	def run(self, subject, allies, enimies, is_EA):
		if is_EA:
			pass
		else:
			if self.long_time_type == EffectType.Effect_After:
				if self.turn == 1:
					self.attach_charm.run(subject, allies, enimies)
				self.turn -= 1
			elif self.long_time_type == EffectType.Effect_Duration:
				self.attach_charm.run(subject, allies, enimies)
				self.turn -= 1
			else:
				assert False