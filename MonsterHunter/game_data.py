import os
import pickle

class GameData():
    '''
    Stores persistent data
    '''

    # Initializes data dictionary keys for saving and loading data
    NUM_ACHIEVEMENTS = 0
    DATA_FILE_PATH = None
    initial_data = {
        'highscore': 0,
        'top10': [0 for i in range(10)],
        'achievements_complete': [False for j in range(NUM_ACHIEVEMENTS)]
    }
    data = initial_data

    @staticmethod
    def __init__(game_name):
        '''
        When GameData class is initialized, it tries to load previous GameData
        '''
        #
        print(GameData.data)

        # Create local data folder and files for game
        home = os.path.expanduser('~')
        local_data_path = 'AppData\\Local\\' + game_name
        data_file_name = 'GameData.pickle'
        game_data_path = os.path.join(home, local_data_path)
        file_path = os.path.join(game_data_path, data_file_name)

        # Create local folder
        GameData.DATA_FILE_PATH = file_path
        if not os.path.exists(game_data_path):
            os.makedirs(game_data_path)

        # Load data if file exists, otherwise create initial file
        if os.path.exists(GameData.DATA_FILE_PATH):
            GameData.load_data()
        else:
            GameData.save_data()

    @staticmethod
    def save_data():
        '''
        Saves data
        '''
        try:
            with open(GameData.DATA_FILE_PATH, 'wb') as f:
                pickle.dump(GameData.data, f, pickle.HIGHEST_PROTOCOL)
        except:
            pass

    @staticmethod
    def load_data():
        '''
        Loads data
        '''
        data = None
        try:
            with open(GameData.DATA_FILE_PATH, 'rb') as f:
                data = pickle.load(f)
                GameData.data = data
        except:
            pass

        return GameData.data

    @staticmethod
    def clear_data(self):
        '''
        Resets data back to initial values
        '''
        GameData.data = GameData.initial_data

    @staticmethod
    def get_key_value(key):
        return GameData.data.get(key)

    @staticmethod
    def set_key_value(key, value):
        GameData.data[key] = value