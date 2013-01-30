import random
import copy
from common.enumtype import PlayerType
from common.datahandler import load_charm_from_id

class Gear(object):
	def __init__(self, id, gear):
		self.id = id
		self.gear = gear

	def generate_charm_list(self):
		spirit = sum([num for (charm, num) in self.gear])
		def gen(gear):
			charm_list = []
			for (charm, num) in gear:
				charm_list.extend([copy.deepcopy(charm) for i in xrange(num)])
			random.shuffle(charm_list)
			for charm in charm_list:
				yield charm
		return gen(self.gear), spirit

	def to_json_obj(self):
		gear = [{'charm_id': charm.id, 'number': num} for (charm, num) in self.gear]
		obj = {
			'id': self.id,
			'gear': gear
		}
		return obj

	@classmethod
	def from_json_obj(cls, obj):
		id = obj['id']
		gear = obj['gear']
		gear = [(load_charm_from_id(charm['charm_id']), charm['number']) for charm in gear]
		return cls(id, gear)

	@classmethod
	def from_string(cls, s):
		id = s.split("#")[0]
		gear = []
		for charms in s.split("#")[1].split():
			num, charm_id = charms.split("x")
			from common.datahandler import load_charm_from_id
			gear.append((load_charm_from_id(charm_id), int(num)))
		return cls(id, gear)
