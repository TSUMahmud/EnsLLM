from typing import List
from itertools import combinations

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    for a, b in combinations(numbers, 2):
        if abs(a - b) < threshold:
            return True
    return False
