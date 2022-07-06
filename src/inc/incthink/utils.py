import random


def prob_generator(number):
    return 1 / (number + 0.2)


def convert_prob_to_bool(prob: float) -> bool:
    """Converts a probability to a True with probability = prob.

    Args:
        prob (float): Probability of True.

    Returns:
        bool: True with probability = prob.
    """
    return random.random() < prob
