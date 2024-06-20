import traceback
from abc import ABC
from typing import List
import lugo4py
from lugo4py import Point
from settings import get_my_expected_position

# Importação de funções customizadas
# Ações
from custom.actions import *

# Getters e setters
from custom.getters_setters import *

DEFENSE_COL = 2
MIDFIELD_COL = 4

class MyBot(lugo4py.Bot, ABC):

    is_marking = False
    marking_player = None

    def on_disputing(
            self,
            inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:

            ball_position = inspector.get_ball().position

            # try the auto complete for reader.make_order_... there are other options
            # BUG isso depende da posição da bola, pq se ela tiver perto do nosso gol, nossos jogadores param de marcar e vão pra cima da bola, deixando varios adversários livres
            if self.should_i_help(
                    get_my_expected_position(inspector, self.mapper,
                                             self.number),
                    inspector.get_my_team_players(), ball_position, 2):
                move_order = inspector.make_order_move_max_speed(ball_position)
            # move_order = inspector.make_order_move_max_speed(ball_position)

            # Try other methods to create Move Orders:
            # move_order = reader.make_order_move_by_direction(lugo4py.DIRECTION_FORWARD)
            # move_order = reader.make_order_move_from_vector(lugo4py.sub_vector(vector_a, vector_b))

            # we can ALWAYS try to catch the ball
            catch_order = inspector.make_order_catch()

            return [move_order, catch_order]
        
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_defending(
            self,
            inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            orders = self.try_to_catch_ball(inspector)
            if orders:
                return orders

            # Nosso time
            my_players = inspector.get_my_team_players()
            me = inspector.get_me()

            # Posições
            ball_position = inspector.get_ball().position
            ball_region = self.mapper.get_region_from_point(
                inspector.get_ball().position)
            my_region = self.mapper.get_region_from_point(
                inspector.get_me().position)
            my_goal = inspector.get_my_team().players

            # Time adversário
            opponent_players = inspector.get_opponent_players()
            print('DEFENDING')

            move_dest = None
            move_order = None

            # Checa se é zagueiro
            if (self.is_defender(me)):
                print('IS A DEFENDER')
                print('MRKING')
                move_dest = self.mark_player(inspector, me, my_players,
                                             opponent_players, 1000,
                                             range(0, DEFENSE_COL + 1))

                # Checa se há algum adversário livre perto do gol caso não
                # esteja marcando ninguém
                # Selecionando somente zagueiros para não puxar um meio
                # campista lá da frente para a linha de fundo
                if (not move_dest):
                    opponents_in_range = self.get_opponents_in_range(
                        me.position, opponent_players,
                        range(0, DEFENSE_COL + 1))
                    if (opponents_in_range):
                        if (
                                not self.is_any_teammate_next_to_opponent(
                                    me.position, my_players,
                                    opponents_in_range[0])
                        ):  # TODO ao invés de pegar só o de índice 0 tem que pegar o mais próximo de mim, e que ao mesmo tempo ta mais longe dos outros
                            move_dest = opponents_in_range[0].position

            # Checa se é meio-campista
            elif (self.is_midfielder(me)):
                print('IS A MIDFIELDER')
                move_dest = self.mark_player(
                    inspector, me, my_players, opponent_players, 1000,
                    range(DEFENSE_COL, MIDFIELD_COL + 1))

            # Pressiona jogador com a bola
            if self.should_i_help(inspector.get_me().position,
                                  inspector.get_my_team_players(),
                                  ball_position, 2):
                print('HELPING')
                move_dest = ball_position

            # Se move_dest não tiver sido definido, então não retorna nenhuma ordem para
            # evitar erros no turno
            #if (not move_dest and not move_order):
            #    return

            if move_dest:
                move_order = inspector.make_order_move_max_speed(move_dest)

            if (lugo4py.geo.distance_between_points(me.position, ball_position)
                    < 500):
                catch_order = inspector.make_order_catch()
                return [catch_order, move_order]

            if (not move_order):
                return

            return [move_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(
            self,
            inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            me = inspector.get_me()
            my_position = me.position
            opponent_goal_point = self.mapper.get_attack_goal().get_center()
            opponent_goal_region = self.mapper.get_region_from_point(opponent_goal_point)
            my_region = self.mapper.get_region_from_point(my_position)
            
            # Verifica se algum oponente está muito próximo
            close_opponents = self.get_opponents_very_close(my_position, inspector.get_opponent_players(), 500)
            if close_opponents:
                # Encontra o companheiro de equipe mais próximo
                nearest_teammate = self.get_nearest_teammate(inspector.get_my_team_players(), my_position)
                if nearest_teammate:
                    # Passa a bola para o companheiro de equipe mais próximo
                    pass_order = inspector.make_order_kick_max_speed(nearest_teammate.position)
                    return [pass_order]

            # Se não houver oponentes muito próximos, continua movendo para o gol adversário
            my_move = inspector.make_order_move_max_speed(opponent_goal_point)
            if self.is_near(my_region, opponent_goal_region, 1):
                my_order = inspector.make_order_kick_max_speed(
                    Point(opponent_goal_point.x,
                          (opponent_goal_point.y - 1350)))
            else:
                my_order = inspector.make_order_move_max_speed(opponent_goal_point)

            return [my_order, my_move]

        except Exception as e:
            print(f'did not play this turn due to exception. {e}')
            traceback.print_exc()

    def on_supporting(
            self,
            inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            orders = self.try_to_catch_ball(inspector)
            if orders:
                return orders

            me = inspector.get_me()
            ball_position = inspector.get_ball().position
            opponent_goal_point = self.mapper.get_attack_goal().get_center()

            # Se é meio-campista e a bola está no campo de ataque, move-se para atacar
            if self.is_midfielder(me) and self.is_ball_in_attack_area(inspector):
                move_order = inspector.make_order_move_max_speed(opponent_goal_point)
            else:
                move_dest = get_my_expected_position(inspector, self.mapper, self.number)
                move_order = inspector.make_order_move_max_speed(move_dest)

            return [move_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def as_goalkeeper(self, inspector: lugo4py.GameSnapshotInspector,
                      state: lugo4py.PLAYER_STATE) -> List[lugo4py.Order]:
        try:
            my_team = inspector.get_my_team_players()
            position = inspector.get_ball().position
            alliedNumber4 = inspector.get_player(inspector.get_my_team_side(),
                                                 4)

            if state != lugo4py.PLAYER_STATE.DISPUTING_THE_BALL:
                position = self.mapper.get_attack_goal().get_center()

            my_order = inspector.make_order_move_max_speed(position)

            if state == lugo4py.PLAYER_STATE.HOLDING_THE_BALL:
                my_order = inspector.make_order_kick_max_speed(
                    alliedNumber4.position)

            return [my_order, inspector.make_order_catch()]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def getting_ready(self, snapshot: lugo4py.GameSnapshot):
        print('getting ready')

    def is_near(self, region_origin: lugo4py.mapper.Region,
                dest_origin: lugo4py.mapper.Region, max_distance: int) -> bool:
        return abs(region_origin.get_row() -
                   dest_origin.get_row()) <= max_distance and abs(
                       region_origin.get_col() -
                       dest_origin.get_col()) <= max_distance

    ########################
    ### Custom functions ###
    ########################

    def should_i_help(self, my_position: Point, my_team,
                      target_position: Point, max_helpers: int):
        nearest_players = 0
        my_distance = lugo4py.geo.distance_between_points(
            my_position, target_position)

        for teamMate in my_team:
            if teamMate.number != self.number:
                distance = lugo4py.geo.distance_between_points(
                    teamMate.position, target_position)
                if distance < my_distance:
                    nearest_players += 1
                    if nearest_players >= max_helpers:
                        return False
        return True

    def opponent_is_near(self, opponent_team,
                         region_origin: lugo4py.mapper.Region,
                         max_distance) -> bool:
        for player in opponent_team:
            dest_origin = self.mapper.get_region_from_point(player.position)
            if region_origin.get_row() - dest_origin.get_row(
            ) <= max_distance and region_origin.get_col(
            ) - dest_origin.get_col() <= max_distance:
                return True
        return False

    def get_nearest_teammate(self, my_team, my_position: Point):
        nearest_teammate = None
        nearest_distance = float('inf')
        for teammate in my_team:
            if teammate.number != self.number:
                distance = lugo4py.geo.distance_between_points(teammate.position, my_position)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_teammate = teammate
        return nearest_teammate

    def get_opponents_very_close(self, my_position: Point, opponent_team, max_distance: int):
        close_opponents = []
        for opponent in opponent_team:
            distance = lugo4py.geo.distance_between_points(opponent.position, my_position)
            if distance < max_distance:
                close_opponents.append(opponent)
        return close_opponents

    def mark_player(self, inspector: lugo4py.GameSnapshotInspector, me,
                    my_players, opponent_players, max_distance,
                    range_defense_columns):
        for opponent in opponent_players:
            opponent_region = self.mapper.get_region_from_point(
                opponent.position)
            if (opponent_region.get_col() in range_defense_columns and lugo4py.geo.distance_between_points(
                    me.position, opponent.position) < max_distance and not self
                    .is_any_teammate_next_to_opponent(me.position, my_players,
                                                      opponent)):
                self.is_marking = True
                self.marking_player = opponent
                return opponent.position

    def is_any_teammate_next_to_opponent(self, my_position, my_players,
                                         opponent):
        my_distance = lugo4py.geo.distance_between_points(my_position,
                                                          opponent.position)
        for player in my_players:
            if player.number != self.number:
                distance = lugo4py.geo.distance_between_points(
                    player.position, opponent.position)
                if distance < my_distance:
                    return True
        return False

    def get_opponents_in_range(self, my_position: Point, opponent_team,
                               range_defense_columns) -> List[lugo4py.Player]:
        near_opponents = []
        for opponent in opponent_team:
            opponent_region = self.mapper.get_region_from_point(
                opponent.position)
            if (opponent_region.get_col() in range_defense_columns):
                near_opponents.append(opponent)
        return near_opponents

    def get_opponent_to_mark(self, player_positions, opponent_positions,
                             my_position):
        for opponent_position in opponent_positions:
            if lugo4py.geo.distance_between_points(
                    my_position,
                    opponent_position) < 1000 and not self.is_any_teammate_next_to_opponent(
                        my_position, player_positions, opponent_position):
                return opponent_position

    def is_defender(self, player):
        return player.number in range(1, 5)

    def is_midfielder(self, player):
        return player.number in range(5, 8)

    def try_to_catch_ball(
            self,
            inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        me = inspector.get_me()
        ball_position = inspector.get_ball().position
        my_team = inspector.get_my_team_players()
        
        # Verifica se este bot é o mais próximo da bola
        if self.is_nearest_to_ball(me, ball_position, my_team):
            move_order = inspector.make_order_move_max_speed(ball_position)
            catch_order = inspector.make_order_catch()
            return [move_order, catch_order]
        return []
    
    def calculate_pass_speed(distance: float) -> float:
        if distance > 1500:  # Se a distância for maior que 1500, usa velocidade máxima
            return 1.0  # Velocidade máxima
        else:
            return 0.5  # Velocidade média


    def is_nearest_to_ball(self, me, ball_position: Point, my_team) -> bool:
        my_distance = lugo4py.geo.distance_between_points(me.position, ball_position)
        for teammate in my_team:
            if teammate.number != self.number:
                distance = lugo4py.geo.distance_between_points(teammate.position, ball_position)
                if distance < my_distance:
                    return False
        return True

    def is_ball_in_attack_area(self, inspector: lugo4py.GameSnapshotInspector) -> bool:
        ball_region = self.mapper.get_region_from_point(inspector.get_ball().position)
        attack_goal_region = self.mapper.get_region_from_point(self.mapper.get_attack_goal().get_center())
        return ball_region.get_col() >= attack_goal_region.get_col()

#######################################################
# Define funções customs que estão em outros arquivos #
#######################################################

############### Actions ################
# Adiciona a função mark_player ao MyBot
MyBot.mark_player = mark_player

########## Getters e setters ###########
# Adiciona a função is_defender ao MyBot
MyBot.is_defender = is_defender
# Adiciona a função is_midfielder ao MyBot
MyBot.is_midfielder = is_midfielder

# Adiciona a função get_nearest_opponent ao MyBot
MyBot.get_nearest_opponent = get_nearest_opponent
# Adiciona a função get_opponents_in_range ao MyBot
MyBot.get_opponents_in_range = get_opponents_in_range
# Adiciona a função is_any_teammate_next_to_opponent ao MyBot
MyBot.is_any_teammate_next_to_opponent = is_any_teammate_next_to_opponent
