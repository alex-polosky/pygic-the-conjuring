import json
import os
import sys
from lark import Lark
from lark.exceptions import UnexpectedCharacters

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sometimes I really hate windows
sys.path.append(os.path.dirname(BASE_DIR))

from grammar.preprocess import preprocess


with open(os.path.join(BASE_DIR, 'full-test.lark'), encoding='utf-8') as f:
    grammar = f.read()

parser = Lark(grammar, import_paths=[BASE_DIR], parser='lalr', debug=True)

with open(os.path.join(BASE_DIR, '..', 'data', 'oracle_only.sorted.txt'), encoding='utf-8') as f:
    test_data = f.read()

pp_data = [
    x
        for y in preprocess(test_data)
    for x in y
]
got_words = []
missing_words = {}

def handle_bad_tokens(expr: str, ex: UnexpectedCharacters):
    if ex.token_history:
        prior_token = ex.token_history[-1]
    else:
        prior_token = None

    try:
        in_str = {s: s in expr[ex.pos_in_stream:] for s in (' .,:;')}
        end_pos = min(expr.index(s, ex.pos_in_stream) for s in in_str if in_str[s]) if any(in_str.values()) else None
    except ValueError:
        end_pos = None

    word = expr[ex.pos_in_stream:end_pos]
    if word not in missing_words:
        missing_words[word] = set()

    missing_words[word].add(repr(prior_token))

    if not end_pos:
        return

    next_expr = expr[end_pos + 1:]
    try:
        _ = parser.parse(next_expr)
    except UnexpectedCharacters as ex:
        handle_bad_tokens(next_expr, ex)

good = 0
total = 0
with open(os.path.join(BASE_DIR, 'test-consume.txt'), 'w', encoding='utf-8') as f:
    for data in pp_data:
        f.write(data + '\n')
        total += 1

        try:
            result = parser.parse(data)
            f.write(str(result) + '\n')
            good += 1
            for token in result.children:
                if token not in got_words:
                    got_words.append(token)
        except UnexpectedCharacters as ex:
            handle_bad_tokens(data, ex)

        f.write('\n')

with open(os.path.join(BASE_DIR, 'test-consume.json'), 'w', encoding='utf-8') as f:
    json.dump({k: list(missing_words[k]) for k in sorted(missing_words.keys(), key=str.casefold)}, f, indent=4)

print(f'Lines able to tokenize {good} / {total} : {((good / total) * 100):2.2f}%')
print(f'Recognized tokens {len(got_words)} / {len(got_words) + len(missing_words)} : {(len(got_words) / (len(got_words) + len(missing_words)) * 100):2.2f}%')
print('')

pass
