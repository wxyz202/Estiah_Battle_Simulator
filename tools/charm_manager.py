from common.enumtype import TargetType, RuneType, EffectType
from common.datahandler import *
from battle.charm import *
from battle.charmterm import *
from battle.effect import *

if __name__ == '__main__':

	def test_charm(charm):
		x=charm.to_json_obj()
		y=Charm.from_json_obj(x)
		z=y.to_json_obj()
		print x==z


	def test_add_charm(charm):
		charms = load_charms()
		if charm.id not in charms:
			charms[charm.id] = charm.to_json_obj()
		save_charms(charms)
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
					name = "Burn",
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
					name = "Burn",
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
					name = "Consume",
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



	for i in xrange(1, 16):
		charm = globals()['charm%d' %(i)]
		test_charm(charm)
		test_add_charm(charm)

