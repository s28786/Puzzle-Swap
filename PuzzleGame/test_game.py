# Description: Unit tests for the Sokoban game class
from packages.mongodb import get_level
from packages.game import Sokoban, Cell

# Mocking the get_level function
level = {
    'player': [1, 1],
    'boxes': [
        [2, 3],
        [3, 2]
    ],
    'goals': [
        [3, 4],
        [3, 5]
    ],
    'map': [
        [1, 1, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
}
sokoban = Sokoban(None, None)


def set_mock_data():
    global sokoban
    sokoban = Sokoban(None, None)
    sokoban.player_name = 'player'
    sokoban.map = level.get('map')
    for i in range(len(sokoban.map)):
        # convert to string also
        sokoban.map[i] = [str(x) for x in sokoban.map[i]]
    sokoban.player = Cell(level.get('player')[0], level.get('player')[1], 'player')
    for box in level.get('boxes'):
        sokoban.boxes.append(Cell(box[0], box[1], 'box'))
    for goal in level.get('goals'):
        sokoban.goals.append(Cell(goal[0], goal[1], 'goal'))


def test_initial_player_position():
    set_mock_data()
    assert sokoban.get_player_coordinates() == [1, 1]


def test_initial_box_positions():
    set_mock_data()
    assert sokoban.get_box_coordinates() == [[2, 3], [3, 2]]


def test_initial_goal_positions():
    set_mock_data()
    assert sokoban.get_goal_coordinates() == [[3, 4], [3, 5]]


def test_move_player_to_empty_space():
    set_mock_data()
    sokoban.player = Cell(1, 1, 'player')
    sokoban.try_to_move('right')
    assert sokoban.get_player_coordinates() == [1, 2]


def test_move_player_to_wall():
    set_mock_data()
    sokoban.player = Cell(1, 1, 'player')
    sokoban.try_to_move('up')
    assert sokoban.get_player_coordinates() == [1, 1]


def test_move_player_and_push_box():
    set_mock_data()
    sokoban.player = Cell(1, 1, 'player')
    sokoban.make_turn('right')
    sokoban.make_turn('right')
    sokoban.make_turn('down')
    assert sokoban.get_player_coordinates() == [2, 3]
    assert sokoban.get_box_coordinates() == [[3, 3], [3, 2]]


def test_move_box_to_wall():
    set_mock_data()
    sokoban.player = Cell(1, 1, 'player')
    sokoban.make_turn('right')
    sokoban.make_turn('right')
    sokoban.make_turn('down')
    sokoban.make_turn('down')
    assert sokoban.get_player_coordinates() == [2, 3]
    assert sokoban.get_box_coordinates() == [[3, 3], [3, 2]]


def test_move_box_to_goal():
    set_mock_data()
    sokoban.player = Cell(1, 1, 'player')
    sokoban.make_turn('down')
    sokoban.make_turn('down')
    sokoban.make_turn('right')
    sokoban.make_turn('right')
    assert sokoban.get_player_coordinates() == [3, 3]
    assert sokoban.get_box_coordinates()[1] == sokoban.get_goal_coordinates()[0]


def test_check_win():
    set_mock_data()
    sokoban.player = Cell(1, 1, 'player')
    sokoban.make_turn('down')
    sokoban.make_turn('down')
    sokoban.make_turn('right')
    sokoban.make_turn('right')
    sokoban.make_turn('right')
    sokoban.make_turn('left')
    sokoban.make_turn('left')
    sokoban.make_turn('left')
    sokoban.make_turn('up')
    sokoban.make_turn('up')
    sokoban.make_turn('right')
    sokoban.make_turn('right')
    sokoban.make_turn('down')
    sokoban.make_turn('up')
    sokoban.make_turn('left')
    sokoban.make_turn('left')
    sokoban.make_turn('down')
    sokoban.make_turn('down')
    sokoban.make_turn('right')
    win_status, _, _ = sokoban.make_turn('right')
    assert win_status == True
