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

good = 0
total = 0
missing_words = {}
with open(os.path.join(BASE_DIR, 'test-consume.txt'), 'w', encoding='utf-8') as f:
    for data in pp_data:
        f.write(data + '\n')
        total += 1

        try:
            result = parser.parse(data)
            f.write(str(result) + '\n')
            good += 1
        except UnexpectedCharacters as ex:
            if ex.token_history:
                prior_token = ex.token_history[-1]
            else:
                prior_token = None
            try:
                end_pos = data.index(' ', ex.pos_in_stream)
            except ValueError:
                end_pos = None
            word = data[ex.pos_in_stream:end_pos]
            if word not in missing_words:
                missing_words[word] = set()
            missing_words[word].add(repr(prior_token))

        f.write('\n')

with open(os.path.join(BASE_DIR, 'test-consume.json'), 'w', encoding='utf-8') as f:
    json.dump({k: list(v) for k,v in missing_words.items()}, f, indent=4, sort_keys=True)

print(f'Tokenizing {good} / {total} : {((good / total) * 100):2.2f}%')
print('')

pass
