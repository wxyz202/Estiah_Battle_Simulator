from common.alltype import ConditionType

class Condition(object):
	pass

class NullCondition(Condition):
	def check(self, player):
		return True

class BeingTargetCondition(Condition):
	def check(self, player):
		return player.is_being_target_turn > 0

class EndCondition(Condition):
	pass