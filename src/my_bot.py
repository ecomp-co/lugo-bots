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

            if self.should_i_help(get_my_expected_position(inspector, self.mapper, self.number), inspector.get_my_team_players(), ball_position, 2):
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

    def on_defending(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            ball_position = inspector.get_ball().position
            ball_region = self.mapper.get_region_from_point(inspector.get_ball().position)
            my_region = self.mapper.get_region_from_point(inspector.get_me().position)
            my_goal = inspector.get_my_team().players

            if self.should_i_help(inspector.get_me().position, inspector.get_my_team_players(), ball_position, 2):
                move_order = inspector.make_order_move_max_speed(ball_position)

            # move_order = inspector.make_order_move_max_speed(move_dest)
            catch_order = inspector.make_order_catch()
            return [catch_order, move_order]
            
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            opponent_goal_point = self.mapper.get_attack_goal().get_center()
            opponent_goal_region = self.mapper.get_region_from_point(opponent_goal_point)
            my_goal_point = self.mapper.get_defense_goal().get_center()
            my_goal_region = self.mapper.get_region_from_point(my_goal_point)
            my_region = self.mapper.get_region_from_point(inspector.get_me().position)

            my_move = inspector.make_order_move_max_speed(opponent_goal_point)

            if self.is_near(my_region, opponent_goal_region, 1):
                my_order = inspector.make_order_kick_max_speed(Point(20000,3600))
            else:
                my_order = inspector.make_order_move_max_speed(opponent_goal_point)

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
            my_team = inspector.get_my_team_players()
            position = inspector.get_ball().position
            alliedNumber4 = inspector.get_player(inspector.get_my_team_side(), 4); 


            if state != lugo4py.PLAYER_STATE.DISPUTING_THE_BALL:
                position = self.mapper.get_attack_goal().get_center()

            my_order = inspector.make_order_move_max_speed(position)

            # Try to kick to a player when the ball is on goalkeepers hold
            if state == lugo4py.PLAYER_STATE.HOLDING_THE_BALL:
                my_order = inspector.make_order_kick_max_speed(alliedNumber4.position)

            return [my_order, inspector.make_order_catch()]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def getting_ready(self, snapshot: lugo4py.GameSnapshot):
        print('getting ready')

    def is_near(self, region_origin: lugo4py.mapper.Region, dest_origin: lugo4py.mapper.Region, max_distance: int) -> bool:
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance
    
    ########################
    ### Custom functions ###
    ########################

    def should_i_help(self, my_position: Point, my_team, target_position: Point, max_helpers: int):
        nearest_players = 0
        my_distance = lugo4py.geo.distance_between_points(my_position, target_position)

        for teamMate in my_team:
            if teamMate.number != self.number:
                distance = lugo4py.geo.distance_between_points(teamMate.position, target_position)
                if distance < my_distance:
                    nearest_players += 1
                    if nearest_players >= max_helpers:
                        return False
        return True
    
    def opponent_is_near(self, opponent_team, region_origin: lugo4py.mapper.Region, max_distance) -> bool:
        for player in opponent_team:
            dest_origin = self.mapper.get_region_from_point(player.position)
            if region_origin.get_row() - dest_origin.get_row() <= max_distance and region_origin.get_col() - dest_origin.get_col() <= max_distance:
                return True
        return False