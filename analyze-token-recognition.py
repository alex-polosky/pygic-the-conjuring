import json
import os
import sys
from lark import Lark
from lark.exceptions import UnexpectedCharacters

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(BASE_DIR))

from grammar.preprocess import preprocess

def create_grammar():

    with open(os.path.join(BASE_DIR, 'grammar', 'words.lark'), encoding='utf-8') as f:
        data = f.read().split('\n')

    parts = [[]]
    SKIP_NEXT = False
    for line in data:
        # Skip the import and blank line
        if SKIP_NEXT and not line:
            SKIP_NEXT = False
            continue
        if line and line[0] == '%':
            SKIP_NEXT = True
            continue

        if line and line[0] == '/':
            continue
        if '    |' in line:
            continue
        if ':' in line:
            parts[-1].append(line.split(':')[0].split('.')[0].strip())
            continue

        if not line:
            parts.append([])

    parts = [x for x in parts if x]

    stdout = sys.stdout

    s = ''
    sys.stdout = s

    s += '''%import common (DIGIT, WS_INLINE)
%ignore WS_INLINE

%import primitives (_A,_B,_C,_D,_E,_F,_G,_H,_I,_J,_K,_L,_M,_N,_O,_P,_Q,_R,_S,_T,_U,_V,_W,_X,_Y,_Z,_PLURAL,_POSSESSIVE)
%import primitives (WHOLE,ZERO,COMMA,PLUS,HYPHEN,SELF,SEMICOLON,COLON,PERIOD,DOT,BAR,PT,BRACKET_L,BRACKET_R)''' '\n'
    for part in parts:
        s += f'%import words ({",".join(part)})' '\n'

    s += '''%import types (CARD_TYPE,SUBTYPE_ARTIFACT,SUBTYPE_ENCHANTMENT,SUBTYPE_BASICLAND,SUBTYPE_LAND,SUBTYPE_PLANESWALKER,SUBTYPE_SPELL,SUBTYPE_CREATURE,SUBTYPE_PLANAR,SUBTYPE_DUNGEON,SUBTYPE_BATTLE,SUBTYPE_ROLE_TOKEN,SUPERTYPE)
%import types (COLOR,ENERGY_COST,TAP_COST,UNTAP_COST,MANA_COST,INVERT_TYPE,PW_COST)
// %import types (cost,subtype,card_type)
%import abilities (ABILITY, IMPLICIT)
%import counters.MARKER
%import keywords.KEYWORD
''' '\n'
    s += f'''start: (ABILITY|IMPLICIT|MARKER|KEYWORD
    |WHOLE|ZERO|COMMA|PLUS|HYPHEN|SELF|COLON|SEMICOLON|PERIOD|DOT|BAR|PT|BRACKET_L|BRACKET_R
    |CARD_TYPE|SUBTYPE_ARTIFACT|SUBTYPE_ENCHANTMENT|SUBTYPE_BASICLAND|SUBTYPE_LAND|SUBTYPE_PLANESWALKER|SUBTYPE_SPELL|SUBTYPE_CREATURE|SUBTYPE_PLANAR|SUBTYPE_DUNGEON|SUBTYPE_BATTLE|SUBTYPE_ROLE_TOKEN|SUPERTYPE|COLOR|ENERGY_COST|TAP_COST|UNTAP_COST|MANA_COST|INVERT_TYPE|PW_COST
    |{"|".join(
    x
        for part in parts
    for x in part
)})*''' '\n'
    s += '\n'

    sys.stdout = stdout

    return s

def main():

    print('Creating grammar...')
    grammar = create_grammar()
    print('Creating parser...')
    parser = Lark(grammar, import_paths=[BASE_DIR, os.path.join(BASE_DIR, 'grammar')], parser='lalr', debug=True)

    print('Loading oracle data...')
    with open(os.path.join(BASE_DIR, 'data', 'out', 'oracle-text.txt'), encoding='utf-8') as f:
        test_data = f.read()

    print('Pre-processing full oracle data...')
    pp_data = [
        x
            for y in preprocess(test_data)
        for x in y
    ]
    got_words = []
    missing_words = {}

    print(f'Discovered {len(pp_data)} total lines of oracle text')

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
            # missing_words[word] = set()
            missing_words[word] = dict()

        if prior_token not in missing_words[word]:
            missing_words[word][prior_token] = 0

        missing_words[word][prior_token] += 1

        # missing_words[word].add(repr(prior_token))

        if not end_pos:
            return

        next_expr = expr[end_pos + 1:]
        try:
            _ = parser.parse(next_expr)
        except UnexpectedCharacters as ex:
            handle_bad_tokens(next_expr, ex)

    good = 0
    total = 0
    with open(os.path.join(BASE_DIR, 'data', 'out', 'analyze-tokens-result.txt'), 'w', encoding='utf-8') as f:
        for i, data in enumerate(pp_data):
            if i and i % 1_000 == 0:
                print(f'Gone through {i} lines: {i/len(pp_data)*100:0.2f}%')
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

    for k0, v0 in missing_words.items():
        for k1, v1 in v0.items():
            pass

    def get_max_value(nested_dict):
        if not nested_dict:
            return 0
        return max(nested_dict.values())

    # data_by_key = {k: (missing_words[k]) for k in sorted(missing_words.keys(), key=str.casefold)}
    data_by_key = dict(sorted(missing_words.items(), key=lambda x: str.casefold(x[0])))
    data_by_num = dict(sorted(missing_words.items(), key=lambda x: get_max_value(x[1]), reverse=True))

    with open(os.path.join(BASE_DIR, 'data', 'out', 'analyze-tokens-result-missing.json'), 'w', encoding='utf-8') as f:
        json.dump(data_by_key, f, indent=4)

    with open(os.path.join(BASE_DIR, 'data', 'out', 'analyze-tokens-result-missing-byweight.json'), 'w', encoding='utf-8') as f:
        json.dump(data_by_num, f, indent=4)

    print(f'Lines able to tokenize {good} / {total} : {((good / total) * 100):2.2f}%')
    print(f'Recognized tokens {len(got_words)} / {len(got_words) + len(missing_words)} : {(len(got_words) / (len(got_words) + len(missing_words)) * 100):2.2f}%')
    print('')

    print("Top 10 keys sorted by highest nested value:")
    print("-" * 50)
    for i, (key, nested_dict) in enumerate(data_by_num.items()):
        if i >= 10:
            break
        max_val = get_max_value(nested_dict)
        max_key = max(nested_dict.keys(), key=lambda k: nested_dict[k])
        print(f"{i+1:2d}. {key:<15} | Max value: {max_val:3d} (key: '{max_key}')")

    print('')

if __name__ == '__main__':
    main()
