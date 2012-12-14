import copy
from common.alltype import EffectType

class Effect(object):
	@staticmethod
	def fromJsonObj(obj):
		effect_type = getattr(EffectType, obj['effect_type'])
		if effect_type == EffectType.Melee:
			return Melee.fromJsonObj(obj['params'])
		else:
			assert False

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


class Melee(Damage):
	def __init__(self, damage, p):
		super(Melee, self).__init__(damage, p)

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

	def toJsonObj(self):
		return {'effect_type': EffectType.reverse(EffectType.Melee), 'params': {'damage': self.damage, 'p': self.p}}

	@staticmethod
	def fromJsonObj(obj):
		damage = obj['damage']
		p = obj['p']
		return Melee(damage, p)
		

class MeleeDrain(Melee):
	def __init__(self, damage, p):
		super(MeleeDrain, self).__init__(damage, p)

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

class Magic(Damage):
	def __init__(self, damage, p):
		super(Magic, self).__init__(damage, p)

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

class MagicDrain(Magic):
	def __init__(self, damage, p):
		super(MagicDrain, self).__init__(damage, p)

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

class ShiftingDamage(Damage):
	def __init__(self, damage, p):
		super(ShiftingDamage, self).__init__(damage, p)

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

class Spirit(Damage):
	def __init__(self, damage):
		super(Spirit, self).__init__(damage, 0)

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


class Defense(Effect):
	def __init__(self, defense, is_cumul):
		self.defense = defense
		self.is_cumul = is_cumul

	def calDef(self, old_defense):
		if self.is_cumul:
			return old_defense + self.defense
		else:
			return max(old_defense, self.defense)


class Armor(Defense):
	def __init__(self, defense, is_cumul):
		super(Armor, self).__init__(defense, is_cumul)

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Armor = self.calDef(target.Armor)

class Ward(Defense):
	def __init__(self, defense, is_cumul):
		super(Ward, self).__init__(defense, is_cumul)

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Ward = self.calDef(target.Ward)

class ShiftingDefense(Defense):
	def __init__(self, defense, is_cumul):
		super(ShiftingDefense, self).__init__(defense, is_cumul)

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		if armor < ward:
			armor = self.calDef(target.Armor)
		else:
			ward = self.calDef(target.Ward)

class Willpower(Defense):
	def __init__(self, defense, is_cumul):
		super(Willpower, self).__init__(defense, is_cumul)

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Willpower = self.calDef(target.Willpower)


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

class Heal(Effect):
	def __init__(self, life):
		self.life = life

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.increaseHp(self.life)
		return

class LifeLose(Effect):
	def __init__(self, life):
		self.life = life

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.reduceHp(self.life)
		return

class ArmorDestroy(Effect):
	def __init__(self, armor):
		self.armor = armor

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Armor = max(target.Armor - self.armor, 0)
		return

class WardDestroy(Effect):
	def __init__(self, ward):
		self.ward = ward

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Ward = max(target.Ward - self.ward, 0)
		return

class WillpowerDestroy(Effect):
	def __init__(self, willpower):
		self.willpower = willpower

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Willpower = max(target.Willpower - self.willpower, 0)
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

class Stun(Effect):
	def __init__(self, turn):
		self.turn = turn

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.stun_turn = max(target.stun_turn, self.turn)
		return

class NextMelee(Effect):
	def __init__(self, PB):
		self.PB = PB

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Melee_NPB += self.PB
		return

class NextMagic(Effect):
	def __init__(self, PB):
		self.PB = PB

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Magic_NPB += self.PB
		return

class OngoingMelee(Effect):
	def __init__(self, PB):
		self.PB = PB

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Melee_CPB += self.PB
		return

class OngoingMagic(Effect):
	def __init__(self, PB):
		self.PB = PB

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.Magic_CPB += self.PB
		return

class Cleanse(Effect):
	def __init__(self):
		pass

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.cleanse()
		return

class Purge(Effect):
	def __init__(self):
		pass

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.purge()
		return

class Normalize(Effect):
	def __init__(self):
		pass

	def run(self, subject, target, is_EA, is_attachment, AOE_players=None):
		target.normalize()
		return


class Aura(Effect):
	def __init__(self, turn, arua_type, attach_charm):
		self.turn = turn
		self.aura_type = aura_type
		self.attach_charm = attach_charm

	def run(self, subject, allies, enimies, is_EA):
		if is_EA:
			pass
		else:
			if self.aura_type == EffectType.Effect_After:
				if self.turn == 1:
					self.attach_charm.run(subject, allies, enimies)
				self.turn -= 1
			elif self.aura_type == EffectType.Effect_Duration:
				self.attach_charm.run(subject, allies, enimies)
				self.turn -= 1
			else:
				assert False


class Bane(Effect):
	def __init__(self, turn, bane_type, attach_charm):
		self.turn = turn
		self.bane_type = bane_type
		self.attach_charm = attach_charm

	def run(self, subject, allies, enimies, is_EA):
		if self.bane_type == EffectType.Effect_After:
			if self.turn == 1:
				self.attach_charm.run(subject, allies, enimies)
			self.turn -= 1
		elif self.bane_type == EffectType.Effect_Duration:
			self.attach_charm.run(subject, allies, enimies)
			if not is_EA:
				self.turn -= 1
		else:
			assert False


class Curse(Effect):
	def __init__(self, turn, attach_charm):
		self.turn = turn
		self.attach_charm = attach_charm

	def run(self, subject, allies, enimies, is_EA):
		if self.curse_type == EffectType.Effect_After:
			if self.turn == 1:
				self.attach_charm.run(subject, allies, enimies)
			self.turn -= 1
		elif self.curse_type == EffectType.Effect_Duration:
			self.attach_charm.run(subject, allies, enimies)
			self.turn -= 1
		else:
			assert False


class Summon(Effect):
	def __init__(self, turn, attach_charm):
		self.turn = turn
		self.attach_charm = attach_charm

	def run(self, subject, allies, enimies, is_EA):
		if is_EA:
			pass
		else:
			if self.summon_type == EffectType.Effect_After:
				if self.turn == 1:
					self.attach_charm.run(subject, allies, enimies)
				self.turn -= 1
			elif self.summon_type == EffectType.Effect_Duration:
				self.attach_charm.run(subject, allies, enimies)
				self.turn -= 1
			else:
				assert False