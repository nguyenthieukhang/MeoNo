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
        self.discard = []
        self.attacked_turn = 1

        for conn in playerconns:
            self.players.append(self.PlayerClient(conn))

    def deal_cards(self):
        self.broadcast(constants.DEAL_CARDS)
        self.deck.shuffle()

        # START BY GIVING THE PLAYERS THE DEFUSES
        for player in self.players:
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

        self.deck.shuffle()
        print('Dealing cards...')
        time.sleep(5)

    def start(self):
        self.deal_cards()
        print('Start game')
        while len(self.players) > 1:

            curr_player = self.players[self.turn_counter]
            print('Current player is', self.turn_counter)
            player_lose = False
            attack = False

            while self.attacked_turn > 0:
                curr_player.connection.send(constants.START_YOUR_TURN)
                print('Start your turn')

                while True:
                    curr_player.connection.send(constants.START_NEW_PLAY)
                    signal = curr_player.connection.receive()
                    self.broadcast(signal)

                    if signal == constants.END_OF_TURN:
                        player_lose = not self.draw_a_card(curr_player)
                        print('Player has drawn a card')
                        break
                    else:
                        print('Asking for response on', signal, 'from current player')
                        success = self.ask_response(curr_player, signal)
                        if not success:
                            continue
                        print('Card executing...')

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

                        print('Done executing card')

                if player_lose:
                    self.attacked_turn = 1
                    break

                if attack:
                    self.attacked_turn += constants.ATTACK_POWER
                    break

                self.attacked_turn -= 1
                print('attacked_turn = ', self.attacked_turn)

            if player_lose:
                self.turn_counter = self.turn_counter
                self.attacked_turn = 1
            else:
                self.turn_counter = (self.turn_counter + 1) % self.count_player
                if not attack:
                    self.attacked_turn = 1


        print('Game over!')

    def see_the_future(self, curr_player):
        pass

    def favor(self, curr_player):
        pass

    def draw_bomb(self, curr_player):
        print('Player draw a bomb!')
        if constants.CARD_DEFUSE not in curr_player.hand:
            curr_player.connection.send(constants.YOU_LOSE)
            self.players.remove(curr_player)
            self.broadcast(constants.SOMEONE_LOSES)
            print('Player loses!')
            return False
        else:
            self.players[self.turn_counter].hand.remove(constants.CARD_DEFUSE)
            self.discard.append(constants.CARD_DEFUSE)
            bomb_position = curr_player.connection.receive()
            self.deck.insert(bomb_position, constants.CARD_BOMB)
            print('Player escape the bomb')
        return True

    def broadcast(self, number: int):
        for player in self.players:
            player.connection.send(number)

    def draw_a_card(self, curr_player):
        curr_player.connection.send(constants.DRAW_A_CARD)
        card = self.deck.take_top()[0]
        curr_player.connection.send(card)
        if card == constants.CARD_BOMB:
            return self.draw_bomb(curr_player)
        else:
            curr_player.hand.append(card)
            return True

    def ask_response(self, curr_player, card) -> bool:
        print('ask response called')
        self.broadcast(constants.ASK_RESPONSE)
        responses = []
        for player in self.players:
            responses.append((player.connection.receive(), player))

        print('responses:', responses)

        for response in responses:
            if response[0] == constants.CARD_NOPE:
                print('There is card nope!')
                for player in self.players:
                    if player == response[1]:
                        player.hand.remove(constants.CARD_NOPE)
                return not self.ask_response(response[1], response[0])

        return True






