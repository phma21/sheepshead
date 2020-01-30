import pytest

from card_types import *
from deck import create_shuffled_deck, count_score
from rules import Sauspiel, Solo, Wenz, Geier, Ramsch, create_standard_game_result, \
    create_ramsch_game_result, SinglePlayerGame
from sheepshead import Game, Tick, Turn

EMPTY_PLAYER_HAND_3 = [set()] * 3
EMPTY_PLAYER_HAND_4 = [set()] * 4


def setup_eichel_rufspiel():
    player_hands = [{Card(EICHEL, SIEBEN)}, set(), set(), set()]
    return Sauspiel(player_hands, Card(EICHEL, SAU), 0)


def setup_gras_rufspiel():
    player_hands = [{Card(GRAS, SIEBEN)}, set(), set(), set()]
    return Sauspiel(player_hands, Card(GRAS, SAU), 0)


def setup_schellen_rufspiel():
    player_hands = [{Card(SCHELLEN, SIEBEN)}, set(), set(), set()]
    return Sauspiel(player_hands, Card(SCHELLEN, SAU), 0)


def test_sauspiel_sau_in_hand():
    player_hands = [{Card(SCHELLEN, SAU)}, set(), set(), set()]

    with pytest.raises(Exception):
        Sauspiel(player_hands, rufsau=Card(SCHELLEN, SAU), playmaker=0)


def test_sauspiel_no_matching_suit():
    player_hands = [set(), {Card(GRAS, OBER)}, set(), set()]

    with pytest.raises(Exception):
        Sauspiel(player_hands, rufsau=Card(GRAS, SAU), playmaker=1)


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


def test_winning_position_wenz():
    cards = [Card(EICHEL, OBER), Card(GRAS, KOENIG), Card(SCHELLEN, UNTER)]

    assert Wenz(EMPTY_PLAYER_HAND_4, 0, GRAS).winning_position(cards) == 2


def test_winning_position_wenz_2():
    cards = [Card(GRAS, OBER), Card(GRAS, KOENIG), Card(SCHELLEN, SAU)]

    assert Wenz(EMPTY_PLAYER_HAND_4, 0, HERZ).winning_position(cards) == 1


def test_winning_position_wenz_3():
    cards = [Card(GRAS, KOENIG), Card(GRAS, OBER)]

    assert Wenz(EMPTY_PLAYER_HAND_4, 0, GRAS).winning_position(cards) == 0


def test_winning_position_geier():
    cards = [Card(HERZ, OBER), Card(GRAS, KOENIG), Card(GRAS, UNTER)]

    assert Geier(EMPTY_PLAYER_HAND_4, 0, GRAS).winning_position(cards) == 0


def test_winning_position_geier_2():
    cards = [Card(GRAS, KOENIG), Card(GRAS, UNTER)]

    assert Geier(EMPTY_PLAYER_HAND_4, 0, GRAS).winning_position(cards) == 0


def test_winning_position_geier_3():
    cards = [Card(GRAS, UNTER), Card(EICHEL, SAU), Card(SCHELLEN, ZEHN), Card(HERZ, ACHT)]

    assert Geier(EMPTY_PLAYER_HAND_4, 0, HERZ).winning_position(cards) == 3


def test_winning_position_geier_4():
    cards = [Card(GRAS, UNTER), Card(EICHEL, SAU), Card(SCHELLEN, ZEHN), Card(HERZ, ACHT)]

    assert Geier(EMPTY_PLAYER_HAND_4, 0, EICHEL).winning_position(cards) == 1


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
    player_cards = [{Card(GRAS, NEUN), Card(SCHELLEN, OBER), Card(GRAS, SAU), Card(GRAS, KOENIG), Card(GRAS, SIEBEN)},
                    {Card(GRAS, ZEHN)}, set(), set()]

    assert Sauspiel(player_cards, rufsau=Card(GRAS, SAU), davon_laufen=True, playmaker=1)\
               .allowed_cards(layed_out_cards, player_cards[0]) == player_cards[0]


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


def test_wenz_allowed_cards_not_trump():
    layed_out_cards = [Card(HERZ, KOENIG)]
    player_cards = {Card(HERZ, SAU), Card(EICHEL, ZEHN), Card(HERZ, OBER), Card(HERZ, UNTER)}

    eichel_wenz = Wenz(EMPTY_PLAYER_HAND_4, playmaker=1, trump=EICHEL)

    assert eichel_wenz.allowed_cards(layed_out_cards, player_cards) \
        == {Card(HERZ, SAU), Card(HERZ, OBER)}


def test_wenz_allowed_cards_trump():
    layed_out_cards = [Card(EICHEL, KOENIG)]
    player_cards = {Card(HERZ, SAU), Card(EICHEL, ZEHN), Card(HERZ, OBER), Card(HERZ, UNTER)}

    eichel_wenz = Wenz(EMPTY_PLAYER_HAND_4, playmaker=1, trump=EICHEL)

    assert eichel_wenz.allowed_cards(layed_out_cards, player_cards) \
        == {Card(EICHEL, ZEHN), Card(HERZ, UNTER)}


def test_geier_allowed_cards_trump():
    layed_out_cards = [Card(HERZ, KOENIG)]
    player_cards = {Card(HERZ, UNTER), Card(HERZ, OBER), Card(HERZ, ACHT), Card(GRAS, UNTER)}

    herz_geier = Geier([set()] * 4, playmaker=1, trump=HERZ)

    assert herz_geier.allowed_cards(layed_out_cards, player_cards) == \
           {Card(HERZ, OBER), Card(HERZ, ACHT), Card(HERZ, UNTER)}


def test_geier_allowed_cards_no_trump():
    layed_out_cards = [Card(HERZ, KOENIG), Card(EICHEL, ZEHN)]
    player_cards = {Card(GRAS, UNTER), Card(GRAS, OBER), Card(HERZ, SAU)}

    schellen_geier = Geier(EMPTY_PLAYER_HAND_4, playmaker=1, trump=SCHELLEN)

    assert schellen_geier.allowed_cards(layed_out_cards, player_cards) == {Card(HERZ, SAU)}


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


def test_play_ramsch():
    player_cards = [{Card(HERZ, OBER), Card(EICHEL, KOENIG)},
                    {Card(GRAS, UNTER), Card(GRAS, ACHT)},
                    {Card(EICHEL, SAU), Card(SCHELLEN, ACHT)}]

    game = Game(Ramsch(player_cards), player_cards)

    assert game.teams == ({0}, {1}, {2})
    assert not game.is_finished()

    with pytest.raises(Exception):
        game.get_game_result()
    assert game.get_scores_per_team() == (0, 0, 0)
    assert game.get_scores_per_player() == (0, 0, 0)
    assert game.get_round() == 0
    assert game.num_players == 3

    with pytest.raises(Exception):
        game.play_card(Card(GRAS, UNTER))

    game.play_card(Card(EICHEL, KOENIG))
    game.play_card(Card(GRAS, ACHT))

    assert game.get_current_turn() == Turn(0, 2, {Card(EICHEL, SAU), Card(SCHELLEN, ACHT)}, {Card(EICHEL, SAU)})

    with pytest.raises(Exception):
        game.play_card(Card(SCHELLEN, ACHT))

    game.play_card((Card(EICHEL, SAU)))

    assert game.get_scores_per_player() == (0, 0, 15)
    assert game.get_scores_per_team() == (0, 0, 15)
    assert game.get_round() == 1
    assert game.get_current_turn() == Turn(1, 2, {Card(SCHELLEN, ACHT)}, {Card(SCHELLEN, ACHT)})

    game.play_card(Card(SCHELLEN, ACHT))
    game.play_card(Card(HERZ, OBER))
    game.play_card(Card(GRAS, UNTER))

    assert game.is_finished()
    assert game.get_scores_per_player() == (5, 0, 15)
    assert game.get_scores_per_team() == (5, 0, 15)

    assert game.get_game_result() == (10, 20, -30)


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
        create_standard_game_result(({1, 2}, {3, 4}), (19, 5), Sauspiel.TARIFF)


def test_game_results():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (61, 59)

    assert create_standard_game_result(teams, scores_per_team, Sauspiel.TARIFF) == (-10, 10, 10, -10)


def test_game_results_2():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (60, 60)

    assert create_standard_game_result(teams, scores_per_team, Sauspiel.TARIFF) == (10, -10, -10, 10)


def test_game_results_3():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (90, 30)

    assert create_standard_game_result(teams, scores_per_team, Sauspiel.TARIFF) == (-10, 10, 10, -10)


def test_game_results_4():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (91, 29)

    assert create_standard_game_result(teams, scores_per_team, Sauspiel.TARIFF) == (-20, 20, 20, -20)


def test_game_results_5():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (120, 0)

    # todo: rules correct?
    assert create_standard_game_result(teams, scores_per_team, Sauspiel.TARIFF) == (-30, 30, 30, -30)


def test_game_results_6():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (31, 89)

    assert create_standard_game_result(teams, scores_per_team, Sauspiel.TARIFF) == (10, -10, -10, 10)


def test_game_results_7():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (30, 90)

    assert create_standard_game_result(teams, scores_per_team, Sauspiel.TARIFF) == (20, -20, -20, 20)


def test_game_results_8():
    teams = ({1, 2}, {0, 3})
    scores_per_team = (0, 120)

    # todo: rules correct?
    assert create_standard_game_result(teams, scores_per_team, Sauspiel.TARIFF) == (30, -30, -30, 30)


def test_game_results_laufende():
    # Won't implement!
    pass


def test_game_results_solo():
    teams = ({1}, {0, 2})
    scores_per_team = (61, 59)

    assert create_standard_game_result(teams, scores_per_team, SinglePlayerGame.TARIFF) == (-50, 100, -50)


def test_game_results_solo_2():
    teams = ({1}, {0, 2})
    scores_per_team = (60, 60)

    assert create_standard_game_result(teams, scores_per_team, SinglePlayerGame.TARIFF) == (50, -100, 50)


def test_game_results_solo_3():
    teams = ({1}, {0, 2})
    scores_per_team = (91, 29)

    assert create_standard_game_result(teams, scores_per_team, SinglePlayerGame.TARIFF) == (-60, 120, -60)


def test_game_results_solo_4():
    teams = ({1}, {0, 2})
    scores_per_team = (0, 120)

    # todo: rules correct?
    assert create_standard_game_result(teams, scores_per_team, SinglePlayerGame.TARIFF) == (70, -140, 70)


def test_game_results_solo_5():
    teams = ({1}, {0, 2, 3})
    scores_per_team = (90, 30)

    assert create_standard_game_result(teams, scores_per_team, SinglePlayerGame.TARIFF) == (-50, 150, -50, -50)


def test_game_results_solo_6():
    teams = ({1}, {0, 2, 3})
    scores_per_team = (110, 10)

    assert create_standard_game_result(teams, scores_per_team, SinglePlayerGame.TARIFF) == (-60, 180, -60, -60)


def test_game_results_ramsch_3_players():
    teams = ({0}, {1}, {2})
    scores_per_team = (30, 30, 60)

    assert create_ramsch_game_result(teams, scores_per_team, Ramsch.TARIFF) == (10, 10, -20)


def test_game_results_ramsch_4_players():
    teams = ({0}, {1}, {2}, {3})
    scores_per_team = (30, 30, 50, 10)

    assert create_ramsch_game_result(teams, scores_per_team, Ramsch.TARIFF) == (10, 10, -30, 10)


def test_game_results_ramsch__even():
    teams = ({0}, {1}, {2}, {3})
    scores_per_team = (0, 60, 60, 0)

    # The game rules for this special case are unclear.
    # For ease of implementation, the first player with highest score pays
    assert create_ramsch_game_result(teams, scores_per_team, Ramsch.TARIFF) == (20, -50, 10, 20)


def test_game_results_ramsch_jungfrau():
    teams = ({0}, {1}, {2})
    scores_per_team = (0, 90, 30)

    assert create_ramsch_game_result(teams, scores_per_team, Ramsch.TARIFF) == (20, -30, 10)


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


def test_teams_sauspiel():
    player_cards = [{Card(GRAS, NEUN), Card(SCHELLEN, OBER)},
                    {Card(GRAS, SAU), Card(GRAS, KOENIG)},
                    {Card(GRAS, OBER), Card(HERZ, SAU)},
                    {Card(GRAS, ACHT), Card(EICHEL, SAU)}]
    playmaker = 3

    rufspiel = Sauspiel(player_cards, Card(GRAS, SAU), playmaker)

    assert rufspiel.teams == ({1, 3}, {0, 2})


def test_teams_wenz():
    eichel_wenz = Wenz(EMPTY_PLAYER_HAND_4, playmaker=2, trump=EICHEL)

    assert eichel_wenz.teams == ({2}, {0, 1, 3})


def test_teams_solo():
    eichel_solo = Solo(EMPTY_PLAYER_HAND_4, playmaker=0, trump=EICHEL)

    assert eichel_solo.teams == ({0}, {1, 2, 3})


def test_teams_geier():
    player_cards = [set(),
                    set(),
                    set()]

    rufspiel = Geier(player_cards, playmaker=1, trump=HERZ)

    assert rufspiel.teams == ({1}, {0, 2})


def test_teams_ramsch():
    player_cards = [set(),
                    set(),
                    set()]
    ramsch = Ramsch(player_cards)

    assert ramsch.teams == ({0}, {1}, {2})
