from flask import Flask, render_template, request, jsonify, redirect, url_for
from packages.mongodb import load_levels, get_number_of_levels, insert_level_record_data, \
    get_all_record_for_a_level_ranked
from packages.game import Sokoban

app = Flask(__name__)

load_levels()

player_name = ''
game = None  # Initialize
in_game = False
current_level_id = 0


# try:
#     create_collection()
#
# except KeyboardInterrupt:
#     exit(0)


@app.route('/')
def index():
    load_levels()
    global player_name
    global game
    player_name = ''
    game = None
    return render_template('index.html')


@app.route('/get-levels-showcase', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        data = request.form

        if data['player_name'] == '':
            return render_template('index.html')
        global player_name
        player_name = data['player_name']
        return redirect(
            url_for('levels_showcase'))
    return render_template('index.html')


@app.route('/levels-showcase')
def levels_showcase():
    global player_name
    if player_name.__eq__(''):
        return redirect(url_for('index'))

    return render_template('levels-showcase.html', player_name=player_name)


@app.route('/get-level-num', methods=['GET'])
def get_level():
    if request.method == 'GET':
        return jsonify({'levelNum': get_number_of_levels()})


@app.route('/get-leaderboard', methods=['POST'])
def get_leaderboard():
    level = request.json['level']

    if request.method == 'POST':
        return jsonify({'leaderboard': get_all_record_for_a_level_ranked(int(level))})


@app.route('/game/<int:level_id>')
def game(level_id):
    global player_name
    if player_name.__eq__(''):
        return redirect(url_for('index'))
    global current_level_id
    global game
    global in_game
    current_level_id = level_id
    in_game = True
    game = Sokoban(player_name, level_id)

    height = len(game.map)
    width = len(game.map[0])

    if (current_level_id < get_number_of_levels()):
        next_level_id = current_level_id + 1
    else:
        next_level_id = current_level_id
    return render_template('game.html',
                           current_player=player_name,
                           grid_height=height,
                           grid_width=width,
                           boxes=game.get_box_coordinates(),
                           goals=game.get_goal_coordinates(),
                           player=game.get_player_coordinates(),
                           walls=game.get_wall_coordinates(),
                           moves=game.moves, current_level_id=current_level_id, next_level_id=next_level_id)


@app.route('/update', methods=['POST'])
def make_move():
    global game
    if not game:
        return jsonify({'error': 'Game has not been initialized.'}), 500

    data = request.json
    direction = data['direction']
    if not game.try_to_move(direction):
        return jsonify({'result': True, 'boxes': game.get_box_coordinates(),
                        'goals': game.get_goal_coordinates(),
                        'player': game.get_player_coordinates(),
                        'walls': game.get_wall_coordinates(),
                        'moves': game.moves,
                        'name': player_name})
    result = (game.check_win())
    global in_game
    if result and in_game:
        in_game = False
        return jsonify({'result': False, 'boxes': game.get_box_coordinates(),
                        'goals': game.get_goal_coordinates(),
                        'player': game.get_player_coordinates(),
                        'walls': game.get_wall_coordinates(),
                        'moves': game.moves,
                        'name': player_name})

    return jsonify({'result': True, 'boxes': game.get_box_coordinates(),
                    'goals': game.get_goal_coordinates(),
                    'player': game.get_player_coordinates(),
                    'walls': game.get_wall_coordinates(),
                    'moves': game.moves,
                    'name': player_name})


@app.route('/reset-cur', methods=['POST'])
def reset_current_level():
    global game
    global in_game
    global current_level_id
    in_game = True
    game = Sokoban(player_name, current_level_id)
    return jsonify({'result': True, 'boxes': game.get_box_coordinates(),
                    'goals': game.get_goal_coordinates(),
                    'player': game.get_player_coordinates(),
                    'walls': game.get_wall_coordinates(),
                    'moves': game.moves,
                    'name': player_name})


@app.route('/save', methods=["POST"])
def save():
    try:
        insert_level_record_data(player_name, current_level_id, game.moves)
        return "OK", 200
    except:
        return "Error", 500


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
