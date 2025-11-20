from .utils import get_tree_sitter_language, count_ngram, clean_code
from collections import Counter
import math
from tree_sitter import Parser

AVAILABLE_LANGS = [
    "python", "java", "javascript", "js",
    "cpp", "c++", "c", "go", "php", "ruby",
    "rust", "typescript"
]


def calc_syntax_match(references, hypothesis, lang):
    language = get_tree_sitter_language(lang)

    parser = Parser()
    parser.set_language(language)

    def get_tree(code):
        return parser.parse(bytes(code, "utf8"))

    ref_tree = get_tree(references[0])
    hyp_tree = get_tree(hypothesis)

    return 1.0 if ref_tree.root_node.sexp() == hyp_tree.root_node.sexp() else 0.0


def calc_dataflow_match(references, hypothesis, lang):
    # Dataflow match is often disabled (weight=0)
    return 0.0


def calc_ngram_match(references, hypothesis, n=4):
    ref = clean_code(references[0])
    hyp = clean_code(hypothesis)

    ref_tokens = ref.split()
    hyp_tokens = hyp.split()

    if len(hyp_tokens) == 0:
        return 0.0

    weights = [1/n] * n
    score = 1.0

    for i in range(1, n+1):
        ref_counts = Counter(count_ngram(ref_tokens, i))
        hyp_counts = Counter(count_ngram(hyp_tokens, i))

        overlap = sum((ref_counts & hyp_counts).values())
        total_hyp = max(sum(hyp_counts.values()), 1)

        precision = overlap / total_hyp
        score *= precision ** weights[i - 1]

    # brevity penalty
    bp = math.exp(1 - len(ref_tokens)/len(hyp_tokens)) if len(hyp_tokens) < len(ref_tokens) else 1.0
    return bp * score


def calc_codebleu(references, hypothesis, lang="python", weights=(0.5, 0.1, 0.2, 0.2)):
    syntax_w, keywords_w, dataflow_w, ngram_w = weights

    syntax = calc_syntax_match(references, hypothesis, lang)
    ngram = calc_ngram_match(references, hypothesis)
    dataflow = calc_dataflow_match(references, hypothesis, lang)

    score = (
        syntax_w * syntax +
        ngram_w * ngram +
        dataflow_w * dataflow
    )

    return {
        "syntax": syntax,
        "ngram": ngram,
        "dataflow": dataflow,
        "codebleu": score
    }
