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
                defense_col: int):
    # Vê qual jogador adversário está mais perto e vai em direção a ele
    nearest_opponent = self.get_nearest_opponent(me.position, opponent_players,
                                                 distance)

    # Checa se não achou algum jogador adversário
    if (not nearest_opponent):
        return None

    opponent_region = self.mapper.get_region_from_point(
        nearest_opponent.position)
    # Checa se o adversário está na zona de defesa
    print('OPPONENT REGION: ', opponent_region)

    if (opponent_region.col > defense_col):
        print('OPPONENT IS NOT IN DEFENSE REGION')
        return None

    print('OPPONENT IS IN DEFENSE REGION')
    return nearest_opponent.position


# Atualiza para NONE o estado de marcação
# Ou seja, não estará marcando ninguém
def stop_marking(self, me: lugo4py.Bot):
    me.markng_opponent = None
    print('STOPPED MARKING')
