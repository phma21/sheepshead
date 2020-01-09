from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Set, Tuple

import numpy as np

from card_types import *


class BasicTrumpGame(ABC):

    def __init__(self, trump=HERZ, face_trump_order=(OBER, UNTER)):
        self.NON_TRUMP_ORDER = [face for face in Face if face not in face_trump_order]

        self.NON_TRUMP_FACE_RANKS = {face: power + 100 for power, face in enumerate(self.NON_TRUMP_ORDER)}

        self.TRUMP_ORDER = []
        for face_trump in face_trump_order:
            self.TRUMP_ORDER += [Card(s, face_trump) for s in Suit]
        self.TRUMP_ORDER += [Card(trump, f) for f in self.NON_TRUMP_ORDER]

        self.TRUMP_CARD_RANKS = {card: power for power, card in enumerate(self.TRUMP_ORDER)}

    def allowed_cards(self, layed_out_cards: List[Card], player_cards: Set[Card]) -> Set[Card]:
        if len(layed_out_cards) == 0:
            return player_cards

        first_card = layed_out_cards[0]

        if first_card in self.TRUMP_CARD_RANKS:
            matching_cards = {c for c in player_cards if c in self.TRUMP_CARD_RANKS}
        else:
            matching_cards = {c for c in player_cards if c.suit == first_card.suit
                              and c.face in self.NON_TRUMP_FACE_RANKS}

        if len(matching_cards) == 0:
            return deepcopy(player_cards)
        else:
            return matching_cards

    def winning_position(self, cards: List[Card]):
        first_suit = cards[0].suit

        def card_to_power(card):
            try:
                return self.TRUMP_CARD_RANKS[card]
            except KeyError:
                if card.suit == first_suit:
                    return self.NON_TRUMP_FACE_RANKS[card.face]
                else:
                    return 1000

        return np.argmin([card_to_power(card) for card in cards])

    @property
    @abstractmethod
    def teams(self):
        pass


class Sauspiel(BasicTrumpGame):

    def __init__(self, player_cards: List[Set[Card]], rufsau: Card, playmaker: int, davon_laufen=False):
        super().__init__()
        self.rufsau = deepcopy(rufsau)
        self.davon_laufen = davon_laufen
        self._teams = self._determine_teams(player_cards, playmaker)

    @property
    def teams(self):
        return self._teams

    # chain this function after applying general_trump_game_rule
    def _apply_rufsau_rule(self, layed_out_cards: List[Card], len_player_cards: int, allowed_cards: Set[Card]) -> Set[Card]:
        if self.rufsau in allowed_cards and len_player_cards != 1:
            if len(layed_out_cards) == 0:  # First card on the table
                call_suits = self._filter_rufsau_accompanying_cards(allowed_cards)
                if self.davon_laufen and len(call_suits) >= 3:
                    return deepcopy(allowed_cards)
                else:  # len(call_suits) < 3
                    return {card for card in allowed_cards if card not in call_suits}
            else:  # len(layed_out_cards) > 0
                if layed_out_cards[0].suit == self.rufsau.suit:
                    return {self.rufsau}
                else:  # Sau was not searched for, all cards except for Sau are allowed
                    return {card for card in allowed_cards if card != self.rufsau}
        else:
            return deepcopy(allowed_cards)

    def allowed_cards(self, layed_out_cards: List[Card], player_cards: Set[Card]) -> Set[Card]:
        allowed_cards_base = super().allowed_cards(layed_out_cards, player_cards)
        allowed_cards_sauspiel = self._apply_rufsau_rule(layed_out_cards, len(player_cards), allowed_cards_base)
        return allowed_cards_sauspiel

    def _filter_rufsau_accompanying_cards(self, cards: Set[Card]) -> Set[Card]:
        return {card for card in cards if
                card.face in self.NON_TRUMP_FACE_RANKS
                and card.suit == self.rufsau.suit
                and card != self.rufsau}

    def _determine_teams(self, player_cards, playmaker) -> Tuple[Set[int], Set[int]]:
        players = set()
        non_players = set()
        for it_player in range(len(player_cards)):
            if any([card == self.rufsau for card in player_cards[it_player]]):
                players.add(it_player)
            elif playmaker == it_player:
                players.add(it_player)
            else:
                non_players.add(it_player)

        return players, non_players


class SinglePlayerGame(BasicTrumpGame):

    def __init__(self, player_cards: List[Set[Card]], playmaker: int, trump: Suit, face_trump_order: Tuple[Face, ...]):
        super().__init__(trump=trump, face_trump_order=face_trump_order)
        self._teams = determine_teams_one_player_game(player_cards, playmaker)

    @property
    def teams(self):
        return self._teams


class Solo(SinglePlayerGame):
    def __init__(self, player_cards: List[Set[Card]], playmaker: int, trump: Suit):
        super().__init__(player_cards, playmaker, trump, face_trump_order=(OBER, UNTER))


class Wenz(SinglePlayerGame):
    def __init__(self, player_cards: List[Set[Card]], playmaker: int, trump: Suit):
        super().__init__(player_cards, playmaker, trump, face_trump_order=(UNTER, ))


class Geier(SinglePlayerGame):
    def __init__(self, player_cards: List[Set[Card]], playmaker: int, trump: Suit):
        super().__init__(player_cards, playmaker, trump, face_trump_order=(OBER, ))


class Ramsch(BasicTrumpGame):
    @property
    def teams(self):
        return {0}, {1}, {2}, {3}

    def __init__(self):
        super().__init__()


def determine_teams_one_player_game(player_cards, playmaker):
    num_players = len(player_cards)
    return {playmaker}, set(range(num_players)) - {playmaker}
