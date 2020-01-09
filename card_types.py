from enum import Enum


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
    SAU = 8
    ZEHN = 7
    KOENIG = 6
    OBER = 5
    UNTER = 4
    NEUN = 3
    ACHT = 2
    SIEBEN = 1


SIEBEN = Face.SIEBEN
ACHT = Face.ACHT
NEUN = Face.NEUN
ZEHN = Face.ZEHN
UNTER = Face.UNTER
OBER = Face.OBER
KOENIG = Face.KOENIG
SAU = Face.SAU


CARD_SCORE = {
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

    def __repr__(self):
        return f"({self.suit.name}, {self.face.name})"
