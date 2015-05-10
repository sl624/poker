# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
import pytz
import pytest
from poker.room.fulltiltpoker import FullTiltPokerHandHistory, _Flop
from poker.card import Card
from poker.hand import Combo
from poker.handhistory import _Player
from poker.constants import Game, Currency, Limit, GameType, Action
from . import ftp_hands


ET = pytz.timezone('US/Eastern')


@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text and returns a FullTiltPokerHandHistory instance."""
    h = FullTiltPokerHandHistory(request.instance.hand_text)
    h.parse_header()
    return h


@pytest.fixture
def hand(request):
    """Parse handhistory defined in hand_text class attribute and returns a FullTiltPokerHandHistory instance."""
    hh = FullTiltPokerHandHistory(request.instance.hand_text)
    hh.parse()
    return hh


@pytest.fixture
def flop(scope='module'):
    return _Flop(
        ['[8h 4h Tc] (Total Pot: 230, 2 Players)',
         'JohnyyR checks',
         'FatalRevange has 15 seconds left to act',
         'FatalRevange bets 120',
         'JohnyyR folds',
         'Uncalled bet of 120 returned to FatalRevange',
         'FatalRevange mucks',
         'FatalRevange wins the pot (230)'
         ], 0)


class TestHandWithFlopOnly:
    hand_text = ftp_hands.HAND1

    @pytest.mark.parametrize(('attribute', 'expected_value'), [
        ('game_type', GameType.TOUR),
        ('sb', Decimal(10)),
        ('bb', Decimal(20)),
        ('date', ET.localize(datetime(2013, 9, 22, 13, 26, 50))),
        ('game', Game.HOLDEM),
        ('limit', Limit.NL),
        ('ident', '33286946295'),
        ('tournament_ident', '255707037'),
        ('table_name', '179'),
        ('tournament_level', None),
        ('buyin', None),
        ('rake', None),
        ('currency', None),
    ])
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize('attribute,expected_value',
        [('players', [
            _Player(name='Popp1987', stack=13587, seat=1, combo=None),
            _Player(name='Luckytobgood', stack=10110, seat=2, combo=None),
            _Player(name='FatalRevange', stack=9970, seat=3, combo=None),
            _Player(name='IgaziFerfi', stack=10000, seat=4, combo=Combo('Ks9d')),
            _Player(name='egis25', stack=6873, seat=5, combo=None),
            _Player(name='gamblie', stack=9880, seat=6, combo=None),
            _Player(name='idanuTz1', stack=10180, seat=7, combo=None),
            _Player(name='PtheProphet', stack=9930, seat=8, combo=None),
            _Player(name='JohnyyR', stack=9840, seat=9, combo=None),
        ]),
        ('button', _Player(name='egis25', stack=6873, seat=5, combo=None)),
        ('max_players', 9),
        ('hero', _Player(name='IgaziFerfi', stack=10000, seat=4, combo=Combo('Ks9d'))),
        ('preflop_actions', ('PtheProphet has 15 seconds left to act',
                           'PtheProphet folds',
                           'JohnyyR raises to 40',
                           'Popp1987 has 15 seconds left to act',
                           'Popp1987 folds',
                           'Luckytobgood folds',
                           'FatalRevange raises to 100',
                           'IgaziFerfi folds',
                           'egis25 folds',
                           'gamblie folds',
                           'idanuTz1 folds',
                           'JohnyyR has 15 seconds left to act',
                           'JohnyyR calls 60')),
        ('turn', None),
        ('river', None),
        ('total_pot', Decimal(230)),
        ('show_down', False),
        ('winners', ('FatalRevange',)),
        ('board', (Card('8h'), Card('4h'), Card('Tc'))),
        ('extra', dict(tournament_name='MiniFTOPS Main Event',
                       turn_pot=None, turn_num_players=None,
                       river_pot=None, river_num_players=None)),
        ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value

    @pytest.mark.parametrize(('attribute', 'expected_value'), [
        ('actions', (('JohnyyR', Action.CHECK),
                     ('FatalRevange', Action.THINK),
                     ('FatalRevange', Action.BET, Decimal(120)),
                     ('JohnyyR', Action.FOLD),
                     ('FatalRevange', Action.RETURN, Decimal(120)),
                     ('FatalRevange', Action.MUCK),
                     ('FatalRevange', Action.WIN, Decimal(230)),
                     )
        ),
        ('cards', (Card('8h'), Card('4h'), Card('Tc'))),
        ('is_rainbow', False),
        ('is_monotone', False),
        ('is_triplet', False),
        # TODO: http://www.pokerology.com/lessons/flop-texture/
        # assert flop.is_dry
        ('has_pair', False),
        ('has_straightdraw', True),
        ('has_gutshot', True),
        ('has_flushdraw', True),
        ('players', ('JohnyyR', 'FatalRevange')),
        ('pot', Decimal(230))
    ])
    def test_flop_attributes(self, hand, attribute, expected_value):
        assert getattr(hand.flop, attribute) == expected_value

    def test_flop(self, hand):
        assert isinstance(hand.flop, _Flop)


class TestHandWithFlopTurnRiver:
    hand_text = ftp_hands.TURBO_SNG

    @pytest.mark.parametrize('attribute,expected_value',
        [('game_type', GameType.SNG),
         ('sb', Decimal(15)),
         ('bb', Decimal(30)),
         ('date', ET.localize(datetime(2014, 6, 29, 5, 57, 1))),
         ('game', Game.HOLDEM),
         ('limit', Limit.NL),
         ('ident', '34374264321'),
         ('tournament_ident', '268569961'),
         ('table_name', '1'),
         ('tournament_level', None),
         ('buyin', Decimal(10)),
         ('rake', None),
         ('currency', Currency.USD),
        ])
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize('attribute,expected_value',
        [('players', [
            _Player(name='snake 422', stack=1500, seat=1, combo=None),
            _Player(name='IgaziFerfi', stack=1500, seat=2, combo=Combo('5d2h')),
            _Player(name='MixaOne', stack=1500, seat=3, combo=None),
            _Player(name='BokkaBlake', stack=1500, seat=4, combo=None),
            _Player(name='Sajiee', stack=1500, seat=5, combo=None),
            _Player(name='AzzzJJ', stack=1500, seat=6, combo=None),
        ]),
        ('button', _Player(name='AzzzJJ', stack=1500, seat=6, combo=None)),
        ('max_players', 6),
        ('hero', _Player(name='IgaziFerfi', stack=1500, seat=2, combo=Combo('5d2h'))),
        ('preflop_actions', ('MixaOne calls 30',
                             'BokkaBlake folds',
                             'Sajiee folds',
                             'AzzzJJ raises to 90',
                             'snake 422 folds',
                             'IgaziFerfi folds',
                             'MixaOne calls 60',)
        ),
        ('turn', None),
        ('turn_actions', None),
        ('river', None),
        ('river_actions', None),
        ('total_pot', Decimal('285')),
        ('show_down', False),
        ('winners', ('AzzzJJ',)),
        ('board', (Card('6s'), Card('9c'), Card('3d'))),
        ('extra', dict(tournament_name='$10 Sit & Go (Turbo)',
                       turn_pot=None, turn_num_players=None,
                       river_pot=None, river_num_players=None)),
        ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value

    @pytest.mark.parametrize(('attribute', 'expected_value'), [
        ('actions', (('MixaOne', Action.BET, Decimal(30)),
                     ('AzzzJJ', Action.RAISE, Decimal(120)),
                     ('MixaOne', Action.FOLD),
                     ('AzzzJJ', Action.RETURN, Decimal(90)),
                     ('AzzzJJ', Action.MUCK),
                     ('AzzzJJ', Action.WIN, Decimal(285)),
                     )
        ),
        ('cards', (Card('6s'), Card('9c'), Card('3d'))),
        ('is_rainbow', True),
        ('is_monotone', False),
        ('is_triplet', False),
        # TODO: http://www.pokerology.com/lessons/flop-texture/
        # assert flop.is_dry
        ('has_pair', False),
        ('has_straightdraw', True),
        ('has_gutshot', True),
        ('has_flushdraw', False),
        ('players', ('MixaOne', 'AzzzJJ')),
        ('pot', Decimal(285))
    ])
    def test_flop_attributes(self, hand, attribute, expected_value):
        assert getattr(hand.flop, attribute) == expected_value

    def test_flop(self, hand):
        assert isinstance(hand.flop, _Flop)
