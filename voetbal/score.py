import pandas as pd
from collections import namedtuple
import math

import generator

Match = namedtuple('Match', 'team1 team2 pred1 pred2 out1 out2')


def calculator(fun, df):
    correct, score = 0, 0
    for index, row in df.iterrows():
        prob1, prob2, = row['prob1'], row['prob2']
        score1, score2 = row['score1'], row['score2']
        if math.isnan(score1):
            continue
        pred1, pred2 = fun(prob1, prob2)
        pred_score = points((score1, score2), (pred1, pred2))
        if pred_score == 200:
            correct += 1
        score += pred_score
    return correct, score


def points(results, prediction):
    score = 0
    if results == prediction:
        # correct prediction
        return 200
    if results[0] == results[1] and prediction[0] == prediction[1]:
        # correctly predicted a draw
        return 100
    real_winner = results[0] > results[1]
    predicted_winner = prediction[0] > prediction[1]
    if real_winner == predicted_winner and results[0] != results[1] and prediction[0] != prediction[1]:
        # correct winner (no draw)
        score = 75
    if results[0] == prediction[0] or results[1] == prediction[1]:
        # correct amount of goals of one team
        score += 20
    return score


def main():
    df = pd.read_csv('wc_matches.csv', usecols=['team1', 'team2', 'prob1', 'prob2', 'score1', 'score2'])
    total_correct, total_score = 0, 0
    num = 1500
    for _ in range(num):
        correct, score = calculator(generator.main, df)
        total_correct += correct
        total_score += score
    print(f"Average correct guesses: {total_correct / num:.2f}\n"
          f"Average score: {round(total_score / num)}")


def main2():
    df = pd.read_csv('wc_matches.csv', usecols=['team1', 'team2', 'prob1', 'prob2', 'score1', 'score2'])
    correct, score = 0, 0
    for index, row in df.iterrows():
        team1, team2 = row['team1'], row['team2']
        prob1, prob2, = row['prob1'], row['prob2']
        score1, score2 = row['score1'], row['score2']
        if math.isnan(score1):
            continue
        pred1, pred2 = generator.main(prob1, prob2)
        pred_score = points((score1, score2), (pred1, pred2))
        if pred_score == 200:
            correct += 1
        score += pred_score
        print((Match(team1, team2, pred1, pred2, score1, score2), pred_score))
    print(f"c {correct}\ts {score}")


if __name__ == '__main__':
    main()
