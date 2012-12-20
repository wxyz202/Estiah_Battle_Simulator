import random
import copy
from common.alltype import PlayerType
from common.datahandler import loadCharmFromId

class Gear(object):
	def __init__(self, id, charm_list, has_order):
		self.id = id
		self.charm_list = charm_list
		self.has_order = has_order

	def generate_charm_list(self):
		charm_list = []
		gear = copy.deepcopy(self.charm_list)
		if self.has_order:
			i = 0
			while len(charm_list) < 1000:
				if len(gear) == 0:
					break
				charm_list.append(gear[i][0])
				if gear[i][1] == None:
					i+=1
				elif gear[i][1] == 1:
					gear.pop(i)
				else:
					gear[i] = (gear[i][0],gear[i][1]-1)
					i += 1
				if i >= len(gear):
					i = 0
		else:
			if gear[-1][1] is None:
				i = 0
				while gear[i][1] is not None:
					charm_list.append(gear[i][0])
					if gear[i][1] == 1:
						gear.pop(i)
					else:
						gear[i] = (gear[i][0],gear[i][1]-1)
				while len(charm_list) < 1000:
					charm_list.append(random.choice(gear)[0])
			else:
				for i in gear:
					charm_list.extends([i[0]] * i[1])
				random.shuffle(charm_list)
		return charm_list

	def toJsonObj(self):
		charm_list = [{'charm_id': charm.id, 'number': n} for (charm, n) in self.charm_list]
		return {'id': self.id, 'charm_list': charm_list, 'has_order': self.has_order}

	@classmethod
	def fromJsonObj(cls, obj):
		id = obj['id']
		charm_list = obj['charm_list']
		charm_list = [(loadCharmFromId(d['charm_id']), d['number']) for d in charm_list]
		has_order = obj['has_order']
		return cls(id, charm_list, has_order)
