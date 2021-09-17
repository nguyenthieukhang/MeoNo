import card
import constants
import deck
import socket
import struct
import time

class Game:
    class PlayerClient:
        def __init__(self, connection):
            self.hand = []
            self.connection = connection

    def __init__(self, playerconns: list): #players is a list of Network objects
        self.players = []
        self.deck = deck.Deck()
        self.count_player = len(playerconns)
        self.turn_counter = 0
        # self.discard = []
        self.attacked_turn = 1

        for conn in playerconns:
            self.players.append(self.PlayerClient(conn))

    def deal_cards(self):
        self.broadcast(constants.DEAL_CARDS)

        # START BY GIVING THE PLAYERS THE DEFUSES
        for player in self.players:
            print('line 29 game.py')
            player.connection.send(constants.CARD_DEFUSE)
            player.hand.append(constants.CARD_DEFUSE)

        # GIVE THEM THE REMAINING CARDS
        for i in range(constants.START_HAND - 1):
            for player in self.players:
                card = self.deck.take_top()[0]
                player.connection.send(card)
                player.hand.append(card)

        # PUT THE BOMBS INTO THE DECK
        for i in range(len(self.players) - 1):
            self.deck.insert(1, constants.CARD_BOMB)

        print('Dealing cards...')
        time.sleep(10)

    def start(self):
        self.deal_cards()
        print('Start game')
        while len(self.players) > 1:

            curr_player = self.players[self.turn_counter]
            player_lose = False
            attack = False

            while self.attacked_turn > 0:
                curr_player.connection.send(constants.START_YOUR_TURN)

                while True:
                    signal = curr_player.connection.receive()
                    self.broadcast(signal)
                    if signal == constants.END_OF_TURN:
                        player_lose = not self.draw_a_card(curr_player)
                        break
                    else:
                        success = self.ask_response(curr_player, signal)
                        if not success:
                            continue

                        # Resolve the card

                        if signal == constants.CARD_SKIP:
                            break
                        elif signal == constants.CARD_SHUFFLE:
                            self.deck.shuffle()
                            self.broadcast(constants.DECK_SHUFFLED)
                        elif signal == constants.CARD_ATTACK:
                            attack = True
                            break
                        elif signal == constants.CARD_SEE_THE_FUTURE:
                            self.see_the_future(curr_player)
                        elif signal == constants.CARD_FAVOR:
                            self.favor(curr_player)

                if player_lose:
                    self.attacked_turn = 1
                    break

                if attack:
                    self.attacked_turn += constants.ATTACK_POWER
                    break

                self.attacked_turn -= 1


            if player_lose:
                self.turn_counter = self.turn_counter
                self.attacked_turn = 1
            else:
                self.turn_counter = (self.turn_counter + 1) % self.count_player


        print('Game over!')

    def see_the_future(self, curr_player):
        pass

    def favor(self, curr_player):
        pass

    def draw_bomb(self, curr_player):
        if constants.CARD_DEFUSE not in curr_player.hand:
            curr_player.connection.send(constants.YOU_LOSE)
            self.players.remove(curr_player)
            self.broadcast(constants.SOMEONE_LOSES)
            return False
        else:
            self.players[self.turn_counter].hand.remove(constants.CARD_DEFUSE)
            self.discard.append(constants.CARD_DEFUSE)
            bomb_position = curr_player.connection.receive()
            self.deck.insert(bomb_position, constants.CARD_BOMB)
        return True

    def broadcast(self, number: int):
        for player in self.players:
            player.connection.send(number)

    def draw_a_card(self, curr_player):
        curr_player.connection.send(constants.DRAW_A_CARD)
        card = self.deck.take_top()
        curr_player.connection.send(card)
        if card == constants.CARD_BOMB:
            return self.draw_bomb(curr_player)
        else:
            curr_player.hand.append(card)
            return True

    def ask_response(self, curr_player, card) -> bool:
        self.broadcast(constants.ASK_RESPONSE)
        responses = []
        for player in self.players:
            if player != curr_player:
                responses.append((player.connection.receive(), player))

        for response in responses:
            if response[0] == constants.CARD_NOPE:
                for player in self.players:
                    if player == response[1]:
                        player.hand.remove(constants.CARD_NOPE)
                return not self.ask_response(response[1], response[0])

        return True






