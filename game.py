import card
import constants
import deck
import socket
import struct

class Game:
    class PlayerClient:
        def __init__(self, connection):
            self.hand = []
            self.connection = connection

    def __init__(self, playerconns: list): #players is a list of Network object
        self.players = []
        self.deck = deck.Deck()
        self.count_player = len(playerconns)
        self.turn_counter = 0
        self.discard = []

        for conn in playerconns:
            self.players.append(self.PlayerClient(conn))

        self.deal_cards()

    def deal_cards(self):
        pass

    def start(self):
        while len(self.players) > 1:
            curr_player = self.players[self.turn_counter]

            #Starting the protocol
            curr_player.connection.send(constants.START_YOUR_TURN)
            someonelose = False

            while True:
                signal = curr_player.connection.receive()
                if signal == constants.END_OF_PLAYING:
                    card = self.deck.take_top()
                    curr_player.connection.send(card)

                    if card == constants.CARD_BOMB:
                        if constants.CARD_DEFUSE not in curr_player.hand:
                            curr_player.connection.send(constants.YOU_LOSE)
                            self.players.remove(curr_player)
                            someonelose = True
                            for player in self.players:
                                player.connection.send(constants.SOMEONE_LOSES)
                        else:
                            self.players[self.turn_counter].hand.remove(constants.CARD_DEFUSE)
                            self.discard.append(constants.CARD_DEFUSE)
                            bomb_position = curr_player.connection.receive()
                            self.deck.insert(bomb_position, constants.CARD_BOMB)

                    break
                elif signal == constants.CARD_SKIP:
                    break
                elif signal == constants.CARD_SHUFFLE:
                    self.deck.shuffle()
                elif signal == constants.CARD_SEE_THE_FUTURE:
                    cards = self.deck.see_top(constants.SEE_THE_FUTURE_NUM)
                    for card in cards:
                        curr_player.connection.send(card)

            if not someonelose:
                self.turn_counter = (self.turn_counter + 1) % self.count_player


