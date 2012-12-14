import random
from common.alltype import TargetType, RuneType, LineType
from effect import Effect
import targeting

class RandomEffectLine(object):
	def __init__(self, effect_target_list):
		self.effect_target_list = effect_target_list
	
	def choice(self):
		return random.choice(self.effect_target_list)

	def toJsonObj(self):
		obj = {'line_type': LineType.reverse(LineType.Effect)}
		obj['effects'] = [{'effect': effect.toJsonObj(), 'target': TargetType.reverse(target)} for effect, target in self.effect_target_list]
		return obj

	@classmethod
	def fromJsonObj(obj):
		effect_target_list = [(Effect.fromJsonObj(effect_target['effect']), getattr(TargetType, effect_target['target'])) for effect_target in obj]
		return cls(effect_target_list)

class Charm(object):
	def __init__(self, id, name, rune1, rune2, lines, is_attachment):
		self.id = id
		self.name = name
		self.rune1 = rune1
		self.rune2 = rune2
		self.lines = lines
		self.is_attachment = is_attachment


	def is_EA(self):
		for line in self.lines:
			if isinstance(line, Condition):
				continue
			if isinstance(line, RandomEffectLine):
				continue
			effect, target = line
			if isinstance(effect, ExtraAction) and condition is None:
				return True
		return False

	def run(self, subject, enimy, allies, enimies):
		if enimy is None:
			enimy = target.chooseRandomEnimy(enimies)
		has_EA = False
		cond_stack = []
		cond_flag = True
		for line in self.lines:
			if isinstance(line, Condition):
				if isinstace(line, EndCondition):
					cond_flag = cond_stack.pop(-1)
				else:
					flag = line.check()
					cond_stack.append(cond_flag)
					cond_flag = cond_flag and flag
			else:
				if not cond_flag:
					continue
				effect, target = line.choice()
				if isinstance(effect, ExtraAction):
					has_EA = True
					continue
				if target == TargetType.Enimy:
					effect.run(subject, enimy, is_EA=self.is_EA(), is_attachment=self.is_attachment)
				elif target == TargetType.Self:
					effect.run(subject, subject, is_EA=self.is_EA(), is_attachment=self.is_attachment)
				elif target == TargetType.AllAllies:
					for player in allies:
						if player.isAlive():
							effect.run(subject, player, is_EA=self.is_EA(), is_attachment=self.is_attachment, AOE_players=len([p for p in allies if p.isAlive()]))
				elif target == TargetType.AllEnimies:
					for player in enimies:
						if player.isAlive():
							effect.run(subject, player, is_EA=self.is_EA(), is_attachment=self.is_attachment, AOE_players=len([p for p in enimies if p.isAlive()]))
				elif target == TargetType.All:
					for player in allies + enimies:
						if player.isAlive():
							effect.run(subject, player, is_EA=self.is_EA(), is_attachment=self.is_attachment, AOE_players=len([p for p in allies + enimies if p.isAlive()]))
				elif target == TargetType.LowestHpEnimy:
					effect.run(subject, target.chooseLowestHpEnimy(enimies), is_EA=self.is_EA(), is_attachment=self.is_attachment)
				else:
					assert False
		return has_EA

	def toJsonObj(self):
		obj = {
			'id': self.id,
			'name': self.name,
			'rune1': RuneType.reverse(self.rune1),
			'rune2': RuneType.reverse(self.rune2),
			'is_attachment': self.is_attachment,
			'lines': []
		}
		for line in self.lines:
			obj['lines'].append(line.toJsonObj())
		return obj

	@classmethod
	def fromJsonObj(obj):
		id = obj['id']
		name = obj['name']
		rune1 = getattr(RuneType, obj['rune1'])
		rune2 = getattr(RuneType, obj['rune2'])
		is_attachment = obj['is_attachment']
		lines = []
		for l in obj['lines']:
			if getattr(LineType, l['line_type']) == LineType.Effect:
				lines.append(RandomEffectLine.fromJsonObj(l['effects']))
			else:
				lines.append(Condition.fromJsonObj(l['condition']))
		return cls(id, name, rune1, rune2, lines, is_attachment)

NullCharm = Charm(None, None, None, None, [], False)
