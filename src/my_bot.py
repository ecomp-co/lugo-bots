import traceback
from abc import ABC
from typing import List
import traceback
import lugo4py
from lugo4py import Point
from settings import get_my_expected_position


class MyBot(lugo4py.Bot, ABC):
    def on_disputing(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:

            ball_position = inspector.get_ball().position

            # try the auto complete for reader.make_order_... there are other options
            move_order = inspector.make_order_move_max_speed(ball_position)

            # Try other methods to create Move Orders:
            # move_order = reader.make_order_move_by_direction(lugo4py.DIRECTION_FORWARD)
            # move_order = reader.make_order_move_from_vector(lugo4py.sub_vector(vector_a, vector_b))

            # we can ALWAYS try to catch the ball
            catch_order = inspector.make_order_catch()

            return [move_order, catch_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_defending(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            ball_position = inspector.get_ball().position
            bot_position = inspector.get_me().position
            my_region = self.mapper.get_region_from_point(inspector.get_ball().position)
            my_region2 = self.mapper.get_region_from_point(inspector.get_me().position)
            bots_moving_to_ball = 0
            my_goal = inspector.get_my_team().players


            # for player in my_goal:
            #     if self.is_near_ball(my_region, my_region2, 2):
            #         bots_moving_to_ball += 1
                    

            # for bot in inspector.get_teammates():
            #     if bots_moving_to_ball < 2:
            #         # Se houver menos de 2 bots indo para a bola, o bot atual pode ir
            #         if self.is_near_ball(my_region, my_region2, 10):
            #             catch_order = inspector.make_order_catch()
            #             target_position = ball_position
            #             move_order = inspector.make_order_move_max_speed(target_position)
            #             bots_moving_to_ball += 1
            #             return [catch_order,move_order]
            #         else:
            #             # Caso contrário, permanece na defesa
            #             move_order = inspector.make_order_move_max_speed(bot.position)
            #             return [move_order]
            #     else:
            #         # Se já houver 2 bots indo para a bola, os outros permanecem na defesa
            #             move_order = inspector.make_order_move_max_speed(bot.position)
            #             return [move_order]
            #     print("AQUIUAUUQUIQUUAIIQUQUQUUQUIQUQUUQUWSUQUUQSUQSUQUUSUIQUQSUUUQSUQUUQUSQUSUQUQSUUSUQSUQUSUQSUSQU",bots_moving_to_ball)

            if self.is_near_ball(my_region, my_region2, 1):
                # Se estiver perto da bola, tenta capturá-la
                target_position = ball_position
                move_order = inspector.make_order_move_max_speed(target_position)
                catch_order = inspector.make_order_catch()
                return [catch_order,move_order]
            else:
                # Supondo que inspector.get_my_team().players retorna uma lista de objetos de jogador
                my_goal = inspector.get_my_team().players
                move_dest = get_my_expected_position(inspector, self.mapper, self.number)
                move_order = inspector.make_order_move_max_speed(move_dest)
                # Iterando sobre a lista de jogadores
                for jogador in my_goal:
                    # Acessando informações sobre cada jogador
                    print("Número:", jogador.number)
                    print("Posição (x, y):", jogador.position.x, jogador.position.y)
                    print("Velocidade (direção):", jogador.velocity.direction)
                    # Imprima outras informações que você deseja acessar sobre o jogador
                return [move_order]
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            opponent_goal_point = self.mapper.get_attack_goal().get_center()
            print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOl",opponent_goal_point)  # Corrigido para get_center()
            goal_region = self.mapper.get_region_from_point(opponent_goal_point)
            my_region = self.mapper.get_region_from_point(inspector.get_me().position)

            # specific_target_point = Point(12500, 8500) 
            # print("CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASSSSSSSSSSSSSSSSSSSIIIIIIIIIIIIIIIIIIOOOOOOOOOOOOO",specific_target_point.get_center()) # Substitua x_coordinate e y_coordinate pelos valores desejados

            my_move = inspector.make_order_move_max_speed(opponent_goal_point)

            if self.is_near(my_region, goal_region):
                my_order = inspector.make_order_kick_max_speed(opponent_goal_point)  # Corrigido para opponent_goal_point
            else:
                my_order = inspector.make_order_move_max_speed(opponent_goal_point)  # Corrigido para opponent_goal_point

            return [my_order, my_move]

        except Exception as e:
            print(f'did not play this turn due to exception. {e}')
            traceback.print_exc()

    def on_supporting(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            ball_holder_position = inspector.get_ball().position

            # "point" is an X and Y raw coordinate referenced by the field, so the side of the field matters!
            # "region" is a mapped area of the field create by your mapper! so the side of the field DO NOT matter!
            ball_holder_region = self.mapper.get_region_from_point(ball_holder_position)
            my_region = self.mapper.get_region_from_point(inspector.get_me().position)

            # if self.is_near(ball_holder_region, my_region):
            move_dest = get_my_expected_position(inspector, self.mapper, self.number)
            # else:
            #     move_dest = ball_holder_position

            move_order = inspector.make_order_move_max_speed(move_dest)
            return [move_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def as_goalkeeper(self, inspector: lugo4py.GameSnapshotInspector, state: lugo4py.PLAYER_STATE) -> List[lugo4py.Order]:
        try:
            position = inspector.get_ball().position

            if state != lugo4py.PLAYER_STATE.DISPUTING_THE_BALL:
                position = self.mapper.get_attack_goal().get_center()

            my_order = inspector.make_order_move_max_speed(position)

            return [my_order, inspector.make_order_catch()]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def getting_ready(self, snapshot: lugo4py.GameSnapshot):
        print('getting ready')

    def is_near(self, region_origin: lugo4py.mapper.Region, dest_origin: lugo4py.mapper.Region) -> bool:
        max_distance = 1
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance
    
    def is_near_ball(self, region_origin: lugo4py.mapper.Region, dest_origin: lugo4py.mapper.Region, max_distance: int) -> bool:
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance
    
    def move_towards_goal(self, position: lugo4py.Point, goal_position: lugo4py.Point) -> lugo4py.Order:
    # Move em direção ao nosso gol
        direction_to_goal = lugo4py.Point(goal_position.x - position.x, goal_position.y - position.y)
        target_position = lugo4py.Point(position.x + direction_to_goal.x, position.y + direction_to_goal.y)
        return inspector.make_order_move_max_speed(target_position)

