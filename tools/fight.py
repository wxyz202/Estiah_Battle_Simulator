from battle.envioronment import Envioronment
from common.datahandler import *
from common.enumtype import EnvioronmentType
import battlelog

if __name__ == '__main__':
	attacker = load_player_from_id("zgreee3")
	defender = load_player_from_id("zgreee")
	attacker.import_gear(load_gear_from_id("zgreee3 - auto"))
	defender.import_gear(load_gear_from_id("zgreee - auto magic"))
	attackers = [attacker]
	defenders = [defender]
	env = Envioronment(attackers, defenders)
	result = env.start()
	battlelog.log(EnvioronmentType.reverse(result))
