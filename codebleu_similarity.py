from codebleu import calc_codebleu
from typing import Callable

def codebleu_similarity(func1: Callable, func2: Callable) -> float:
    """
    Computes CodeBLEU similarity score between two functions based on syntax and data flow similarity.

    :param func1: First function to compare.
    :param func2: Second function to compare.
    :return: CodeBLEU score (between 0 and 1).
    """
    syntax_weight = 0.5
    dataflow_weight = 0.5

    codebleu_score = calc_codebleu(
        [func1],
        func2,
        lang="python",
        # weights=(syntax_weight, 0, dataflow_weight, 0)
    )

    SSim = codebleu_score["codebleu"]

    return SSim