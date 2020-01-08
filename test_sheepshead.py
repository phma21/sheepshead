import pytest

from deck import *
from sheepshead import Game, Tick, get_game_results, Turn
from rules import Sauspiel, Solo


def setup_eichel_rufspiel():
    return Sauspiel(create_shuffled_player_hands(), Card(EICHEL, SAU), 0)


def setup_gras_rufspiel():
    return Sauspiel(create_shuffled_player_hands(), Card(GRAS, SAU), 0)


def setup_schellen_rufspiel():
    return Sauspiel(create_shuffled_player_hands(), Card(SCHELLEN, SAU), 0)


def test_winning_position_trump():
    cards = [Card(HERZ, ACHT), Card(EICHEL, ZEHN), Card(EICHEL, NEUN), Card(GRAS, SAU)]

    assert setup_eichel_rufspiel().winning_position(cards) == 0


def test_winning_position_trump_2():
    cards = [Card(HERZ, KOENIG), Card(HERZ, ZEHN), Card(EICHEL, SAU), Card(GRAS, UNTER)]

    assert setup_eichel_rufspiel().winning_position(cards) == 3


def test_winning_position_trump_3():
    cards = [Card(HERZ, SAU), Card(HERZ, OBER), Card(EICHEL, OBER), Card(GRAS, UNTER)]

    assert setup_eichel_rufspiel().winning_position(cards) == 2


def test_winning_position_np_trump():
    cards = [Card(SCHELLEN, SIEBEN), Card(EICHEL, KOENIG), Card(SCHELLEN, ZEHN), Card(GRAS, SAU)]

    assert setup_eichel_rufspiel().winning_position(cards) == 2


def test_winning_position_no_trump_2():
    cards = [Card(SCHELLEN, KOENIG), Card(EICHEL, KOENIG), Card(GRAS, ZEHN)]

    assert setup_eichel_rufspiel().winning_position(cards) == 0


def test_score():
    deck = create_shuffled_deck()

    assert count_score(deck) == 120


def test_allowed_cards():
    layed_out_cards = []
    player_cards = set(create_shuffled_deck())

    # 32 - 5 (5 cards in suit of Rufsau)
    assert len(setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards)) == 27


def test_allowed_cards_2():
    layed_out_cards = [Card(SCHELLEN, ACHT)]
    player_cards = {Card(HERZ, NEUN), Card(SCHELLEN, OBER), Card(SCHELLEN, SAU), Card(GRAS, SIEBEN)}

    assert setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards) == {Card(SCHELLEN, SAU)}


def test_allowed_cards_3():
    layed_out_cards = [Card(SCHELLEN, ACHT), Card(SCHELLEN, KOENIG), Card(EICHEL, UNTER)]
    player_cards = {Card(HERZ, NEUN), Card(SCHELLEN, OBER), Card(SCHELLEN, SIEBEN)}

    assert setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards) == {Card(SCHELLEN, SIEBEN)}


def test_allowed_cards_4():
    layed_out_cards = [Card(SCHELLEN, UNTER)]
    player_cards = {Card(GRAS, NEUN), Card(GRAS, SAU), Card(SCHELLEN, SIEBEN)}

    assert setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards) == player_cards


def test_allowed_cards_5():
    layed_out_cards = [Card(SCHELLEN, UNTER)]
    player_cards = {Card(GRAS, NEUN), Card(EICHEL, SAU), Card(SCHELLEN, SIEBEN), Card(GRAS, OBER)}

    assert setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards) == {Card(GRAS, OBER)}


def test_allowed_cards_6():
    layed_out_cards = [Card(SCHELLEN, ACHT)]
    player_cards = {Card(HERZ, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SIEBEN)}

    assert setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards) == player_cards


def test_allowed_cards_rufsau_empty_trick():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU)}

    assert setup_gras_rufspiel().allowed_cards(layed_out_cards, player_cards) == {Card(GRAS, SAU), Card(SCHELLEN, OBER)}


def test_allowed_cards_rufsau_empty_trick_2():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU), Card(GRAS, KOENIG), Card(GRAS, OBER)}

    assert setup_gras_rufspiel().allowed_cards(
        layed_out_cards, player_cards) == {Card(GRAS, SAU), Card(SCHELLEN, OBER), Card(GRAS, OBER)}


def test_allowed_cards_rufsau_empty_trick_3():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU), Card(GRAS, KOENIG), Card(GRAS, SIEBEN)}

    assert setup_gras_rufspiel().allowed_cards(layed_out_cards, player_cards) == \
           {Card(GRAS, SAU), Card(SCHELLEN, OBER)}


def test_allowed_cards_rufsau_empty_trick_4():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, KOENIG), Card(GRAS, SIEBEN)}

    assert setup_gras_rufspiel().allowed_cards(layed_out_cards, player_cards) == player_cards


def test_allowed_cards_rufsau_empty_trick_davonlaufen():
    layed_out_cards = []
    player_cards = {Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU), Card(GRAS, KOENIG), Card(GRAS, SIEBEN)}

    assert Sauspiel(create_shuffled_player_hands(), rufsau=Card(GRAS, SAU), davon_laufen=True, playmaker=0)\
               .allowed_cards(layed_out_cards, player_cards) == player_cards


def test_allowed_cards_rufsau_irrelevant_suit():
    layed_out_cards = [Card(SCHELLEN, ZEHN)]
    player_cards = {Card(EICHEL, SAU), Card(GRAS, SAU)}

    assert setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards) == {Card(GRAS, SAU)}


def test_allowed_cards_rufsau_irrelevant_suit_2():
    layed_out_cards = [Card(SCHELLEN, ZEHN)]
    player_cards ={Card(EICHEL, SAU), Card(GRAS, SAU), Card(EICHEL, KOENIG)}

    assert setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards) \
        == {Card(EICHEL, KOENIG), Card(GRAS, SAU)}


def test_allowed_cards_rufsau_irrelevant_suit_3():
    layed_out_cards = [Card(SCHELLEN, ZEHN)]
    player_cards = {Card(EICHEL, SAU), Card(EICHEL, ZEHN), Card(EICHEL, KOENIG), Card(EICHEL, NEUN)}

    assert setup_eichel_rufspiel().allowed_cards(layed_out_cards, player_cards) \
        == {Card(EICHEL, ZEHN), Card(EICHEL, KOENIG), Card(EICHEL, NEUN)}


def test_allowed_cards_rufsau_search():
    layed_out_cards = [Card(SCHELLEN, KOENIG)]
    player_cards = {Card(SCHELLEN, ZEHN), Card(SCHELLEN, UNTER), Card(SCHELLEN, SAU), Card(SCHELLEN, NEUN)}

    assert setup_schellen_rufspiel().allowed_cards(layed_out_cards, player_cards) \
        == {Card(SCHELLEN, SAU)}


def test_allowed_cards_rufsau_search_2():
    layed_out_cards = [Card(SCHELLEN, KOENIG)]
    player_cards = {Card(SCHELLEN, ZEHN), Card(SCHELLEN, SAU), Card(SCHELLEN, NEUN), Card(SCHELLEN, ACHT)}

    assert setup_schellen_rufspiel().allowed_cards(layed_out_cards, player_cards) \
        == {Card(SCHELLEN, SAU)}


class DummyMode:

    def winning_position(self, _):
        return 1

    def allowed_cards(self, _, player_cards):
        return player_cards

    def determine_teams(self, _):
        return ()


def test_play_card():

    player_cards = [{Card(HERZ, OBER)}, {Card(GRAS, UNTER)}, {Card(EICHEL, SAU)}, {Card(SCHELLEN, ACHT)}]

    game = Game(mode=DummyMode(), player_cards=player_cards)

    assert game.num_players == 4
    assert game.current_trick == []
    assert game.current_player == 0
    assert len(game.player_cards[0]) == 1
    assert game.get_scores_per_player() == (0, 0, 0, 0)
    assert not game.is_finished()

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
    assert game.past_ticks == [
        Tick([Card(HERZ, OBER), Card(GRAS, UNTER), Card(EICHEL, SAU), Card(SCHELLEN, ACHT)], 1)]

    assert game.get_scores_per_player() == (0, 16, 0, 0)
    assert game.is_finished()


def setup_3_player_2_cards_sauspiel():
    player_cards = [{Card(HERZ, OBER), Card(EICHEL, KOENIG)},
                    {Card(GRAS, UNTER), Card(GRAS, ACHT)},
                    {Card(EICHEL, SAU), Card(EICHEL, ACHT)}]

    return Game(Sauspiel(player_cards, Card(EICHEL, SAU), playmaker=0), player_cards)


def test_get_current_turn():
    game = setup_3_player_2_cards_sauspiel()

    assert game.get_current_turn() == Turn(0, 0, {Card(HERZ, OBER), Card(EICHEL, KOENIG)}, {Card(HERZ, OBER), Card(EICHEL, KOENIG)})
    game.play_card(Card(HERZ, OBER))
    assert game.get_current_turn() == Turn(0, 1, {Card(GRAS, UNTER), Card(GRAS, ACHT)}, {Card(GRAS, UNTER)})


def test_play_sauspiel_disallowed_card():
    game = setup_3_player_2_cards_sauspiel()
    with pytest.raises(Exception):
        game.play_card(Card(GRAS, UNTER))


def test_play_sauspiel_disallowed_card_2():
    game = setup_3_player_2_cards_sauspiel()
    game.play_card(Card(HERZ, OBER))

    with pytest.raises(Exception):
        game.play_card(Card(GRAS, ACHT))


def test_play_sauspiel_until_end():
    game = setup_3_player_2_cards_sauspiel()

    tick_1 = Tick([Card(HERZ, OBER), Card(GRAS, UNTER), Card(EICHEL, ACHT)], scoring_player=0)
    tick_2 = Tick([Card(EICHEL, KOENIG), Card(GRAS, ACHT), Card(EICHEL, SAU)], scoring_player=2)

    assert game.teams == ({0, 2}, {1})
    assert not game.is_finished()

    game.play_card(Card(HERZ, OBER))
    game.play_card(Card(GRAS, UNTER))
    game.play_card(Card(EICHEL, ACHT))

    assert game.current_trick == []
    assert game.current_player == 0
    assert game.past_ticks == [tick_1]

    game.play_card(Card(EICHEL, KOENIG))
    game.play_card(Card(GRAS, ACHT))
    game.play_card(Card(EICHEL, SAU))

    assert game.current_trick == []
    assert game.current_player == 2
    assert game.past_ticks == [tick_1, tick_2]

    assert game.get_scores_per_player() == (5, 0, 15)

    assert game.get_scores_per_team() == (20, 0)
    assert game.is_finished()


# todo: test for wenz:
# unter gewinnt vor ober, herz wird gestochen von z.b. schellen
# ober gehört bei allowed cards zum normalen zeug
# ober wird von koenig gestochen
# teams


# todo: test for geier:
# unter sind kein trumpf, wird von z.b. sau gestochen
# trumpffrabe sticht herz
# unter gehört zu normalen farben
# unter wird von Zehn gestochen
# teams

# todo: test for ramsch
# -> needs change to how game results are calculated!


def test_solo():
    player_cards = [{Card(HERZ, ZEHN)}, {Card(GRAS, KOENIG)}]
    mode = Solo(player_cards, playmaker=0, trump=GRAS)
    game = Game(mode, player_cards)

    assert game.teams == ({0}, {1})

    game.play_card(Card(HERZ, ZEHN))
    game.play_card(Card(GRAS, KOENIG))

    assert game.past_ticks[0].scoring_player == 1


def test_game_results_score_missmatch():
    with pytest.raises(Exception):
        get_game_results(None, (19, 5))


def test_game_results():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (61, 59)

    assert get_game_results(teams, scores_per_team) == (-10, 10, 10, -10)


def test_game_results_2():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (60, 60)

    assert get_game_results(teams, scores_per_team) == (10, -10, -10, 10)


def test_game_results_3():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (90, 30)

    assert get_game_results(teams, scores_per_team) == (-10, 10, 10, -10)


def test_game_results_4():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (91, 29)

    assert get_game_results(teams, scores_per_team) == (-20, 20, 20, -20)


def test_game_results_5():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (120, 0)

    # todo: rules correct?
    assert get_game_results(teams, scores_per_team) == (-30, 30, 30, -30)


def test_game_results_6():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (31, 89)

    assert get_game_results(teams, scores_per_team) == (10, -10, -10, 10)


def test_game_results_7():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (30, 90)

    assert get_game_results(teams, scores_per_team) == (20, -20, -20, 20)


def test_game_results_8():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (0, 120)

    # todo: rules correct?
    assert get_game_results(teams, scores_per_team) == (30, -30, -30, 30)


def test_game_results_laufende():
    # TODO: Laufende
    pass


def test_resolve_winning_player():
    current_player = 2
    winning_pos = 3

    expected_winning_player = 2

    assert expected_winning_player == Game(None, list(range(4))).resolve_tick_winner(current_player, winning_pos)


def test_resolve_winning_player_2():
    current_player = 2
    winning_pos = 1

    expected_winning_player = 0

    assert expected_winning_player == Game(None, list(range(4))).resolve_tick_winner(current_player, winning_pos)


def test_resolve_winning_player_3():
    current_player = 2
    winning_pos = 0

    expected_winning_player = 3

    assert expected_winning_player == Game(None, list(range(4))).resolve_tick_winner(current_player, winning_pos)


def test_resolve_winning_player_4():
    current_player = 0
    winning_pos = 2

    expected_winning_player = 3

    assert expected_winning_player == Game(None, list(range(4))).resolve_tick_winner(current_player, winning_pos)


def test_determine_teams():
    player_cards = [{Card(GRAS, NEUN), Card(SCHELLEN, OBER)},
                    {Card(GRAS, SAU), Card(GRAS, KOENIG)},
                    {Card(GRAS, OBER), Card(HERZ, SAU)},
                    {Card(GRAS, ACHT), Card(EICHEL, SAU)}]
    playmaker = 3

    rufspiel = Sauspiel(create_shuffled_player_hands(), Card(GRAS, SAU), playmaker)

    assert rufspiel._determine_teams(player_cards, playmaker) == ({1, 3}, {0, 2})
