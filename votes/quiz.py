from fractions import Fraction
from operator import itemgetter
from collections import Counter, namedtuple

fraction_sort_key = lambda x: x[1].fraction

class Score(object):

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        self.fraction = Fraction(numerator, denominator)

    def __eq__(self, other):
        return type(self) == type(other) and \
            (self.numerator, self.denominator) == (other.numerator, other.denominator)

    def __hash__(self):
        return hash((self.numerator, self.denominator))

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)

class Quiz(object):

    def __init__(self, response):
        self.response = response
        self.systems = Counter()
        self.potential = Counter()
        self.system_score = {}
        self.system_order = []

    def calculate(self):
        for answer in self.response.answers:
            for system in answer.systems:
                self.systems[system] += 1
            for potential_answer in answer.question.answers:
                for system in potential_answer.systems:
                    self.potential[system] += 1

        self.system_score = { i: Score(j, self.potential[i]) for i, j in self.systems.items()}

        sorted_systems = sorted(self.system_score.items(), key=fraction_sort_key, reverse=True)
        self.system_order = [i for i, j in sorted_systems]

        return self

    def winners(self):
        if self:
            top = self[0]
            winners = []
            for i in self:
                if i[1].fraction == top[1].fraction:
                    winners.append(i[0])
                else:
                    break

            return winners
        else:
            return []


    def __getitem__(self, key):
        if isinstance(key, int):
            system = self.system_order[key]
            return (system, self.system_score[system])
        else:
            return (key, self.system_score[key])

    def __iter__(self):
        for system in self.system_order:
            yield (system, self.system_score[system])

    def __len__(self):
        return len(self.system_score)
