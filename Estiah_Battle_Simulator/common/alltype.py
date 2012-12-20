class BaseEnumType(object):
	def __init__(self, s):
		elements = s.split()
		self.__enum_dict = dict(zip(elements, range(len(elements))))

	def __getattr__(self, attr):
		if attr not in self.__enum_dict:
			raise AttributeError('This object has no attribute %s' %(attr))
		return self.__enum_dict[attr]

	def reverse(self, value):
		for attr in self.__enum_dict:
			if self.__enum_dict[attr] == value:
				return attr
		return None

EffectType = BaseEnumType("""
	Null
	Melee
	MeleeDrain
	Magic
	MagicDrain
	ShiftingDamage
	Spirit
	Armor
	Ward
	ShiftingDefense
	Willpower
	Projection
	Heal
	LifeLose
	ArmorDestroy
	WardDestroy
	WillpowerDestroy
	ExtraAction
	FocusOrProtect
	Stun
	NextMelee
	NextMagic
	OngoingMelee
	OngoingMagic
	Cleanse
	Purge
	Normalize
	Aura
	Bane
	Curse
	Summon
	Effect_After
	Effect_During
""")

PlayerType = BaseEnumType("""
	Random
	Alive
	Dead
	Out_of_Spirit
	Attacker
	Defender
""")

TargetType = BaseEnumType("""
	Null
	Enimy
	Self
	AllAllies
	AllEnimies
	All
	LowestHpEnimy
""")

RuneType = BaseEnumType("""
	Null
	Axe
	Sword
	Mace
	Twinblades
	Spear
	Fist
	Earth
	Shadow
	Holy
	Lighting
	Frost
	Fire
	Spirit
	Armor
	Ward
	Willpower
	Summon
	Buff
	Debuff
	Tech
""")

ConditionType = BaseEnumType("""
	Null
	EndCondition
	BeingTarget
""")

LineType = BaseEnumType("""
	Condition 
	Effect
""")
