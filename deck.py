from enum import Enum
from random import shuffle
from typing import List, Iterable


class Suit(Enum):
    EICHEL = 1
    GRAS = 2
    HERZ = 3
    SCHELLEN = 4


SCHELLEN = Suit.SCHELLEN
HERZ = Suit.HERZ
GRAS = Suit.GRAS
EICHEL = Suit.EICHEL


class Face(Enum):
    SIEBEN = 1
    ACHT = 2
    NEUN = 3
    UNTER = 4
    OBER = 5
    KOENIG = 6
    ZEHN = 7
    SAU = 8


SIEBEN = Face.SIEBEN
ACHT = Face.ACHT
NEUN = Face.NEUN
ZEHN = Face.ZEHN
UNTER = Face.UNTER
OBER = Face.OBER
KOENIG = Face.KOENIG
SAU = Face.SAU


SCORE_VALUES = {
    SIEBEN: 0,
    ACHT: 0,
    NEUN: 0,
    ZEHN: 10,
    UNTER: 2,
    OBER: 3,
    KOENIG: 4,
    SAU: 11
}


class Card:
    def __init__(self, suit: Suit, face: Face):
        assert isinstance(suit, Suit)
        assert isinstance(face, Face)
        self.suit = suit
        self.face = face

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.face == other.face
        else:
            return False

    def __hash__(self):
        return int(str(self.face.value) + str(self.suit.value))

    def __str__(self):
        return f"{self.suit.name} {self.face.name}"


def create_shuffled_deck() -> List[Card]:
    deck = []
    for f in Face:
        for s in Suit:
            deck.append(Card(s, f))
    shuffle(deck)
    return deck


def create_shuffled_player_hands() -> List[List[Card]]:
    deck = create_shuffled_deck()
    return [deck[0:8], deck[8:16], deck[16:24], deck[24:32]]


def count_score(cards: Iterable[Card]):
    return sum(map(lambda card: SCORE_VALUES[card.face], cards))
