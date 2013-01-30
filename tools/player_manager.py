from battle.player import Player
from common.datahandler import *

if __name__ == '__main__':
	
	def test_add_player(player):
		players = load_players()
		if player.id not in players:
			players[player.id] = player.to_json_obj()
		save_players(players)

	player1 = Player(
		id = "zgreee3",
		name = "zgreee3",
		level = 34,
		max_hp = 655
	)

	player2 = Player(
		id = "zgreee",
		name = "zgreee",
		level = 34,
		max_hp = 646
	)

	test_add_player(player1)
	test_add_player(player2)
