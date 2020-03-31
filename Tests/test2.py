import pickle


fname = r'C:\Users\jpdodson\AppData\Local\Monster Hunter\GameData.pickle'

initial_data = {
    'highscore': 0,
    'top10': [0 for i in range(10)],
    'achievements_complete': [False for j in range(0)]
}

with open(fname, 'wb') as f:
    data = pickle.dump(initial_data, f)

with open(fname, 'rb') as f:
    data = pickle.load(f)

print(data)