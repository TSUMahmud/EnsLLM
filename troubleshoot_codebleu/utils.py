import re
from tree_sitter_languages import get_language


def get_tree_sitter_language(lang: str):
    """
    Patched version of CodeBLEU tree-sitter loader.
    Works on Python 3.12 and Windows/Linux/Mac.
    """

    lang = lang.lower()

    # Map CodeBLEU expected lang names to tree_sitter_languages names
    mapping = {
        "python": "python",
        "py": "python",
        "java": "java",
        "javascript": "javascript",
        "js": "javascript",
        "cpp": "cpp",
        "c++": "cpp",
        "c": "c",
        "go": "go",
        "ruby": "ruby",
        "rust": "rust",
        "typescript": "typescript",
        "php": "php",
    }

    if lang not in mapping:
        raise ValueError(f"Unsupported language: {lang}")

    return get_language(mapping[lang])


def count_ngram(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def clean_code(code: str) -> str:
    """Remove comments & extra whitespace."""
    code = re.sub(r"#.*", "", code)
    code = re.sub(r"//.*", "", code)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    code = re.sub(r"\s+", " ", code)
    return code.strip()
