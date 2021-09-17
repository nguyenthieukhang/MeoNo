import random

import constants


class Deck:
    def __init__(self):
        self.cards = self.basic_deck()

    def shuffle(self):
        random.shuffle(self.cards)

    def see_top(self, count = 1):
        if count > len(self.cards):
            return []
        ret = self.cards[-count:]
        return ret

    def see_bottom(self, count = 1):
        if count > len(self.cards):
            return []
        ret = self.cards[0:count]
        return ret

    def take_top(self, count = 1):
        if count > len(self.cards):
            return []
        ret = self.cards[-count:]
        self.cards = self.cards[:len(self.cards) - count]
        return ret

    def take_bottom(self, count = 1):
        if count > len(self.cards):
            return []
        ret = self.cards[0:count]
        self.cards = self.cards[count:]
        return ret

    def insert(self, position: int, card: int):
        try:
            self.cards.insert(len(self.cards) - position + 1, card)
        except Exception as e:
            print(str(e))

    def basic_deck(self)-> list:
        return [constants.CARD_DEFUSE]*2 + [constants.CARD_SKIP]*4 + [constants.CARD_ATTACK]*4 + [constants.CARD_SEE_THE_FUTURE]*5 + [constants.CARD_NOPE]*5 + [constants.CARD_SHUFFLE]*4 + [constants.CARD_USELESS_CAT_1]*4 + [constants.CARD_USELESS_CAT_2]*4 + [constants.CARD_USELESS_CAT_3]*4 + [constants.CARD_USELESS_CAT_4]*4 + [constants.CARD_USELESS_CAT_5]*4 + [constants.CARD_FAVOR]*4
