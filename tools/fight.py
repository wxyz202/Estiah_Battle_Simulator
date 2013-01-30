from battle.envioronment import Envioronment
from common.datahandler import *
from common.enumtype import EnvioronmentType
import battlelog

if __name__ == '__main__':
	attacker = load_player_from_id("zgreee")
	defender = load_player_from_id("zgreee3")
	attacker.import_gear(load_gear_from_id("zgreee - auto magic"))
	defender.import_gear(load_gear_from_id("zgreee3 - auto"))
	attackers = [attacker]
	defenders = [defender]
	env = Envioronment(attackers, defenders)
	result = env.start()
	battlelog.log(EnvioronmentType.reverse(result))
