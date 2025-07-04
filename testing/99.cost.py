import os
from lark import Lark, Tree, Transformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# with open(os.path.join(BASE_DIR, f'{os.path.basename(__file__)[:-3]}.lark'), encoding='utf-8') as f:
#     grammar = f.read()
grammar = r'''
%import common.WS_INLINE
%ignore WS_INLINE

%import primitives (_A,_B,_C,_D,_E,_F,_G,_H,_I,_J,_K,_L,_M,_N,_O,_P,_Q,_R,_S,_T,_U,_V,_W,_X,_Y,_Z)
%import types (card_type, subtype, cost, CARD_TYPE, SUBTYPE_LAND, SUBTYPE_BASICLAND, INVERT_TYPE)

COMMA       : ","

start: (COMMA? cost)*
'''

class Autobot(Transformer):
    pass

parser = Lark(grammar, import_paths=[BASE_DIR], parser='lalr', debug=True)
transformer = Autobot()

# test it:
for expr, expected in (
('{0}', ''),
('{1}', ''),
('{10}', ''),
('{11}', ''),
('{12}', ''),
('{13}', ''),
('{14}', ''),
('{15}', ''),
('{16}', ''),
('{2}', ''),
('{2/B}', ''),
('{2/G}', ''),
('{2/R}', ''),
('{2/U}', ''),
('{2/W}', ''),
('{3}', ''),
('{4}', ''),
('{5}', ''),
('{6}', ''),
('{7}', ''),
('{8}', ''),
('{9}', ''),
('{B}', ''),
('{B/G}', ''),
('{B/P}', ''),
('{B/R}', ''),
('{C}', ''),
('{C/B}', ''),
('{C/G}', ''),
('{C/R}', ''),
('{C/U}', ''),
('{C/W}', ''),
('{CHAOS}', ''),
('{E}', ''),
('{G}', ''),
('{G/P}', ''),
('{G/U}', ''),
('{G/U/P}', ''),
('{G/W}', ''),
('{G/W/P}', ''),
('{P}', ''),
('{Q}', ''),
('{R}', ''),
('{R/G}', ''),
('{R/G/P}', ''),
('{R/P}', ''),
('{R/W}', ''),
('{R/W/P}', ''),
('{S}', ''),
('{T}', ''),
('{U}', ''),
('{U/B}', ''),
('{U/P}', ''),
('{U/R}', ''),
('{W}', ''),
('{W/B}', ''),
('{W/P}', ''),
('{W/U}', ''),
('{X}', ''),
('{Y}', ''),
('{Z}', ''),
('{3}{R}{R}{G}{G}', ''),
('{3}{R}{R}{G}{G}', ''),
('{3}{R}, {T}', ''),
):
    print(expr)

    tree = parser.parse(expr)
    if isinstance(tree, Tree):
        print(tree.pretty())
    else:
        print(tree)

    result = transformer.transform(tree)
    # print(result)

    # print(result == expected)

    print('')
