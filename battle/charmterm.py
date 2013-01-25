import targeting
from common.enumtype import TargetType, CharmTermType
import constants

class CharmTerm(object):
	@staticmethod
	def from_json_obj(obj):
		charm_term_type = obj['charm_term_type']
		charm_term = obj['charm_term']
		return globals()[charm_term_type].from_json_obj(charm_term)

class EffectTerm(CharmTerm):
	def __init__(self, effect_target_list):
		self.effect_target_list = effect_target_list
	
	def choice(self):
		return random.choice(self.effect_target_list)

	def choose_effect_target(self, subject, target, allies, enimies, special_target):
		if special_target == TargetType.Null:
			target_dict = {
				TargetType.Self: [subject],
				TargetType.Enimy: [target]
			}
			effect, target = self.choice()
			target_list = target_dict[target]
		else:
			effect, target = self.choice()
			if special_target == TargetType.All_Allies:
				target_list = allies
			elif special_target == TargetType.All_Enimies:
				target_list = enimies
			elif special_target == TargetType.All:
				target_list = allies + enimies
			elif special_target == TargetType.Lowest_Hp_Enimy:
				target_list = targeting.choose_lowest_hp(enimies)
			else:
				assert False
		return effect, target_list

	def execute(self, subject, target, allies, enimies, special_target, base_multiplier, CPB_multiplier=1, NPB_multiplier=1, total_booster_multiplier=1):
		effect, target_list = self.choose_effect_target(subject, target, allies, enimies, special_target)
		if len(target_list) > 1:
			total_booster_multiplier *= (constants.AOE_BOOSTER_MULTIPLIER) / len(target_list)
		else:
			total_booster_multiplier *= 1
		from effect import *
		for target in target_list:
			if isinstance(effect, Damage):
				effect.execute(subject, target, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
			elif isinstance(effect, FocusProtect) or isinstance(effect, BreakFocus):
				effect.execute(subject, target, allies, enimies)
			elif isinstance(effect, Projection):
				effect.execute(subject, target)
			else:
				effect.execute(subject, target, base_multiplier)
		subject.check_melee_NPB()
		subject.check_magic_NPB()
		subject.check_spirit_NPB()
				

	def to_json_obj(self):
		obj = {'charm_term_type': CharmTermType.reverse(CharmTermType.EffectTerm)}
		obj['charm_term'] = [{'effect': effect.to_json_obj(), 'target': TargetType.reverse(target)} for effect, target in self.effect_target_list]
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		from effect import Effect
		effect_target_list = [(Effect.from_json_obj(effect_target['effect']), getattr(TargetType, effect_target['target'])) for effect_target in obj]
		return cls(effect_target_list)
