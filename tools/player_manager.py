from battle.player import Player
from common.datahandler import *

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
