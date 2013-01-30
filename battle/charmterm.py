import random
import targeting
from common.enumtype import TargetType, CharmTermType, EffectParamType
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
		for target in target_list:
			effect_param_type = effect.needed_param()
			if effect_param_type == EffectParamType.All_Multiplier:
				effect.execute(subject, target, base_multiplier, CPB_multiplier, NPB_multiplier, total_booster_multiplier)
			elif effect_param_type == EffectParamType.Base_Multiplier:
				effect.execute(subject, target, base_multiplier)
			elif effect_param_type == EffectParamType.All_Party:
				effect.execute(subject, target, allies, enimies)
			elif effect_param_type == EffectParamType.Normal:
				effect.execute(subject, target)
			else:
				assert False
		subject.check_melee_NPB()
		subject.check_magic_NPB()
		subject.check_spirit_NPB()

	def is_extra_action(self):
		if len(self.effect_target_list) != 1:
			return False
		effect, target = self.effect_target_list[0]
		from effect import ExtraAction
		return isinstance(effect, ExtraAction)

	def to_json_obj(self):
		obj = {'charm_term_type': CharmTermType.reverse(CharmTermType.EffectTerm)}
		obj['charm_term'] = [{'effect': effect.to_json_obj(), 'target': TargetType.reverse(target)} for effect, target in self.effect_target_list]
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		from effect import Effect
		effect_target_list = [(Effect.from_json_obj(effect_target['effect']), getattr(TargetType, effect_target['target'])) for effect_target in obj]
		return cls(effect_target_list)
