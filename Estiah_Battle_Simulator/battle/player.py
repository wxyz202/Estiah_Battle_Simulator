import random
from common.alltype import PlayerType

class Player(object):
	@staticmethod
	def generate_charm_list(gear, has_order):
		charm_list = []
		if has_order:
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

	def __init__(self, name, max_hp, gear, has_order=False, is_no_dizzy=False):
		self.name = name
		self.max_hp = max_hp
		self.hp = self.max_hp
		self.charm_list = Player.generate_charm_list(gear, has_order)
		self.charm_used = 0
		self.max_spirit = len(charm_list)
		self.spirit = self.max_spirit
		self.turn_list = []
		if is_no_dizzy:
			self.max_dizzy_turn = 1000
		else:
			self.max_dizzy_turn = 4
		self.alive_type = PlayerType.Alive
		self.reset()

	def reset(self):
		self.Melee_CPB = 0
		self.Melee_NPB = 0
		self.Magic_CPB = 0
		self.Magic_NPB = 0
		self.Spirit_CPB = 0
		self.Spirit_NPB = 0
		self.Armor = 0
		self.Ward = 0
		self.Willpower = 0
		self.effect_list = []
		self.is_being_target_turn = 0
		self.stun_turn = 0

	def cleanse(self):
		self.effect_list = [e for e in self.effect_list if not isinstance(e, Bane)]
		self.Melee_CPB = max(0, self.Melee_CPB)
		self.Melee_NPB = max(0, self.Melee_NPB)
		self.Magic_CPB = max(0, self.Magic_CPB)
		self.Magic_NPB = max(0, self.Magic_NPB)
		self.Spirit_CPB = max(0, self.Spirit_CPB)
		self.Spirit_NPB = max(0, self.Spirit_NPB)
		return

	def purge(self):
		self.effect_list = [e for e in self.effect_list if not isinstance(e, Aura)]
		self.Melee_CPB = min(0, self.Melee_CPB)
		self.Melee_NPB = min(0, self.Melee_NPB)
		self.Magic_CPB = min(0, self.Magic_CPB)
		self.Magic_NPB = min(0, self.Magic_NPB)
		self.Spirit_CPB = min(0, self.Spirit_CPB)
		self.Spirit_NPB = min(0, self.Spirit_NPB)
		return

	def normalize(self):
		self.Melee_CPB = 0
		self.Melee_NPB = 0
		self.Magic_CPB = 0
		self.Magic_NPB = 0
		self.Spirit_CPB = 0
		self.Spirit_NPB = 0
		return

	def die(self):
		self.alive_type = PlayerType.Dead
		self.reset()

	def outOfSpirit(self):
		self.alive_type = PlayerType.Out_of_Spirit

	def isAlive(self):
		return self.alive_type == PlayerType.Alive

	def reduceHp(self, hp):
		if self.hp > hp:
			self.hp -= hp
		else:
			self.hp = 0
			self.die()

	def increaseHp(self, hp):
		self.hp = max(self.hp+hp, self.max_hp)

	def reduceSpirit(self, spirit):
		if self.spirit > spirit:
			self.spirit -= spirit
		else:
			self.spirit = 0
			self.outOfSpirit()

	def playCharm(self, enimy, allies, enimies, turn):
		if self.stun_turn > 0:
			self.turn_list.append((turn, [charms.NullCharm]))
			self.stun_turn -= 1
			return False
		charm = self.charm_list[self.charm_used]
		self.charm_used += 1
		if len(self.turn_list = []) or self.turn_list[-1][0] != turn:
			self.turn_list.append((turn, [charm]))
		else:
			self.turn_list[-1][1].append(charm)
		is_EA = charm.run(self, enimy, allies, enimies)
		return is_EA

	def triggerEffects(self, allies, enimies, is_EA):
		for effect in effect_list:
			effect.run(self, None, allies, enimies, is_EA)