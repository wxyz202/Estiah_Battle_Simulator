import random
from common.enumtype import TargetType, RuneType, CharmTermType
from charmterm import *
import constants

class BaseCharm(object):
	def execute(self, subject, allies, enimies):
		target = targeting.choose_enimy(enimies)
		state_stack = []
		special_target = TargetType.Null
		condition_satisfy = True
		multiplier = 1
		for term in self.charm_terms:
			if isinstance(term, EffectTerm):
				if condition_satisfy:
					self.execute_effect(term, subject, target, allies, enimies, special_target, multiplier)
			elif isinstance(term, ChangeTargetTerm):
				state_stack.append((special_target, condition_satisfy, multiplier))
				if condition_satisfy:
					special_target = term.change_target()
			elif isinstance(term, ConditionTerm):
				state_stack.append((special_target, condition_satisfy, multiplier))
				if condition_satisfy:
					condition_satisfy = term.check(subject, target, allies, enimies, special_target)
			elif isinstance(term, EndTerm):
				special_target, condition_satisfy, multiplier = state_stack.pop()
			else:
				assert False


class Charm(BaseCharm):
	def __init__(self, id, name, rune1, rune2, charm_terms):
		self.id = id
		self.name = name
		self.rune1 = rune1
		self.rune2 = rune2
		self.charm_terms = charm_terms

	def is_extra_action(self):
		condition_cnt = 0
		for term in self.charm_terms:
			if isinstance(term, EffectTerm):
				if condition_cnt != 0:
					continue
				if term.is_extra_action():
					return True
			elif isinstance(term, ChangeTargetTerm) or isinstance(term, ConditionTerm):
				condition_cnt += 1
			elif isinstance(term, EndTerm):
				condition_cnt -= 1
			else:
				assert False
		return False

	def execute_effect(self, term, subject, target, allies, enimies, special_target, multiplier):
		if self.is_extra_action():
			term.execute(subject, target, allies, enimies, special_target, base_multiplier = multiplier, CPB_multiplier = constants.EXTRA_ACTION_CPB_MULTIPLIER)
		else:
			term.execute(subject, target, allies, enimies, special_target, base_multiplier = multiplier)

	def to_json_obj(self):
		obj = {
			'id': self.id,
			'name': self.name,
			'rune1': RuneType.reverse(self.rune1),
			'rune2': RuneType.reverse(self.rune2),
			'charm_terms': []
		}
		for term in self.charm_terms:
			obj['charm_terms'].append(term.to_json_obj())
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		id = obj['id']
		name = obj['name']
		rune1 = getattr(RuneType, obj['rune1'])
		rune2 = getattr(RuneType, obj['rune2'])
		charm_terms = []
		for term in obj['charm_terms']:
			charm_terms.append(CharmTerm.from_json_obj(term))
		return cls(id, name, rune1, rune2, charm_terms)

class AttachCharm(BaseCharm):
	def __init__(self, charm_terms):
		self.charm_terms = charm_terms

	def execute_effect(self, term, subject, target, allies, enimies, special_target, multiplier):
		if special_target == TargetType.Null and self.source.is_affect_attach_target():
			target = self.source.target
		self.source.trigger_log()
		term.execute(subject, target, allies, enimies, special_target, base_multiplier = multiplier, CPB_multiplier = 0, NPB_multiplier = 0, total_booster_multiplier = 0)

	def to_json_obj(self):
		obj = {
			'charm_terms': []
		}
		for term in self.charm_terms:
			obj['charm_terms'].append(term.to_json_obj())
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		charm_terms = []
		for term in obj['charm_terms']:
			charm_terms.append(CharmTerm.from_json_obj(term))
		return cls(charm_terms)

