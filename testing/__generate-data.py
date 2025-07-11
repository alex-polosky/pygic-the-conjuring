import os
import sys
from hypothesis import given, strategies as st
from hypothesis.extra.lark import from_lark
from lark import Lark

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

print('Creating grammar...')
grammar = create_grammar()
print('Creating parser...')
parser = Lark(grammar, import_paths=[BASE_DIR, os.path.join(BASE_DIR, 'grammar')], parser='lalr', debug=True)
print('parser done')

@given(from_lark(parser))
def test_with_random_input(s):
    # s is a randomly-generated text matching your grammar
    tree = parser.parse(s)
    # …do whatever you like with tree…
    print(s)


@given(from_lark(parser).filter(str.isascii))
def test_ascii_only(s: str):
    # any s that slips through will be pure ASCII
    with open(os.path.join(BASE_DIR, 'data', '__grammar-gen.txt'), 'a') as f:
        f.write(s + '\n')

if __name__ == '__main__':
        for _ in range(100):
            test_ascii_only()
