import random

class Deck:
    def __init__(self, max_card):
        self.cards = []
        for i in range(max_card):
            self.cards.append(0)

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

