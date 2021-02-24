import unittest
from datetime import datetime
from pprint import pprint

from card.cards import Card, MathDeck, ReadingDeck


class TestCards(unittest.TestCase):
    last_wed = datetime(year=2021, month=2, day=17).date()
    last_thurs = datetime(year=2021, month=2, day=16).date()
    today = datetime.today().date()

    def test_math_cards(self):
        deck = MathDeck(cards=
        [
            Card(start_date=TestCards.last_wed, content=i, max_used_day=35) for i in range(1, 100)
        ],
            subject="MATH")

        deck.current_pile.do_replace_card()

    def test_reading_card(self):
        deck = ReadingDeck(cards=
        [
            Card(start_date=TestCards.today, content="Anything 1"),
            Card(start_date=TestCards.last_thurs, content="Anything 2"),
            Card(start_date=TestCards.last_thurs, content="Anything 3"),
            Card(start_date=TestCards.last_thurs, content="Anything 4"),
            Card(start_date=TestCards.last_thurs, content="Anything 5"),
            Card(start_date=TestCards.last_thurs, content="Anything 6"),
            Card(start_date=TestCards.last_thurs, content="Anything 7"),

        ])

        deck.current_pile.do_replace_card()
