import constants
import network

class PlayerInterface:
    def __init__(self, network: network.Network):
        self.hand = []
        self.network = network

    def show_cards(self):
        print('This is your hand')
        for card in self.hand:
            print(card, end = ' ')
        print()

    def choose_card(self) -> int:
        ind = int(input('Choose the card number or enter -1 to end the playing phase'))
        if ind == -1:
            return constants.END_OF_TURN
        while ind >= len(self.hand) or ind < 0:
            ind = int(input('You enter the wrong index. Please try again!'))
        card_played = self.hand.pop(ind)
        print('You play the card', card_played)
        return card_played

    def draw(self):
        drawn_card = self.network.receive()
        self.hand.append(drawn_card)

    def play(self):
        while len(self.hand) > 0:
            card_played = self.choose_card()
            self.network.send(card_played)
            signal = self.network.receive()
            if signal == constants.DRAW_A_CARD:
                self.draw()
                break


