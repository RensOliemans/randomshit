from collections import namedtuple

import pandas as pd
import numpy as np

from sklearn import svm

DATA_DIR = 'data/'
DATA_FILE = 'spi_matches.csv'  # The large dataset
# DATA_FILE = 'wc_matches_train.csv'  # The dataset with world cup 2018 results

PROB_FILE = 'wc_matches.csv'  # file with the matches which have to be played, with their probabilities

Game = namedtuple('Game', 'team1 team2 prob1 prob2 score1 score2')

csv = pd.read_csv(DATA_DIR + DATA_FILE)


def get_dataset(games, diff):
    '''
    converts a list of games to a generator, more in dataset format.
    :param diff:
        determines whether you want the goal difference or the 'base' amount of goals
        in a match. base example: in a 3-1, the 'base' level is 1.
    '''
    for game in games:
        score = game.score1 - game.score2 if diff else min(game.score1, game.score2)
        yield(((game.prob1, game.prob2), score))


def get_games(csv_file):
    for index, row in csv_file.iterrows():
        yield(Game(row['team1'], row['team2'], row['prob1'], row['prob2'], row['score1'], row['score2']))


def build_dataset(csv_file, diff=True):
    '''
    Takes a csv file as input and returns (data, target), a tuple containing the
    dataset needed for scikit-learn
    :param diff:
        Determines whether you want the target in the dataset to contain the goal
        difference or the 'base' amount of goals in a match.
        Base example: in a 3-1, the 'base' level is 1.
    '''
    games = get_games(csv_file)
    data, target = zip(*get_dataset(games, diff))

    zeros = np.zeros((len(data), 2))

    for x, item in enumerate(data):
        zeros[x] = data[x]
    data = zeros

    zeros = np.zeros((len(data), ))

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
    (data, target) = build_dataset(csv, diff=True)
    diff_clf = learn(data, target)

    (data, target) = build_dataset(csv, diff=False)
    base_clf = learn(data, target)

    for teams, probs in get_probs(pd.read_csv(DATA_DIR + PROB_FILE)):
        print(f"{teams[0]} - {teams[1]}")
        print(probs)
        difference, base = int(diff_clf.predict([probs])[0]), int(base_clf.predict([probs])[0])
        score = [base, base]
        if difference > 0:
            score[0] += difference
        else:
            score[1] -= difference
        print(f"{score[0]} - {score[1]}\n")
