"""
This module represents a dice object. The dice can have any amount of faces
and can be weighted or not.
"""
from numpy.random import choice
from fractions import Fraction


class Dice(object):

    def __init__(self, faces=[1, 2, 3, 4, 5, 6], weight=None):
        if weight is None:
            # set weight to be [1,1,1,...] (fair dice)
            weight = [1 for _ in range(len(faces))]
        self.faces = faces
        if len(weight) != len(faces):
            raise ValueError("Length of weight must be the same as the amount"
                             "of faces!")

        self.weight = self._determine_integer_weight(weight)
        # fair if all weights are the same
        self.is_fair = all([x == weight[0] for x in weight])
        # normalise the weights
        sum_weight = sum(weight)
        self.normalised_weight = self.weight
        for i, val in enumerate(weight):
            self.normalised_weight[i] = val / sum_weight

    def roll(self, times=1):
        rolls = list()
        for _ in range(times):
            rolls.append(choice(self.faces, p=self.normalised_weight))
        return rolls

    def get_weight(self):
        return self.weight

    def change_faces(self, faces=None):
        if faces and len(faces) == len(self.weight):
            self.faces = faces
        else:
            raise ValueError("Amount of faces must be the same as the length "
                             "of weights!")

    def change_weight(self, weight=None):
        if weight and len(weight) == len(self.faces):
            sum_weight = sum(weight)
            for i, val in enumerate(weight):
                self.weight[i] = val / sum_weight
        else:
            raise ValueError("Length of weight must be the same as the amount "
                             "of faces!")

    def _determine_integer_weight(self, weight):
        fractions = [Fraction(x).limit_denominator() for x in weight]
        highest_denominator = max([x.denominator for x in fractions])
        # round instead of int - incorrect conversion from float to fraction
        # and vice versa might lead to something like 56.9999999999 - which
        # should be 57 instead of 56, which is what would happen if int() would
        # do the job
        return [round(x * highest_denominator) for x in weight]

    def __str__(self):
        return "Dice, faces: {}.".format(self.faces)

    def __repr__(self):
        return "Dice, faces: {}, weight: {}".format(self.faces, self.weight)

    def __eq__(self, other):
        return self.faces == other.faces and self.weight == other.weight
