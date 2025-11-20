def separate_paren_groups(paren_string: str) -> list[str]:
    s = paren_string.replace(" ", "")
    result = []
    current = ""
    depth = 0

    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1

        current += ch

        # ❌ Wrong: runs only when encountering "("
        if depth == 0 and ch == "(":
            result.append(current)
            current = ""

    return result
