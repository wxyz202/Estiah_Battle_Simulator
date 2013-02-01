from battle.player import Player
from common.datahandler import DataHandler

if __name__ == '__main__':
	
	def test_add_player(player):
		players = DataHandler.load_players()
		if player.id not in players:
			players[player.id] = player.to_json_obj()
		DataHandler.save_players(players)

	player1 = Player(
		id = "zgreee3",
		name = "zgreee3",
		level = 35,
		max_hp = 673
	)

	player2 = Player(
		id = "zgreee",
		name = "zgreee",
		level = 35,
		max_hp = 664
	)

	player3 = Player(
		id = "Salabajzer",
		name = "Salabajzer",
		level = 35,
		max_hp = 652
	)

	test_add_player(player1)
	test_add_player(player2)
	test_add_player(player3)
