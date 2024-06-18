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
                opponent_players: List[lugo4py.Bot], distance: float):
    # Vê qual jogador adversário está mais perto e vai em direção a ele
    nearest_opponent = self.get_nearest_opponent(me.position, opponent_players,
                                                 distance)

    # Checa se achou algum jogador adversário
    if (nearest_opponent != None):
        print('TRYING TO MARK ', nearest_opponent.number)
        print('FOUND OPPONENT')
        # Vê se outro jogador já está marcando o mesmo jogador
        for player in my_team_players:
            if (player.number == me.number):
                continue

            for opponent in marked_players:
                if (opponent.number == nearest_opponent.number):
                    print('ALREADY MARKED')
                    return me.position

            # if (self.is_marking):
            #     if (player.markng_opponent.number == nearest_opponent.number):
            #         print('BBBBBBBBB')
            #         # Se já estiver marcando, não faz nada
            #         # TODO: futuramente, fazer algo pra ele não ficar parado
            #         return me.position

        # Indica qual oponente está sendo marcado
        marked_players.append(nearest_opponent)
        self.markng_opponent = nearest_opponent
        self.is_marking = True

        print('MARKING ATTACKER')

        # Se o oponente estiver sem marcação, vai em direção a ele
        return nearest_opponent.position


# Atualiza para NONE o estado de marcação
# Ou seja, não estará marcando ninguém
def stop_marking(self, me: lugo4py.Bot):
    me.markng_opponent = None
    print('STOPPED MARKING')
