import lugo4py
import lugo4py.mapper as mapper

# yapf: disable # desabilita formatador nesse arquivo

# MAPPER_COLS and MAPPER_ROWS define the number of regions on the field.
# great values leads to more precision
# Use this tool to help you to decide about it https://github.com/mauriciorobertodev/strategy-creator-lugo-bots
MAPPER_COLS = 10
MAPPER_ROWS = 6

# Example how to create your custom initial positions
# Parece que isso aqui não ta mudando a posição inicial:
PLAYER_INITIAL_POSITIONS = {
            2: {'Col': 2, 'Row': 1},
            3: {'Col': 2, 'Row': 2},
            4: {'Col': 2, 'Row': 3},
            5: {'Col': 2, 'Row': 4},
            6: {'Col': 3, 'Row': 1},
            7: {'Col': 3, 'Row': 2},
            8: {'Col': 4, 'Row': 1},
            9: {'Col': 4, 'Row': 4},
            10: {'Col': 5, 'Row': 3},
            11: {'Col': 5, 'Row': 2},
 }

def get_my_expected_position(inspector: lugo4py.GameSnapshotInspector, my_mapper: mapper.Mapper, number: int):
    mapper_cols = MAPPER_COLS

    player_tactic_positions = {
        'DEFENSIVE': {
            2: {'Col': 0, 'Row': 1},
            3: {'Col': 0, 'Row': 2},
            4: {'Col': 0, 'Row': 3},
            5: {'Col': 0, 'Row': 4},
            6: {'Col': 1, 'Row': 1},
            7: {'Col': 1, 'Row': 2},
            8: {'Col': 1, 'Row': 3},
            9: {'Col': 1, 'Row': 4},
            10: {'Col': 1, 'Row': 3},
            11: {'Col': 4, 'Row': 2},
        },
        'NORMAL': {
            2: {'Col': 2, 'Row': 1},
            3: {'Col': 2, 'Row': 2},
            4: {'Col': 2, 'Row': 3},
            5: {'Col': 2, 'Row': 4},
            6: {'Col': 3, 'Row': 1},
            7: {'Col': 3, 'Row': 2},
            8: {'Col': 4, 'Row': 1},
            9: {'Col': 4, 'Row': 4},
            10: {'Col': 5, 'Row': 3},
            11: {'Col': 5, 'Row': 2},
        },
        'OFFENSIVE': {
            2: {'Col': 3, 'Row': 1},
            3: {'Col': 3, 'Row': 2},
            4: {'Col': 3, 'Row': 3},
            5: {'Col': 3, 'Row': 4},
            6: {'Col': 4, 'Row': 1},
            7: {'Col': 4, 'Row': 2},
            8: {'Col': 4, 'Row': 1},
            9: {'Col': 4, 'Row': 4},
            10: {'Col': 4, 'Row': 3},
            11: {'Col': 5, 'Row': 2},
        }
    }

    ball_region = my_mapper.get_region_from_point(inspector.get_ball().position)
    field_third = mapper_cols / 3
    ball_cols = ball_region.get_col()

    team_state = "OFFENSIVE"
    if ball_cols < field_third:
        team_state = "DEFENSIVE"
    elif ball_cols < field_third * 2:
        team_state = "NORMAL"

    expected_region = my_mapper.get_region(player_tactic_positions[team_state][number]['Col'],
                                           player_tactic_positions[team_state][number]['Row'])
    return expected_region.get_center()
