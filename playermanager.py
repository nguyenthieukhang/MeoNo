import constants
import network

class PlayerManager:
    def __init__(self, conn):
        self.network = network.Network(conn)
        self.hand = []

    def show_cards(self):
        print('These are your cards:')
        for card in self.hand:
            print(card, end = ' ')
        print()

    def start(self):
        myturn = False

        while True:
            signal = self.network.receive()
            print(signal, 'received')

            if signal == constants.START_YOUR_TURN:
                myturn = True
                print('Start your turn!')

            elif signal == constants.END_YOUR_TURN:
                print('The end of your turn')
                myturn = False

            elif signal == constants.START_NEW_PLAY and myturn:
                number = int(input('Choose a card to play?'))
                self.network.send(number)
                print('Played card', number)

            elif signal == constants.DEAL_CARDS:
                for i in range(constants.START_HAND):
                    self.hand.append(self.network.receive())
                    print('Take the card', self.hand[-1])
                self.show_cards()

            elif signal == constants.ASK_RESPONSE:
                if constants.CARD_NOPE not in self.hand:
                    self.network.send(constants.NO_RESPONSE)
                else:
                    ans = input('Do you want to respond with a Nope?, Enter Y/N?')
                    if ans == 'Y':
                        self.network.send(constants.CARD_NOPE)
                    else:
                        self.network.send(constants.NO_RESPONSE)

            elif signal == constants.SOMEONE_LOSES:
                print('The turn player has lost!')
                continue

            elif signal == constants.DRAW_A_CARD and myturn:
                print('You are drawing a card!')
                card = self.network.receive()
                if card == constants.CARD_BOMB:
                    if constants.CARD_DEFUSE in self.hand:
                        self.hand.remove(constants.CARD_DEFUSE)
                        print('You have drawn a bomb!')
                        pos = int(input('Now enter the position of the bomb into the deck!'))
                        self.network.send(pos)
                self.hand.append(card)
            elif signal == constants.YOU_LOSE and myturn:
                print('You Lose!')
                print('Just wait and see other people playing!')
            else:
                print('Other people play this card:', signal)