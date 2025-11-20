from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    nums = sorted(numbers)
    for i in range(len(nums) - 1):
        if abs(nums[i] - nums[i + 1]) < threshold:
            return True
    return False
