import pymongo
from pymongo import MongoClient
import json

levels = []


def load_levels():
    # load data from json file in static folder
    level_data = open('static/levels.json', 'r')
    global levels
    levels = json.loads(level_data.read())


def get_level(level_id):
    return levels['levels'][level_id - 1]


def get_number_of_levels():
    return len(levels['levels'])


def get_all_levels():
    return levels['levels']


# this is for online


password = "thisispassword"
connection_string = f"mongodb+srv://sokoban:{password}@sokoban.etzck3n.mongodb.net/?retryWrites=true&w=majority&appName=Sokoban"
client = MongoClient(connection_string)
database = client.sokoban


def insert_level_record_data(player_name, level_id, moves):
    collection = database.level_record
    game_data = {
        'player_name': player_name,
        'level_id': level_id,
        'moves': moves
    }
    collection.insert_one(game_data)


def validate_connection():
    collist = database.list_collection_names()
    if "level_record" in collist:
        return True
    return False


def create_collection():
    if not validate_connection():
        database.create_collection("level_record")
        print('Collection created')


def get_all_level_record():
    collection = database.level_record
    level_record_list = []
    for x in collection.find():
        level_record_list.append([x.get('player_name'), x.get('level_id'), x.get('moves')])
    return level_record_list


def get_all_record_for_a_level(level_id):
    collection = database.level_record
    level_record_list = []
    for x in collection.find({'level_id': level_id}):
        level_record_list.append([x.get('player_name'), x.get('level_id'), x.get('moves')])
    return level_record_list


def get_all_record_for_a_level_ranked(level_id):
    collection = database.level_record
    level_record_list = []
    for x in collection.find({'level_id': level_id}).sort('moves', 1):
        level_record_list.append([x.get('player_name'), x.get('level_id'), x.get('moves')])
    return level_record_list
