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

# Constante que define o maior número da camisa dos defensores
DEFENDER_GREATEST_NUMBER = 5
# Constante que define o maior número da camisa dos meio-campistas
MIDFIELDER_GREATEST_NUMBER = 10


# Retorna se algum jogador é ZAGUEIRO ou não
def is_defender(self, player: lugo4py.Player) -> bool:
    return player.number <= DEFENDER_GREATEST_NUMBER


# Retorna se algum jogador é MEIO-CAMPISTA ou não
def is_midfielder(self, player: lugo4py.Player) -> bool:

    return player.number > DEFENDER_GREATEST_NUMBER and player.number <= MIDFIELDER_GREATEST_NUMBER


# Obtém o oponente mais próximo dentro de um raio indicado pelo parâmetro nearest_distance
def get_nearest_opponent(self, my_position: Point,
                         opponent_players: List[lugo4py.Player],
                         nearest_distance: float) -> lugo4py.Player:
    print('GETTING NEAREST OPPONENT')
    for opponent in opponent_players:
        distance = lugo4py.geo.distance_between_points(my_position,
                                                       opponent.position)

        print('DISTANCE from opponent: ', distance, 'opp number: ',
              opponent.number)
        if (distance <= nearest_distance):
            print('NEAREST OPPONENT FOUND')
            print('NEAREST OPPONENT: ', opponent.number)
            return opponent


def get_opponents_in_range(self, my_position: Point,
                           opponent_players: List[lugo4py.Player],
                           field_cols_range: range) -> List[lugo4py.Player]:

    opponents_in_range = []

    for opponent in opponent_players:
        opponent_region = self.mapper.get_region_from_point(opponent.position)
        if (opponent_region.col in field_cols_range):
            opponents_in_range.append(opponent)

    return opponents_in_range


# TODO Futuramente da pra fazer isso retornar o teammate mais perto e ver se ele está marcando esse oponente em específico
# BUG e realmente ta dando uma falha de um teammate ficar entre 2 adversários e ninguém ir ajudar por não saber qual dos 2 ele ta marcando
def is_any_teammate_next_to_opponent(self, my_position: Point,
                                     my_team_players: List[lugo4py.Player],
                                     opponent: lugo4py.Player) -> bool:
    # Calculate my distance from oppponent
    my_distance = lugo4py.geo.distance_between_points(my_position,
                                                      opponent.position)

    for teammate in my_team_players:
        teammate_distance = lugo4py.geo.distance_between_points(
            opponent.position, teammate.position)

        if (teammate_distance < my_distance):
            return False
