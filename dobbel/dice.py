"""
This module represents a dice object. The dice can have any amount of faces
and can be weighted or not.
"""
from fractions import Fraction
from numpy.random import choice


class Dice(object):

    def __init__(self, faces=None, weight=None):
        faces = faces or [1, 2, 3, 4, 5, 6]
        # set weight to be [1,1,1,...] (fair dice)
        weight = weight or [1] * len(faces)
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

    def roll(self, times=1) -> list():
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

    def __str__(self):
        return f"Dice, faces: {self.faces}."

    def __repr__(self):
        return f"Dice, faces: {self.faces}, weight: {self.weight}"

    def __eq__(self, other):
        return self.faces == other.faces and self.weight == other.weight

    @classmethod
    def _determine_integer_weight(cls, weight):
        fractions = [Fraction(x).limit_denominator() for x in weight]
        highest_denominator = max([x.denominator for x in fractions])
        # round instead of int - incorrect conversion from float to fraction
        # and vice versa might lead to something like 56.9999999999 - which
        # should be 57 instead of 56, which is what would happen if int() would
        # do the job
        return [round(x * highest_denominator) for x in weight]
