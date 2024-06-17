import traceback
from abc import ABC
from typing import List
import traceback
import lugo4py
from lugo4py import Point
from settings import get_my_expected_position


# Marca os atacantes adversários que estão sem a bola e próximos do bot
# me -> jogador que está marcando
# opponent_players -> lista de jogadores adversários
# distance -> distância que define se um jogador está próximo ou não
def mark_player(self, inspector: lugo4py.GameSnapshotInspector,
                me: lugo4py.Bot, opponent_players: List[lugo4py.Bot],
                distance: int):
    # Vê qual jogador adversário está mais perto e vai em direção a ele
    nearest_opponent = self.get_nearest_opponent(me.position, opponent_players,
                                                 distance)
    if (nearest_opponent):
        inspector.make_order_move_max_speed(nearest_opponent.position)

    print('MARKING ATTACKER')
