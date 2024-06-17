###############################################################################
###############################################################################
#               Arquivo que contém funções getters e setters                  #
#                       Work on my_bot.py file                                #
###############################################################################
###############################################################################

import traceback
from abc import ABC
from typing import List
import traceback
import lugo4py
from lugo4py import Point
from settings import get_my_expected_position


# Retorna se algum jogador é ZAGUEIRO ou não
def is_defender(self, player: lugo4py.Player) -> bool:
    # Constante que define o maior número da camisa dos defensores
    DEFENDER_GREATEST_NUMBER = 5

    return player.number <= DEFENDER_GREATEST_NUMBER


# Obtém o oponente mais próximo dentro de um raio indicado pelo parâmetro nearest_distance
def get_nearest_opponent(self, my_position: Point,
                         opponent_players: List[lugo4py.Player],
                         nearest_distance: int) -> lugo4py.Player:
    for opponent in opponent_players:
        distance = lugo4py.geo.distance_between_points(my_position,
                                                       opponent.position)
        if (distance <= nearest_distance):
            return opponent
