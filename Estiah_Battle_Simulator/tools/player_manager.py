import json
from battle.player import Player

def loadPlayers():
	f = open('data/players.json')
	players = json.load(f)
	f.close()
	return players

def savePlayers(players):
	f = open('data/players.json', 'w')
	json.dump(players, f, indent=4, sort_keys=True)
	f.close()
	return

def loadPlayer(player_id):
	players = loadPlyers()
	return Plyaer.fromJsonObj(players[player_id])

if __name__ == '__main__':
	
	def testAddPlayer():
		players = loadPlayers()
		def addPlayer(player):
			if player.id not in players:
				players[player.id] = player.toJsonObj()
			return
		addPlayer(Player('Hamster', 'Hamster', 1, 4, False))
		addPlayer(Player('Mouse', 'Mouse', 1, 6, False))
		addPlayer(Player('wii03', 'wii03', 11, 115, False))
		savePlayers(players)


	testAddPlayer()
