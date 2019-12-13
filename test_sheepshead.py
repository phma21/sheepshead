from deck import *
from sheepshead import Sauspiel, Game


def setup_sauspiel():
    return Sauspiel(Card(EICHEL, SAU))


def test_winning_position_trump():
    cards = [Card(HERZ, ACHT), Card(EICHEL, ZEHN), Card(EICHEL, NEUN), Card(GRAS, SAU)]

    assert setup_sauspiel().winning_position(cards) == 0


def test_winning_position_trump_2():
    cards = [Card(HERZ, KOENIG), Card(HERZ, ZEHN), Card(EICHEL, SAU), Card(GRAS, UNTER)]

    assert setup_sauspiel().winning_position(cards) == 3


def test_winning_position_trump_3():
    cards = [Card(HERZ, SAU), Card(HERZ, OBER), Card(EICHEL, OBER), Card(GRAS, UNTER)]

    assert setup_sauspiel().winning_position(cards) == 2


def test_winning_position_np_trump():
    cards = [Card(SCHELLEN, SIEBEN), Card(EICHEL, KOENIG), Card(SCHELLEN, ZEHN), Card(GRAS, SAU)]

    assert setup_sauspiel().winning_position(cards) == 2


def test_winning_position_no_trump_2():
    cards = [Card(SCHELLEN, KOENIG), Card(EICHEL, KOENIG), Card(GRAS, ZEHN)]

    assert setup_sauspiel().winning_position(cards) == 0


def test_score():
    deck = create_shuffled_deck()

    assert count_score(deck) == 120


def test_allowed_cards():
    layed_out_cards = []
    player_cards = create_shuffled_deck()

    # 32 - 5 (5 cards in suit of Rufsau)
    assert len(setup_sauspiel().allowed_cards(layed_out_cards, player_cards)) == 27


def test_allowed_cards_2():
    layed_out_cards = [Card(SCHELLEN, ACHT)]
    player_cards = {Card(HERZ, NEUN), Card(SCHELLEN, OBER), Card(SCHELLEN, SAU), Card(GRAS, SIEBEN)}

    assert setup_sauspiel().allowed_cards(layed_out_cards, player_cards) == {Card(SCHELLEN, SAU)}


def test_allowed_cards_3():
    layed_out_cards = [Card(SCHELLEN, ACHT), Card(SCHELLEN, KOENIG), Card(EICHEL, UNTER)]
    player_cards = {Card(HERZ, NEUN), Card(SCHELLEN, OBER), Card(SCHELLEN, SIEBEN)}

    assert setup_sauspiel().allowed_cards(layed_out_cards, player_cards) == {Card(SCHELLEN, SIEBEN)}


def test_allowed_cards_4():
    layed_out_cards = [Card(SCHELLEN, UNTER)]
    player_cards = {Card(GRAS, NEUN), Card(GRAS, SAU), Card(SCHELLEN, SIEBEN)}

    assert setup_sauspiel().allowed_cards(layed_out_cards, player_cards) == player_cards


def test_allowed_cards_5():
    layed_out_cards = [Card(SCHELLEN, UNTER)]
    player_cards = {Card(GRAS, NEUN), Card(EICHEL, SAU), Card(SCHELLEN, SIEBEN), Card(GRAS, OBER)}

    assert setup_sauspiel().allowed_cards(layed_out_cards, player_cards) == {Card(GRAS, OBER)}


def test_allowed_cards_6():
    layed_out_cards = [Card(SCHELLEN, ACHT)]
    player_cards = {Card(HERZ, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SIEBEN)}

    assert setup_sauspiel().allowed_cards(layed_out_cards, player_cards) == player_cards


def test_allowed_cards_rufsau_empty_trick():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU)}

    assert Sauspiel(rufsau=Card(GRAS, SAU))\
               .allowed_cards(layed_out_cards, player_cards) == {Card(GRAS, SAU), Card(SCHELLEN, OBER)}


def test_allowed_cards_rufsau_empty_trick_2():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU), Card(GRAS, KOENIG), Card(GRAS, OBER)}

    assert Sauspiel(rufsau=Card(GRAS, SAU))\
               .allowed_cards(layed_out_cards, player_cards) == {Card(GRAS, SAU), Card(SCHELLEN, OBER), Card(GRAS, OBER)}


def test_allowed_cards_rufsau_empty_trick_3():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU), Card(GRAS, KOENIG), Card(GRAS, SIEBEN)}

    assert Sauspiel(rufsau=Card(GRAS, SAU), davon_laufen=False).allowed_cards(layed_out_cards, player_cards) == \
           {Card(GRAS, SAU), Card(SCHELLEN, OBER)}


def test_allowed_cards_rufsau_empty_trick_davonlaufen():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU), Card(GRAS, KOENIG), Card(GRAS, SIEBEN)}

    assert Sauspiel(rufsau=Card(GRAS, SAU), davon_laufen=True).allowed_cards(layed_out_cards, player_cards) == player_cards


def test_allowed_cards_rufsau_irrelevant_suit():
    layed_out_cards = [Card(SCHELLEN, ZEHN)]
    player_cards = {Card(EICHEL, SAU), Card(GRAS, SAU)}

    assert Sauspiel(rufsau=Card(EICHEL, SAU)).allowed_cards(layed_out_cards, player_cards) == {Card(GRAS, SAU)}


def test_allowed_cards_rufsau_irrelevant_suit_2():
    layed_out_cards = [Card(SCHELLEN, ZEHN)]
    player_cards ={Card(EICHEL, SAU), Card(GRAS, SAU), Card(EICHEL, KOENIG)}

    assert Sauspiel(rufsau=Card(EICHEL, SAU)).allowed_cards(layed_out_cards, player_cards) \
        == {Card(EICHEL, KOENIG), Card(GRAS, SAU)}


def test_allowed_cards_rufsau_irrelevant_suit_3():
    layed_out_cards = [Card(SCHELLEN, ZEHN)]
    player_cards = {Card(EICHEL, SAU), Card(EICHEL, ZEHN), Card(EICHEL, KOENIG), Card(EICHEL, NEUN)}

    assert Sauspiel(rufsau=Card(EICHEL, SAU)).allowed_cards(layed_out_cards, player_cards) \
        == {Card(EICHEL, ZEHN), Card(EICHEL, KOENIG), Card(EICHEL, NEUN)}


def test_allowed_cards_rufsau_search():
    layed_out_cards = [Card(SCHELLEN, KOENIG)]
    player_cards = {Card(SCHELLEN, ZEHN), Card(SCHELLEN, UNTER), Card(SCHELLEN, SAU), Card(SCHELLEN, NEUN)}

    assert Sauspiel(rufsau=Card(SCHELLEN, SAU)).allowed_cards(layed_out_cards, player_cards) \
        == {Card(SCHELLEN, SAU)}


def test_allowed_cards_rufsau_search_2():
    layed_out_cards = [Card(SCHELLEN, KOENIG)]
    player_cards = {Card(SCHELLEN, ZEHN), Card(SCHELLEN, SAU), Card(SCHELLEN, NEUN), Card(SCHELLEN, ACHT)}

    assert Sauspiel(rufsau=Card(SCHELLEN, SAU)).allowed_cards(layed_out_cards, player_cards) \
        == {Card(SCHELLEN, SAU)}


class DummyMode:

    def winning_position(self, _):
        return 1

    def allowed_cards(self, _, player_cards):
        return player_cards


def test_play_card():

    player_cards = [{Card(HERZ, OBER)}, {Card(GRAS, UNTER)}, {Card(EICHEL, SAU)}, {Card(SCHELLEN, ACHT)}]

    game = Game(mode=DummyMode(), player_cards=player_cards)

    assert game.num_players == 4
    assert game.current_trick == []
    assert game.current_player == 0
    assert len(game.player_cards[0]) == 1
    assert game.get_scores_per_player() == [0, 0, 0, 0]

    game.play_card(Card(HERZ, OBER))

    assert game.current_player == 1
    assert len(game.player_cards[0]) == 0
    assert game.current_trick == [Card(HERZ, OBER)]

    game.play_card(Card(GRAS, UNTER))
    game.play_card(Card(EICHEL, SAU))

    assert game.current_trick == [Card(HERZ, OBER), Card(GRAS, UNTER), Card(EICHEL, SAU)]

    game.play_card(Card(SCHELLEN, ACHT))

    assert game.current_player == 1  # player 1 won the trick
    assert len(game.player_cards[3]) == 0
    assert game.current_trick == []
    # todo: will be changed anyway
    assert game.past_tricks == [
        [],
        [[Card(HERZ, OBER), Card(GRAS, UNTER), Card(EICHEL, SAU), Card(SCHELLEN, ACHT)]],
        [],
        []]

    # assert game.get_scores_per_player() == [0, 16, 0, 0]


def test_resolve_winning_player():
    current_player = 2
    winning_pos = 3

    expected_winning_player = 2

    assert expected_winning_player == Game(None, list(range(4))).resolve_winning_player(current_player, winning_pos)


def test_resolve_winning_player_2():
    current_player = 2
    winning_pos = 1

    expected_winning_player = 0

    assert expected_winning_player == Game(None, list(range(4))).resolve_winning_player(current_player, winning_pos)


def test_resolve_winning_player_3():
    current_player = 2
    winning_pos = 0

    expected_winning_player = 3

    assert expected_winning_player == Game(None, list(range(4))).resolve_winning_player(current_player, winning_pos)


def test_resolve_winning_player_4():
    current_player = 0
    winning_pos = 2

    expected_winning_player = 3

    assert expected_winning_player == Game(None, list(range(4))).resolve_winning_player(current_player, winning_pos)
