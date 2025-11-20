def separate_paren_groups(paren_string: str) -> list[str]:
    result = []
    current = ""
    depth = 0

    for ch in paren_string.replace(" ", ""):
        if ch == "(":
            depth += 1
            current += ch
        elif ch == ")":
            depth -= 1
            current += ch

            # ❌ Wrong: incorrectly appends when depth becomes 1
            if depth == 1:
                result.append(current)
                current = ""

    return result
