###############################################################################
###############################################################################
#         Arquivo que contém funções que faz o bot realizar ações             #
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

marked_players = []


# Marca os atacantes adversários que estão sem a bola e próximos do bot
# me -> jogador que está marcando
# opponent_players -> lista de jogadores adversários
# distance -> distância que define se um jogador está próximo ou não
def mark_player(self, inspector: lugo4py.GameSnapshotInspector,
                me: lugo4py.Bot, my_team_players: List[lugo4py.Bot],
                opponent_players: List[lugo4py.Bot], distance: float,
                defense_range: range):
    # Vê qual jogador adversário está mais perto e vai em direção a ele
    nearest_opponent = self.get_nearest_opponent(me.position, opponent_players,
                                                 distance)

    # Checa se não achou algum jogador adversário
    if (not nearest_opponent):
        return None

    my_distance = lugo4py.geo.distance_between_points(
        nearest_opponent.position, me.position)

    # Se tiver um amigo muito próximo, não marca
    for teammate in my_team_players:
        teammate_distance = lugo4py.geo.distance_between_points(
            nearest_opponent.position, teammate.position)

        if (teammate_distance < my_distance):
            return None

    opponent_region = self.mapper.get_region_from_point(
        nearest_opponent.position)
    # Checa se o adversário está na zona de defesa
    print('OPPONENT REGION: ', opponent_region)

    # Checa se o adversário não está na range da zona de defesa
    if (opponent_region.col not in defense_range):
        print('OPPONENT IS NOT IN DEFENSE REGION')
        return None

    # Se o adversário está com a bola, vai na direção da bola
    if (nearest_opponent == inspector.get_ball_holder()):
        return inspector.get_ball().position

    print('OPPONENT IS IN DEFENSE REGION')
    return nearest_opponent.position


# Atualiza para NONE o estado de marcação
# Ou seja, não estará marcando ninguém
def stop_marking(self, me: lugo4py.Bot):
    me.markng_opponent = None
    print('STOPPED MARKING')
