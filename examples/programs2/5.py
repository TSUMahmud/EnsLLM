from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    if len(numbers) < 2:
        return False
    return abs(numbers[0] - numbers[1]) < threshold
