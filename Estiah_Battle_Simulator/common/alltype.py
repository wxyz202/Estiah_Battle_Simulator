class BaseType(object):
	@classmethod
	def reverse(cls, value):
		for attr in dir(cls):
			if attr.startswith('_'):
				continue
			if getattr(cls, attr) == value:
				return attr
		return None

class EffectType(BaseType):
	Null = 0
	Melee = 1
	MeleeDrain = 2
	Magic = 3
	MagicDrain = 4
	ShiftingDamage = 5
	Spirit = 6
	Armor = 7
	Ward = 8
	ShiftingDefense = 9
	Willpower = 10
	Projection = 11
	Heal = 12
	LifeLose = 13
	ArmorDestroy = 14
	WardDestroy = 15
	WillpowerDestroy = 16
	ExtraAction = 17
	FocusOrProtect = 18
	Stun = 19
	NextMelee = 20
	NextMagic = 21
	OngoingMelee = 22
	OngoingMagic = 23
	Cleanse = 24
	Purge = 25
	Normalize = 26
	Aura = 27
	Bane = 28
	Curse = 29
	Summon = 30
	Effect_After = 1000
	Effect_During = 1001

class PlayerType(BaseType):
	Random = -1
	Alive = 0
	Dead = 1
	Out_of_Spirit = 2
	Attacker = 3
	Defender = 4

class TargetType(BaseType):
	Null = 0
	Enimy = 1
	Self = 2
	AllAllies = 3
	AllEnimies = 4
	All = 5
	LowestHpEnimy = 6

class RuneType(BaseType):
	Null = 0
	Axe = 1
	Sword = 2
	Mace = 3
	Twinblades = 4
	Spear = 5
	Fist = 6
	Earth = 7
	Shadow = 8
	Holy = 9
	Lighting = 10
	Frost = 11
	Fire = 12
	Spirit = 13
	Armor = 14
	Ward = 15
	Willpower = 16
	Summon = 17
	Buff = 18
	Debuff = 19
	Tech = 20

class ConditionType(BaseType):
	Null = 0
	EndCondition = 1
	BeingTarget = 2

class LineType(BaseType):
	Condition = 0
	Effect = 1
