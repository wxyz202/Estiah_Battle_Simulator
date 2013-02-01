from common.enumtype import TargetType, RuneType, EffectType
from common.datahandler import DataHandler
from battle.charm import *
from battle.charmterm import *
from battle.effect import *

if __name__ == '__main__':

	def test_charm(charm):
		x=charm.to_json_obj()
		y=Charm.from_json_obj(x)
		z=y.to_json_obj()
		print charm.id, x==z


	def test_add_charm(charm):
		charms = DataHandler.load_charms()
		if charm.id not in charms:
			charms[charm.id] = charm.to_json_obj()
		DataHandler.save_charms(charms)
		return


	charm1 = Charm(
		id = '668',
		name = 'Blue Dragon Bone',
		rune1 = RuneType.Tech,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(ExtraAction(1), TargetType.Self)]),
			EffectTerm([(WardDestroy(30), TargetType.Self)]),
			EffectTerm([(NextMagic(18), TargetType.Self)])
		]
	)

	charm2 = Charm(
		id = '610',
		name = 'Hastened Blast',
		rune1 = RuneType.Tech,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(ExtraAction(1), TargetType.Self)]),
			EffectTerm([(Spirit(1), TargetType.Self)]),
			EffectTerm([(Magic(18), TargetType.Enimy)])
		]
	)

	charm3 = Charm(
		id = '968',
		name = 'Shaman Inner Flames',
		rune1 = RuneType.Tech,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(25, 20), TargetType.Enimy)]),
			EffectTerm([(
				Attach(Bane(
					name = 'Shaman Inner Flames',
					description = "Burn",
					turn = 5,
					long_time_type = EffectType.AttachmentDuring,
					attach_charm = AttachCharm(
						charm_terms = [
							EffectTerm([(Magic(7,40), TargetType.Enimy)])
						]
					)
				)),
				TargetType.Enimy
			)])
		]
	)

	charm4 = Charm(
		id = '973',
		name = 'Shaman Voltage',
		rune1 = RuneType.Tech,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(28, 20), TargetType.Enimy)]),
			EffectTerm([(
				Attach(Bane(
					name = 'Shaman Voltage',
					description = "Burn",
					turn = 5,
					long_time_type = EffectType.AttachmentDuring,
					attach_charm = AttachCharm(
						charm_terms = [
							EffectTerm([(Magic(8,40), TargetType.Enimy)])
						]
					)
				)),
				TargetType.Enimy
			)])
		]
	)

	charm5 = Charm(
		id = '1057',
		name = "Thor's Fist",
		rune1 = RuneType.Mace,
		rune2 = RuneType.Lightning,
		charm_terms = [
			EffectTerm([(ShiftingDamage(45), TargetType.Enimy)])
		]
	)

	charm6 = Charm(
		id = '1077',
		name = "Challenger's Aquatic Ring",
		rune1 = RuneType.Frost,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(41, 32), TargetType.Enimy)])
		]
	)

	charm7 = Charm(
		id = '1108',
		name = "Demon Heart",
		rune1 = RuneType.Frost,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(53, 15), TargetType.Enimy)])
		]
	)

	charm8 = Charm(
		id = '1221',
		name = "Superior Fire Oil",
		rune1 = RuneType.Buff,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(OngoingMagic(13), TargetType.Self)]),
			EffectTerm([(
				Attach(Curse(
					name = "Superior Fire Oil",
					description = "Consume",
					turn = 6,
					long_time_type = EffectType.AttachmentDuring,
					attach_charm = AttachCharm(
						charm_terms = [
							EffectTerm([(WardDestroy(10), TargetType.Self)])
						]
					)
				)),
				TargetType.Self
			)])
		]
	)

	charm9 = Charm(
		id = '1496',
		name = 'Icy Winds',
		rune1 = RuneType.Frost,
		rune2 = RuneType.Buff,
		charm_terms = [
			EffectTerm([(ExtraAction(1), TargetType.Self)]),
			EffectTerm([(OngoingMagic(5), TargetType.Self)]),
			EffectTerm([(LifeLose(5), TargetType.Self)])
		]
	)

	charm10 = Charm(
		id = "940",
		name = "Wizard Shadow Bone",
		rune1 = RuneType.Shadow,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(WardDestroy(21), TargetType.Enimy)]),
			EffectTerm([(Magic(51, 0), TargetType.Enimy)]),
			EffectTerm([(LifeLose(5), TargetType.Self)])
		]
	)

	charm11 = Charm(
		id = "1074",
		name = "Challenger's Darkening Ring",
		rune1 = RuneType.Shadow,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(WardDestroy(21), TargetType.Enimy)]),
			EffectTerm([(Magic(50, 0), TargetType.Enimy)])
		]
	)

	charm12 = Charm(
		id = "344",
		name = "Lightning Reflexes",
		rune1 = RuneType.Lightning,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(ExtraAction(1), TargetType.Self)]),
			EffectTerm([(Magic(6, 25), TargetType.Enimy)])
		]
	)

	charm13 = Charm(
		id = "947",
		name = "Wizard Fire Orb",
		rune1 = RuneType.Fire,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(61, 0), TargetType.Enimy)]),
			EffectTerm([(LifeLose(6), TargetType.Self)])
		]
	)

	charm14 = Charm(
		id = "1078",
		name = "Challenger's Pyric Ring",
		rune1 = RuneType.Fire,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(54, 0), TargetType.Enimy)])
		]
	)

	charm15 = Charm(
		id = "942",
		name = "Wizard Burning Toss",
		rune1 = RuneType.Fire,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(56, 0), TargetType.Enimy)]),
			EffectTerm([(LifeLose(5), TargetType.Self)])
		]
	)

	charm16 = Charm(
		id = "1540",
		name = "Flame Scabbard",
		rune1 = RuneType.Fire,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(28, 0), TargetType.Enimy)]),
			EffectTerm([(NextMagic(23), TargetType.Self)])
		]
	)

	charm17 = Charm(
		id = "1541",
		name = "Ice Scabbard",
		rune1 = RuneType.Frost,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Magic(23, 38), TargetType.Enimy)]),
			EffectTerm([(OngoingMagic(5), TargetType.Self)])
		]
	)

	charm18 = Charm(
		id = "865",
		name = "Night Cloak",
		rune1 = RuneType.Buff,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(ExtraAction(1), TargetType.Self)]),
			EffectTerm([(OngoingMelee(5), TargetType.Self)]),
			EffectTerm([(LifeLose(5), TargetType.Self)])
		]
	)

	charm19 = Charm(
		id = "900",
		name = "Honor Mace",
		rune1 = RuneType.Mace,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Melee(46, 0), TargetType.Enimy)])
		]
	)

	charm20 = Charm(
		id = "903",
		name = "Honor Gauntlets",
		rune1 = RuneType.Fist,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(ArmorDestroy(22), TargetType.Enimy)]),
			EffectTerm([(Melee(40, 0), TargetType.Enimy)])
		]
	)

	charm21 = Charm(
		id = "983",
		name = "Guard Strategic Hit",
		rune1 = RuneType.Tech,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Melee(25, 0), TargetType.Enimy)]),
			EffectTerm([(Armor(47, True), TargetType.Self)])
		]
	)

	charm22 = Charm(
		id = "986",
		name = "Guard Thorned Mace",
		rune1 = RuneType.Mace,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Melee(28, 0), TargetType.Enimy)]),
			EffectTerm([(Projection(42, EffectType.Melee, EffectType.Armor), TargetType.Enimy)])
		]
	)

	charm23 = Charm(
		id = "987",
		name = "Guard Sting",
		rune1 = RuneType.Spear,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Melee(21, 15), TargetType.Enimy)]),
			EffectTerm([(Projection(42, EffectType.Melee, EffectType.Armor), TargetType.Enimy)]),
			EffectTerm([(Armor(17, True), TargetType.Self)])
		]
	)

	charm24 = Charm(
		id = "988",
		name = "Guard Strategic Strike",
		rune1 = RuneType.Tech,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(Melee(28, 0), TargetType.Enimy)]),
			EffectTerm([(Armor(51, True), TargetType.Self)])
		]
	)

	charm25 = Charm(
		id = '1054',
		name = "Invoke Defender",
		rune1 = RuneType.Buff,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(
				Attach(Summon(
					name = "Invoke Defender",
					description = "Defender",
					turn = 10,
					long_time_type = EffectType.AttachmentDuring,
					attach_charm = AttachCharm(
						charm_terms = [
							EffectTerm([(Armor(14, True), TargetType.Self), (Ward(14, True), TargetType.Self)])
						]
					)
				)),
				TargetType.Self
			)])
		]
	)

	charm26 = Charm(
		id = '1060',
		name = "Release Seal",
		rune1 = RuneType.Buff,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(LifeLose(11), TargetType.Self)]),
			EffectTerm([(Willpower(2, False), TargetType.Self)]),
			EffectTerm([(
				Attach(Aura(
					name = "Release Seal",
					description = "Releasing seal",
					turn = 4,
					long_time_type = EffectType.AttachmentAfter,
					attach_charm = AttachCharm(
						charm_terms = [
							EffectTerm([(NextMelee(72), TargetType.Self)])
						]
					)
				)),
				TargetType.Self
			)])
		]
	)

	charm27 = Charm(
		id = "1923",
		name = "Luminous Idea",
		rune1 = RuneType.Willpower,
		rune2 = RuneType.Null,
		charm_terms = [
			EffectTerm([(ExtraAction(1), TargetType.Self)]),
			EffectTerm([(Willpower(2, True), TargetType.Self)])
		]
	)



	for i in xrange(1, 28):
		charm = globals()['charm%d' %(i)]
		test_charm(charm)
		test_add_charm(charm)

