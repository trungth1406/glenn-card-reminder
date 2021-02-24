import random
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


def next_number_of_day(start_date, days):
    return start_date + timedelta(days=days)


class Card:

    def __init__(self, start_date, content, max_used_day=5):
        self.start_date = start_date
        self.max_use = max_used_day
        self.content = content
        self.used = False

    def should_change(self):
        return next_number_of_day(self.start_date, self.max_use) < next_number_of_day(datetime.now().date().today(), 0)


class FlashCardDeck:

    def __init__(self, cards: [Card] = None, subject=None):
        if cards is None:
            self.cards = []
        self.cards = cards
        self.subject = subject

    def take(self, index, card: [Card]):
        self.cards.insert(index, card)

    @abstractmethod
    def get_replace_card(self):
        """
            Get card that should be replaced
        :return:
        """
        raise ValueError("Implement this")


class CardPile(ABC):

    def __init__(self, from_deck=None):
        self.max_card = 5
        self.max_replace = 1
        self.from_deck = from_deck

    @abstractmethod
    def do_replace_card(self):
        """
            Replace card of current active pile
        :return:
        """


class ReadingDeck(FlashCardDeck):

    def __init__(self, cards: [Card] = None, subject=None):
        super().__init__(cards, subject)
        self.current_pile = ReadingCardPile(self.cards[:5], self)

    def get_replace_card(self, amount=1):
        unused = [card for card in self.cards if not card.used and card not in self.current_pile.cards]
        if not unused:
            return []
        return random.choice(unused)

    def get_current_pile(self):
        return self.current_pile


class ReadingCardPile(FlashCardDeck, CardPile):

    def __init__(self, cards=None, from_deck=None):
        super().__init__(cards)
        self.from_deck = from_deck

    def do_replace_card(self):
        pile_replace = self.get_replace_card()
        card_from_deck = self.from_deck.get_replace_card()
        if card_from_deck:
            self.cards[self.cards.index(pile_replace)] = card_from_deck

    def get_replace_card(self):
        replace = min(self.cards, key=lambda card: card.start_date)
        if replace.should_change():
            replace.used = True
            return replace
        return None


class MathDeck(FlashCardDeck):

    def __init__(self, cards=None, subject=None):
        super().__init__(cards, subject)
        self.current_pile = MathCardPile(cards=self.cards[:10], from_deck=self)

    def get_replace_card(self):
        return self.get_next_current_mins(self.current_pile.get_current_min_values())

    def get_next_current_mins(self, current_mins):
        next_min_card = [0 for _ in range(2)]
        for i in range(2):
            next_cur_min = current_mins[i].content + 10
            next_min_card[i] = self.cards[next_cur_min - 1]
        return next_min_card


class MathCardPile(FlashCardDeck, CardPile):

    def __init__(self, cards=None, from_deck=None):
        FlashCardDeck.__init__(self, cards=cards)
        CardPile.__init__(self, from_deck)
        if len(cards) < 10:
            raise ValueError("Total number of math cards per pile must be 10 ")
        self.current_count = 0

    def get_replace_card(self):
        return self.get_current_min_values()

    def do_replace_card(self):
        """
        :return:
        """
        today = next_number_of_day(datetime.now().date().today(), 0)
        from_6th_day = next_number_of_day(self.get_current_min_values()[0].start_date, 6)
        if self.current_count != len(self.cards):
            if today >= from_6th_day:
                self.replace_card()
        else:
            if self.get_max_value() < 100:
                self.reset_pile(today)

    def replace_card(self):
        replace_from_deck = self.from_deck.get_replace_card()
        current_min = self.get_current_min_values()
        index_d = 0
        for index, min_num in enumerate(current_min):
            min_num.used = True
            self.cards[index] = replace_from_deck[index_d]
            index_d += 1
        self.current_count += 1

    def reset_pile(self, today):
        last_card = self.cards[len(self.cards) - 1]
        if today == next_number_of_day(last_card.start_date, 49):
            new_max = self.get_max_value()
            self.cards = self.from_deck[new_max:  new_max + 10]
            self.current_count = 0

    def get_max_value(self):
        return max([card.content for card in self.cards])

    def get_current_min_values(self):
        self.cards.sort(key=lambda x: x.content)
        return self.cards[0], self.cards[1]
