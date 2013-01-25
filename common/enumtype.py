class BaseEnumType(object):
	def __init__(self, elements):
		elements = elements.split()
		self._enum_dict = dict(zip(elements, range(len(elements))))

	def __getattr__(self, attr):
		if attr not in self._enum_dict:
			raise AttributeError('This object has no attribute %s' %(attr))
		return self._enum_dict[attr]

	def reverse(self, value):
		for attr in self._enum_dict:
			if self._enum_dict[attr] == value:
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
	FocusProtect
	BreakFocus
	Vanish
	Stun
	NextMelee
	NextMagic
	NextSpirit
	OngoingMelee
	OngoingMagic
	OngoingSpirit
	Cleanse
	Purge
	Normalize
	Attach
	Aura
	Bane
	Curse
	Summon
	AttachmentAfter
	AttachmentDuring
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
	Self
	Enimy
	All_Allies
	All_Enimies
	All
	Lowest_Hp_Enimy
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
	End_Condition
	Being_Target
""")

CharmTermType = BaseEnumType("""
	Condition 
	ChangeTarget
	ForEachMultiplier
	ConsumeMultiplier
	Effect
	End
""")

EnvioronmentType = BaseEnumType("""
	Win
	Lose
""")
