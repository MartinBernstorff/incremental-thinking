import random


def prob_generator(number):
    return 1 / (number + 0.2)


def convert_prob_to_bool(prob):
    return random.random() < prob
