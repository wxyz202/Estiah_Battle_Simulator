from battle.envioronment import Envioronment
from battle.gear import Gear
from common.datahandler import DataHandler
from common.enumtype import EnvioronmentType
import battlelog

simulating_times = 1000
name1 = "zgreee"
name2 = "zgreee3"
name3 = "Salabajzer"
gear1 = "zgreee - 1#3x668 5x610 5x968 5x973 5x1057 5x1077 5x1108 5x1221 5x1496"
gear2 = "zgreee3 - 1#5x668 5x940 5x1074 5x1221 5x344 5x947 5x1078 5x942"
gear3 = "zgreee - 2#5x668 3x610 5x968 5x973 5x1057 5x1221 5x1108 5x1496 5x1541"
gear4 = "zgreee3 - 2#5x668 5x940 5x1074 5x1221 5x344 5x947 5x1078 5x942 5x1540"
gear5 = "Salabajzer#5x865 5x900 5x903 5x983 5x986 5x987 5x988 5x1054 5x1060 5x1923"

def test_vs(name1, gear1, name2, gear2):
	battlelog.log_close()
	player1_win_cnt = 0
	player2_win_cnt = 0
	for cnt in xrange(simulating_times):
		if cnt == 0:
			battlelog.log_open()
		else:
			battlelog.log_close()
		player1 = DataHandler.load_player_from_id(name1)
		player2 = DataHandler.load_player_from_id(name2)
		player1.import_gear(Gear.from_string(gear1))
		player2.import_gear(Gear.from_string(gear2))
		attackers = [player1]
		defenders = [player2]
		env = Envioronment(attackers, defenders)
		result = env.start()
		if result == EnvioronmentType.Win:
			player1_win_cnt += 1
		else:
			player2_win_cnt += 1
	battlelog.log_open()
	battlelog.log("%s vs %s, total %d times: %s win probability = %f%%, %s win probability = %f%%\n" %(player1.name, player2.name, simulating_times, player1.name, float(player1_win_cnt*100)/simulating_times, player2.name, float(player2_win_cnt*100)/simulating_times))

def test_double_vs(name1, gear1, name2, gear2):
	test_vs(name1, gear1, name2, gear2)
	test_vs(name2, gear2, name1, gear1)

if __name__ == '__main__':
	test_double_vs(name1, gear1, name3, gear5)

