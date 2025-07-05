import os
import sys

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'testing', 'words.lark'), encoding='utf-8') as f:
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

with open(os.path.join(BASE_DIR, 'testing', 'full-test.lark'), 'w', encoding='utf-8') as f:
    stdout = sys.stdout

    sys.stdout = f

    print('''%import common (DIGIT, WS_INLINE)
%ignore WS_INLINE

%import primitives (_A,_B,_C,_D,_E,_F,_G,_H,_I,_J,_K,_L,_M,_N,_O,_P,_Q,_R,_S,_T,_U,_V,_W,_X,_Y,_Z,_PLURAL,_POSSESSIVE)
%import primitives (WHOLE,ZERO,COMMA,PLUS,HYPHEN,SELF,SEMICOLON,COLON,PERIOD,DOT,BAR,PT)''')
    for part in parts:
        print(f'%import words ({",".join(part)})')

    print('''%import types (CARD_TYPE,SUBTYPE_ARTIFACT,SUBTYPE_ENCHANTMENT,SUBTYPE_BASICLAND,SUBTYPE_LAND,SUBTYPE_PLANESWALKER,SUBTYPE_SPELL,SUBTYPE_CREATURE,SUBTYPE_PLANAR,SUBTYPE_DUNGEON,SUBTYPE_BATTLE,SUBTYPE_ROLE_TOKEN,SUPERTYPE)
%import types (COLOR,ENERGY_COST,TAP_COST,UNTAP_COST,MANA_COST,INVERT_TYPE,PW_COST)
// %import types (cost,subtype,card_type)
%import abilities.ABILITY
%import abilities.IMPLICIT
%import counters.MARKER
%import keywords.KEYWORD
''')
    print(f'''start: (ABILITY|IMPLICIT|MARKER|KEYWORD|WHOLE|ZERO|COMMA|PLUS|HYPHEN|SELF|COLON|SEMICOLON|PERIOD|DOT|BAR|PT
    |CARD_TYPE|SUBTYPE_ARTIFACT|SUBTYPE_ENCHANTMENT|SUBTYPE_BASICLAND|SUBTYPE_LAND|SUBTYPE_PLANESWALKER|SUBTYPE_SPELL|SUBTYPE_CREATURE|SUBTYPE_PLANAR|SUBTYPE_DUNGEON|SUBTYPE_BATTLE|SUBTYPE_ROLE_TOKEN|SUPERTYPE|COLOR|ENERGY_COST|TAP_COST|UNTAP_COST|MANA_COST|INVERT_TYPE|PW_COST
    |{"|".join(
    x
        for part in parts
    for x in part
)})*''')
    print('')

    sys.stdout = stdout
