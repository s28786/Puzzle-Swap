import copy
from .mongodb import get_level


class Cell:
    def __init__(self, row, col, status):
        self.row = row
        self.col = col
        self.status = status  # 'box' 'player' 'goal'

    def __setstatus__(self, status):
        self.status = status

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def get_coordinates(self):
        return [self.row, self.col]

    def set_coordinates(self, row, col):
        self.row = row
        self.col = col

    def print_object(self):
        print(self.row, self.col, self.status)


class Sokoban:
    player_name = ''
    map = []
    boxes = []
    goals = []
    player = None
    moves = 0

    def __init__(self, player_name, level_id):
        self.player = None
        self.map = []
        self.boxes = []
        self.goals = []
        self.moves = 0
        if player_name is not None:
            self.player_name = player_name
        if level_id is not None:
            self.load_level(level_id)

    def load_level(self, level_id):

        level = get_level(level_id)

        self.map = level.get('map')

        for i in range(len(self.map)):
            # convert to string also
            self.map[i] = [str(x) for x in self.map[i]]
        self.player = Cell(level.get('player')[0], level.get('player')[1], 'player')
        for box in level.get('boxes'):
            self.boxes.append(Cell(box[0], box[1], 'box'))
        for goal in level.get('goals'):
            self.goals.append(Cell(goal[0], goal[1], 'goal'))

    def try_to_move(self, direction):
        new_row = self.player.row
        new_col = self.player.col
        if direction == 'up':
            new_row -= 1
        elif direction == 'down':
            new_row += 1
        elif direction == 'left':
            new_col -= 1
        else:
            new_col += 1

        if self.map[new_row][new_col] == '1':
            return False
        for box in self.boxes:
            if box.row == new_row and box.col == new_col:
                if direction == 'up':
                    if self.map[new_row - 1][new_col] == '1':
                        return False
                    for box2 in self.boxes:
                        if box2.row == new_row - 1 and box2.col == new_col:
                            return False
                    box.row -= 1
                elif direction == 'down':

                    if self.map[new_row + 1][new_col] == '1':
                        return False
                    for box2 in self.boxes:
                        if box2.row == new_row + 1 and box2.col == new_col:
                            return False
                    box.row += 1
                elif direction == 'left':
                    if self.map[new_row][new_col - 1] == '1':
                        return False
                    for box2 in self.boxes:
                        if box2.row == new_row and box2.col == new_col - 1:
                            return False
                    box.col -= 1
                else:
                    if self.map[new_row][new_col + 1] == '1':
                        return False
                    for box2 in self.boxes:
                        if box2.row == new_row and box2.col == new_col + 1:
                            return False
                    box.col += 1
                break
        self.player.set_coordinates(new_row, new_col)
        self.moves += 1
        return True

    def check_win(self):
        for goal in self.goals:
            box_on_goal = False
            for box in self.boxes:
                if box.row == goal.row and box.col == goal.col:
                    box_on_goal = True
                    break
            if not box_on_goal:
                return False
        return True

    def make_turn(self, direction):
        if self.try_to_move(direction):
            if self.check_win():
                return True, self.get_return_board(), self.moves
        else:
            return False, self.get_return_board(), self.moves

    def get_return_board(self):
        # deep copy of the map
        return_board = copy.deepcopy(self.map)
        for i in range(len(return_board)):
            for j in range(len(return_board[i])):
                if self.player.row == i and self.player.col == j:
                    return_board[i][j] = '2'
                else:
                    box = False
                    for b in self.boxes:
                        if b.row == i and b.col == j:
                            return_board[i][j] = '3'
                            box = True
                            break
                    if not box:
                        goal = False
                        for goal in self.goals:
                            if goal.row == i and goal.col == j:
                                return_board[i][j] = '4'
                                goal = True
                                break
                        if not goal:
                            if return_board[i][j] == '1':
                                return_board[i][j] = '1'
                            else:
                                return_board[i][j] = '0'

        return return_board

    def get_box_coordinates(self):
        box_coordinates = []
        for box in self.boxes:
            box_coordinates.append([box.row, box.col])
        return box_coordinates

    def get_goal_coordinates(self):
        goal_coordinates = []
        for goal in self.goals:
            goal_coordinates.append([goal.row, goal.col])
        return goal_coordinates

    def get_player_coordinates(self):
        return self.player.get_coordinates()

    def get_wall_coordinates(self):
        wall_coordinates = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == '1':
                    wall_coordinates.append([i, j])
        return wall_coordinates
