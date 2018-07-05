from collections import namedtuple

import pandas as pd
import numpy as np

from sklearn import svm

DATA_DIR = 'data/'
DATA_FILE = 'spi_matches.csv'
# DATA_FILE = 'wc_matches_train.csv'

PROB_FILE = 'wc_matches.csv'

Game = namedtuple('Game', 'team1 team2 prob1 prob2 score1 score2')

csv = pd.read_csv(DATA_DIR + DATA_FILE)


def get_dataset(games, diff):
    if diff:
        for game in games:
            yield(((game.prob1, game.prob2), (game.score1 - game.score2)))
    else:
        for game in games:
            yield(((game.prob1, game.prob2), min(game.score1, game.score2)))


def get_games(csv_file):
    for index, row in csv_file.iterrows():
        yield(Game(row['team1'], row['team2'], row['prob1'], row['prob2'], row['score1'], row['score2']))


def build_dataset(csv_file, diff=True):
    games = list(get_games(csv_file))
    dataset = list(get_dataset(games, diff))

    data = [x[0] for x in dataset]
    data_len = len(data)

    zeros = np.zeros((data_len, 2))

    for x, item in enumerate(data):
        zeros[x] = data[x]
    data = zeros

    target = [x[1] for x in dataset]
    zeros = np.zeros((data_len, ))

    for x, item in enumerate(target):
        zeros[x] = target[x]
    target = zeros

    return (data, target)


def learn(data, target):
    clf = svm.LinearSVC()
    clf.set_params(penalty='l1', loss='squared_hinge', dual=False)
    clf.fit(data, target)
    return clf


def get_probs(csv_file):
    for index, row in csv_file.iterrows():
        yield(((row['team1'], row['team2']), (row['prob1'], row['prob2'])))


if __name__ == '__main__':
    (data, target) = build_dataset(csv, True)
    diff_clf = learn(data, target)

    (data, target) = build_dataset(csv, False)
    abs_clf = learn(data, target)

    for teams, probs in get_probs(pd.read_csv(DATA_DIR + PROB_FILE)):
        print(f"{teams[0]} - {teams[1]}")
        print(probs)
        difference, base = int(diff_clf.predict([probs])[0]), int(abs_clf.predict([probs])[0])
        score = [base, base]
        if difference > 0:
            score[0] = score[0] + difference
        else:
            score[1] = score[1] + abs(difference)
        print(f"{score[0]} - {score[1]}\n")
