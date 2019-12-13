import numpy as np

from deck import *


class BasicTrumpGame:

    def __init__(self, trump=HERZ):
        self.trump = trump




class Sauspiel:

    NON_TRUMP_ORDER = [SAU, ZEHN, KOENIG, NEUN, ACHT, SIEBEN]
    NON_TRUMP_FACE_RANKS = {face: power + 100 for power, face in enumerate(NON_TRUMP_ORDER)}

    TRUMP_ORDER = [Card(s, OBER) for s in Suit] \
        + [Card(s, UNTER) for s in Suit] \
        + [Card(HERZ, f) for f in NON_TRUMP_ORDER]
    TRUMP_CARD_RANKS = {card: power for power, card in enumerate(TRUMP_ORDER)}

    def __init__(self, rufsau: Card, davon_laufen=False):
        self.rufsau = rufsau
        self.davon_laufen = davon_laufen

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

    def allowed_cards_basegame(self, layed_out_cards: List[Card], player_cards: Set[Card]) -> Set[Card]:
        if len(layed_out_cards) == 0:
            return player_cards

        first_card = layed_out_cards[0]

        if first_card in self.TRUMP_CARD_RANKS:
            matching_cards = {c for c in player_cards if c in self.TRUMP_CARD_RANKS}
        else:
            matching_cards = {c for c in player_cards if c.suit == first_card.suit
                              and c.face in self.NON_TRUMP_FACE_RANKS}

        if len(matching_cards) == 0:
            return player_cards
        else:
            return matching_cards

    # chain this function after applying general_trump_game_rule
    def apply_rufsau_rule(self, layed_out_cards: List[Card], len_player_cards: int, allowed_cards: Set[Card]) -> Set[Card]:
        if self.rufsau in allowed_cards or len_player_cards != 1:
            if len(layed_out_cards) == 0:  # First card on the table
                call_suits = self.filter_rufsau_accompanying_cards(allowed_cards)
                if self.davon_laufen and len(call_suits) >= 3:
                    return allowed_cards
                else:  # len(call_suits) < 3
                    return {card for card in allowed_cards if card not in call_suits}
            else:  # len(layed_out_cards) > 0
                if layed_out_cards[0].suit == self.rufsau.suit:
                    return {self.rufsau}
                else:  # Sau was not searched for, all cards except for Sau are allowed
                    return {card for card in allowed_cards if card != self.rufsau}
        else:
            return allowed_cards

    def allowed_cards(self, layed_out_cards: List[Card], player_cards: Set[Card]) -> Set[Card]:
        allowed_cards_base = self.allowed_cards_basegame(layed_out_cards, player_cards)
        return self.apply_rufsau_rule(layed_out_cards, len(player_cards), allowed_cards_base)

    def filter_rufsau_accompanying_cards(self, cards: Set[Card]) -> Set[Card]:
        return {card for card in cards if
                    card.face in self.NON_TRUMP_FACE_RANKS
                    and card.suit == self.rufsau.suit
                    and card != self.rufsau}

    # todo later: extend and extract to generalize to different trump
    # todo: after implementing rufsau, add function to determine teams

    # todo: add replay functionality to game (need to change how past_tricks are stored)


class Game:
    def __init__(self, mode, player_cards: List[Set[Card]]):
        self.mode: Sauspiel = mode
        self.player_cards = player_cards
        self.num_players = len(player_cards)
        self.past_tricks = [[] for _ in range(self.num_players)]
        self.current_trick = []
        self.current_player = 0

    def resolve_winning_player(self, current_player, winning_pos):
        winning_pos_relative_to_player = winning_pos - (self.num_players - 1)
        winning_player = current_player + winning_pos_relative_to_player  # can be negative
        return (winning_player + self.num_players) % 4

    # todo
    def get_scores_per_player(self):
        return [0, 0, 0, 0]

    # todo
    def get_scores_per_team(self):
        # 0 player team, 1 non-player team
        return [0, 0]

    # todo
    def get_teams(self):
        return [[0], [1, 2, 3]]

    def play_card(self, card):
        # Player must hold the card in hand
        if card not in self.player_cards[self.current_player]:
            raise Exception("Attempted to play a card which isn't yours!")
        # Card must be allowed to play
        if card not in self.mode.allowed_cards(self.current_trick, self.player_cards[self.current_player]):
            raise Exception("You are not allowed to play this card")

        # Execute move
        self.player_cards[self.current_player].remove(card)
        self.current_trick.append(card)

        # tick complete
        if len(self.current_trick) == self.num_players:
            # determine winner, give tick to him and set him as next player
            winning_pos = self.mode.winning_position(self.current_trick)
            winning_player = self.resolve_winning_player(self.current_player, winning_pos)

            self.past_tricks[winning_player].append(self.current_trick)
            self.current_trick = []
            self.current_player = winning_player
        else:
            self.current_player = (self.current_player + 1) % self.num_players


if __name__ == '__main__':

    deck = create_shuffled_deck()

    sauspiel = Sauspiel()

    print(sauspiel.TRUMP_ORDER)
