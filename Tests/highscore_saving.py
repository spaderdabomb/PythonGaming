import pickle

class GameData():
    '''
    Stores persistent data
    '''

    # Initializes data dictionary keys for saving and loading data
    NUM_ACHIEVEMENTS = 0
    FILE_NAME = 'GameData.pickle'
    initial_data = {
        'highscore': 0,
        'top10': [0 for i in range(10)],
        'achievements_complete': [False for j in range(NUM_ACHIEVEMENTS)]
    }
    data = initial_data

    @staticmethod
    def __init__():
        '''
        When GameData class is initialized, it tries to load previous GameData
        '''
        GameData.load_data()

    @staticmethod
    def save_data():
        '''
        Saves data
        '''
        try:
            with open(GameData.FILE_NAME, 'wb') as f:
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
            with open(GameData.FILE_NAME, 'rb') as f:
                data = pickle.load(f)
        except:
            pass

        GameData.data = data

        return data

    @staticmethod
    def clear_data(self):
        '''
        Resets data back to initial values
        '''
        GameData.data = GameData.initial_data

    @staticmethod
    def get_key_value(key):
        return GameData.data[key]

    @staticmethod
    def set_key_value(key, value):
        GameData.data[key] = value


# attributes = inspect.getmembers(GameData, lambda a:not(inspect.isroutine(a)))
# print([a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])

GameData()
print(GameData.get_key_value('highscore'))
print(GameData.data['highscore'])

